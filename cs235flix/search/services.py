import math
from difflib import SequenceMatcher
from editdistance import distance
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domainmodel.movie import Movie
from cs235flix.services import movie_to_dict, get_page_items, get_number_pages
from cs235flix.movies.services import movies_to_dict
import string


def levenshtein_ratio(string1, string2):
    lv_ratio = ((len(string1) + len(string2)) - distance(string1, string2)) / (
            len(string1) + len(string2))

    return lv_ratio


def partial_ratio(string1, string2):
    if len(string1) == 0 or len(string1) == 0:
        return 0

    if len(string1) > len(string2):
        longer = string1
        shorter = string2
    else:
        longer = string2
        shorter = string1

    scores = []

    # list of triples (i, j, n), s.t. shorter[i:i+n] == longer[j:j+n]
    matching_blocks = SequenceMatcher(None, shorter, longer).get_matching_blocks()
    for block in matching_blocks[:len(matching_blocks) - 1]:
        long_start = block[1] if block[1] + len(shorter) < len(longer) else len(longer) - len(shorter)
        k_len_substring = longer[long_start:long_start + len(shorter)]
        substring_start = block[1]
        while substring_start >= 0 and longer[substring_start] != " ":
            substring_start -= 1
        substring_end = longer.find(" ", block[1])
        if SequenceMatcher(None, shorter, longer[substring_start:substring_end]).ratio() > 0.6 or SequenceMatcher(None,
                                                                                                                  shorter,
                                                                                                                  k_len_substring).ratio() > 0.8:
            scores.append(max(levenshtein_ratio(shorter, k_len_substring),
                              levenshtein_ratio(shorter, longer[substring_start:substring_end])))

    return max(scores) if len(scores) > 0 else 0


def token_set_ratio(search_q, movie_str):
    search_q = search_q.lower()
    movie_str = movie_str.lower()

    matching_keywords = set()

    keyword_sum = 0

    for keyword in search_q.split():

        for movie_word in movie_str.split():
            lv_ratio = levenshtein_ratio(keyword, movie_word)
            if keyword not in matching_keywords and (lv_ratio > 0.8 or keyword in movie_word):
                matching_keywords.add(keyword)
                keyword_sum += lv_ratio

    return keyword_sum


def build_movie_string(movie: Movie):
    movie_str = " ".join(
        [movie.title, str(movie.release_year),
         " ".join([actor.actor_full_name for actor in movie.actors]), movie.director.director_full_name]).translate(
        str.maketrans('', '', string.punctuation))

    return movie_str


def search_tuple_to_movies_dict(movies_obj_tuple_list):
    movies_dict_list = list()
    for tup in movies_obj_tuple_list:
        movies_dict_list.append(movie_to_dict(tup[1]))
    return movies_dict_list


def get_page_items_movies_search(search_query: str, match_threshold: float, current_page_num: int,
                                 results_per_page: int,
                                 repo: AbstractRepository):
    search_result_set = []
    for movie in repo.get_all_movies():
        movie_str = build_movie_string(movie)
        tk_set_ratio = token_set_ratio(search_query, movie_str)
        if tk_set_ratio > match_threshold:
            search_result_set.append((tk_set_ratio, movie))

    search_result_set.sort(reverse=True)

    movies_obj_tuple_list, prev_page, next_page = get_page_items(current_page_num, results_per_page, search_result_set)
    number_pages = get_number_pages(results_per_page, len(search_result_set))
    number_results = len(search_result_set)

    return search_tuple_to_movies_dict(movies_obj_tuple_list), prev_page, next_page, number_pages, number_results
