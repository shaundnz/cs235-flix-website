

class Director:

    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"{self.__director_full_name}"

    def __eq__(self, other):
        if isinstance(other, Director):
            return self.director_full_name == other.director_full_name
        return False

    def __lt__(self, other):
        if isinstance(other, Director):
            if self.director_full_name is None or other.director_full_name is None:
                if (self.director_full_name is None and other.director_full_name is None):
                    return False
                elif self.director_full_name is not None and other.director_full_name is None:
                    return self.director_full_name < ""
                elif self.director_full_name is None and other.director_full_name is not None:
                    return "" < other.director_full_name
            else:
                return self.director_full_name < other.director_full_name
        else:
            raise TypeError

    def __hash__(self):
        return hash(self.director_full_name)


