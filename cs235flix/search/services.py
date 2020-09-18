import math
from difflib import SequenceMatcher
from editdistance import distance
from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domainmodel.movie import Movie
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
        if SequenceMatcher(None, shorter, longer[substring_start:substring_end]).ratio() > 0.6 or SequenceMatcher(None, shorter, k_len_substring).ratio()> 0.8:
            scores.append(max(levenshtein_ratio(shorter, k_len_substring), levenshtein_ratio(shorter, longer[substring_start:substring_end])))

    return max(scores) if len(scores) > 0 else 0


def token_set_ratio(string1, string2):
    string1 = string1.lower()
    string2 = string2.lower()

    string1_set = set(string1.split())
    string2_set = set(string2.split())

    intersect = string1_set.intersection(string2_set)
    string1_rest = string1_set.difference(string2_set)
    string2_rest = string2_set.difference(string1_set)

    intersect_sorted = " ".join(sorted(intersect)).strip()

    string_1_and_intersect = (intersect_sorted + " " + " ".join(sorted(string1_rest))).strip()
    string_2_and_intersect = (intersect_sorted + " " + " ".join(sorted(string2_rest))).strip()

    if max(len(string1), len(string2)) // min(len(string1), len(string2)) > 8:
        return max(levenshtein_ratio(string1, string2),
                   partial_ratio(string1, string2),
                   partial_ratio(string_1_and_intersect, string_2_and_intersect),
                    partial_ratio(intersect_sorted, string_2_and_intersect),
                    partial_ratio(intersect_sorted, string_1_and_intersect))*0.6

    return max(levenshtein_ratio(string1, string2),
               levenshtein_ratio(intersect_sorted, string_1_and_intersect),
               levenshtein_ratio(intersect_sorted, string_2_and_intersect),
               levenshtein_ratio(string_1_and_intersect, string_2_and_intersect))


def build_movie_string(movie: Movie):
    movie_str = " ".join(
        [movie.title, str(movie.release_year),
         " ".join([actor.actor_full_name for actor in movie.actors]), movie.director.director_full_name]).translate(str.maketrans('', '', string.punctuation))

    return movie_str


def get_next_n_search_results(search_query: str, match_threshold: float, page_num: int, results_per_page: int,
                              repo: AbstractRepository):
    search_result_set = []
    movies = list()
    for movie in repo.get_all_movies():
        movie_str = build_movie_string(movie)
        tk_set_ratio = token_set_ratio(search_query, movie_str)
        if tk_set_ratio > match_threshold:
            search_result_set.append((tk_set_ratio, movie))

    search_result_set.sort(reverse=True)

    next_page = prev_page = None

    if page_num * results_per_page <= len(search_result_set):
        for i in range(results_per_page):
            movies.append(movie_to_dict(search_result_set[(page_num - 1) * results_per_page + i][1]))
    else:
        for i in range(len(search_result_set) % max(((page_num - 1) * results_per_page), results_per_page)):
            movies.append(movie_to_dict(search_result_set[((page_num - 1) * results_per_page + i)][1]))

    if page_num > 1:
        prev_page = page_num - 1

    number_results = len(search_result_set)
    number_pages = math.ceil(len(search_result_set) / results_per_page)

    if page_num < number_pages:
        next_page = page_num + 1

    return movies, prev_page, next_page, number_pages, number_results


def movie_to_dict(movie: Movie):
    movie_dict = {
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'genres': movie.genres,
        'runtime_minutes': movie.runtime_minutes,
        'reviews': movie.get_reviews()
    }
    return movie_dict
