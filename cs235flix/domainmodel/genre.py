

class Genre:

    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if isinstance(other, Genre):
            return self.genre_name == other.genre_name
        return False

    def __lt__(self, other):
        if isinstance(other, Genre):
            if self.genre_name is None or other.genre_name is None:
                if self.genre_name is None and other.genre_name is None:
                    return False
                elif self.genre_name is not None and other.genre_name is None:
                    return self.genre_name < ""
                elif self.genre_name is None and other.genre_name is not None:
                    return "" < other.genre_name
            else:
                return self.genre_name < other.genre_name
        else:
            raise TypeError

    def __hash__(self):
        return hash(self.genre_name)