
class Entity:
    def __init__(self, name, entity_id, token):
        self.__name = name
        self.__entity_id = entity_id
        self.__token = token
        self.__player_limits = 0
        self.__expire_date = None

