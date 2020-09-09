from cs235flix.domainmodel.movie import Movie


class WatchList:

    def __init__(self):
        self.__watch_list = []
        self.__index = 0;

    def add_movie(self, movie):
        if type(movie) is Movie and movie not in self.__watch_list:
            self.__watch_list.append(movie)

    def remove_movie(self, movie):
        if type(movie) is Movie and movie in self.__watch_list:
            self.__watch_list.remove(movie)

    def select_movie_to_watch(self, index):
        if index < self.size():
            return self.__watch_list[index]
        else:
            return None

    def size(self):
        return len(self.__watch_list)

    def first_movie_in_watchlist(self):
        if self.size() > 0:
            return self.__watch_list[0]
        else:
            return None

    def __iter__(self):
        return self

    def __next__(self):
        if (self.__index >= len(self.__watch_list)):
            self.__index = 0
            raise StopIteration
        index = self.__index
        self.__index += 1
        return self.__watch_list[index]


