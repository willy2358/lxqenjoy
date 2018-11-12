
from GCore.Statement import Statement

# send some cards from a variable
# <send_cards player="@drawer" cards="@drawn_card" ></send_cards>
class SendCards(Statement):
    def __init__(self, cards, recv_player):
        self.__cards = cards
        self.__recv_player = recv_player

    def gen_runtime_obj(self, scene):

        player_func = self.__recv_player.gen_runtime_obj(scene)
        cards_func = self.__cards.gen_runtime_obj(scene)
        def send_cards_rtobj():
            playerRef = player_func()
            cardsRef = cards_func()
            player = scene.get_prop_value(playerRef.get_name())
            cards = scene.get_prop_value(cardsRef.get_name())
            if player and cards:
                player.send_cards(cards)

        return send_cards_rtobj
