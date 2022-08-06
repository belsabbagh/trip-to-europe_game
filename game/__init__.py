import random
from game import perks, player, play_turn_queue


class Game:
    __players_queue: play_turn_queue.PlayersQueue = play_turn_queue.PlayersQueue([])

    def __init__(self, players_list):
        self.__players_queue = play_turn_queue.PlayersQueue(players_list)

    @staticmethod
    def __move_player_to(current_player: player.Player, pos):
        current_player.set_position(pos)

    @staticmethod
    def __roll_dice() -> int:
        return random.randint(1, 6)

    def run_perk_for_player(self, current_player: player.Player):
        current_player_position = current_player.get_current_position()
        if current_player_position == 23:
            perks.all_players_go_back_3(self.__players_queue.get_all_players())
            return
        if current_player_position in perks.position_perks.keys():
            current_player.set_position(perks.position_perks[current_player_position])
            return
        if current_player_position in perks.play_again_perks:
            self.__run_turn(current_player)
            return

    def run_perks(self):
        [self.run_perk_for_player(i) for i in self.__players_queue.get_all_players()]

    def __run_turn(self, current_player: player.Player):
        current_dice_roll = Game.__roll_dice()
        print(f"Dice: {current_dice_roll}")
        next_position = current_player.get_current_position() + current_dice_roll
        for play in self.__players_queue.get_all_players():
            if play.get_current_position() is next_position:
                play.move_player(-1)
                break
        current_player.set_position(next_position)
        self.run_perks()

    def run_game(self):
        while max([i.get_current_position() for i in self.__players_queue.get_all_players()]) < 50:
            self.__run_turn(self.__players_queue.get_current_player())
            self.__players_queue.update_turn()
            print(self.__players_queue)
            print("----------------------")
