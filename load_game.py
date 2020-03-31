import pickle
from game import LoadedGame


def import_files():
    path = "game_save.txt"
    file = open(path, "rb")
    hints = pickle.load(file)
    notes = pickle.load(file)
    cells_list = pickle.load(file)
    unsolved_table = pickle.load(file)
    solved_table = pickle.load(file)
    saved_game_time = pickle.load(file)
    file.close()
    return hints, notes, cells_list, unsolved_table, solved_table, saved_game_time


def run():
    hints, notes, cells_list, unsolved_table, solved_table, saved_game_time = import_files()
    loaded_game = LoadedGame(hints, notes, cells_list, unsolved_table, solved_table, saved_game_time )
    loaded_game.handle_events()

