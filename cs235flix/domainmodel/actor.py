
class Actor:

    def __init__(self,  actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__colleagues = []

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        if isinstance(other, Actor):
            return self.actor_full_name == other.actor_full_name
        return False

    def __lt__(self, other):
        if isinstance(other, Actor):
            if self.actor_full_name is None or other.actor_full_name is None:
                if self.actor_full_name is None and other.actor_full_name is None:
                    return False
                elif self.actor_full_name is not None and other.actor_full_name is None:
                    return self.actor_full_name < ""
                elif self.actor_full_name is None and other.actor_full_name is not None:
                    return "" < other.actor_full_name
            else:
                return self.actor_full_name < other.actor_full_name
        else:
            raise TypeError

    def __hash__(self):
        return hash(self.actor_full_name)

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, Actor):
            self.__colleagues.append(colleague)
        else:
            raise TypeError("Can only add instances of 'Actor' class")

    def check_if_this_actor_worked_with(self, colleague):
        return self.__colleagues.__contains__(colleague)

