from genericpath import exists
import math
from . import database
import sqlite3
from .helpers import add_dictionary_entries, multiply_dictionary_entries, upgrade_dictionary
import pandas

DEFAULT_CHARACTER_BANNER_SOFT_PITY = {73: .06, 74: .12, 75: .18, 76: .24, 77: .3, 78: .35,
                                          79: .4, 80: .45, 81: .5, 82: .55, 83: .6, 84: .65, 85: .65, 86: .5, 87: .5, 88: .25, 89: 0.5, 90: 1}

DEFAULT_WEAPON_BANNER_SOFT_PITY = {62: 0.08, 63: 0.15, 64: 0.22, 65: 0.28, 66: 0.36, 67: 0.42, 68: 0.5,
                                       69: 0.56, 70: 0.6, 71: 0.67, 72: 0.71, 73: 0.75, 74: 0.80, 75: 0.83, 76: 0.84, 77: 0.80, 78: 0.5, 79: .5, 80: 1}

BASE_CHARACTER_FIVE_STAR_RATE = 0.006
BASE_WEAPON_FIVE_STAR_RATE = 0
BASE_MAXIMUM_FATE_POINTS = 2

class AnalyticalCharacter:

    def update_analytical_db(self) -> int:
        # converting to sets now
        analytical_sets = []
        for key in self.hashtable.keys():
            # convert to tuple in a way for proper storage
            current_list = tuple([key]+[self.hashtable[key][i]
                                 for i in self.hashtable[key].keys()])
            analytical_sets.append(current_list)

        with sqlite3.connect(self.db_file) as conn:
            database.update_data_in_table(
                analytical_sets, self.tablename, conn)
        return 0

    def load_hashtable(self) -> None:
        # stored in db is prioritized over files
        if database.check_db(self.db_file):
            conn = database.get_db_connection(self.db_file)
            data = database.table_data_to_hashtable(
                self.tablename, conn)
            self.hashtable.update(data)

    def lookup_num_generator(self, num_wishes: int, pity: int, guaranteed: bool) -> int:
        # malformed cases
        if num_wishes < 0 or num_wishes > self.max_wishes_required:
            return -1
        elif pity > self.hard_pity or pity < 0:
            return -1
        elif not (guaranteed == True or guaranteed == False):
            return -1
        # just a good way to ensure there is no collision and to have an invertible function
        # mod 1261 gives num_wishes, mod 1261*91 gives pity, mod 1261*91*2 gives guaranteed at least for character banner
        lookup_num = num_wishes+(self.max_wishes_required+1) * \
            pity+(self.hard_pity+1)*(self.max_wishes_required+1)*guaranteed
        return lookup_num

    def lookup_num_to_setting(self, lookup_num: int) -> list[int, int, bool]:
        # exact inverse of lookup_num_generator
        num_wishes = lookup_num % (self.max_wishes_required+1)
        lookup_num = math.floor(lookup_num/(self.max_wishes_required+1))
        pity = lookup_num % (self.hard_pity+1)
        lookup_num = math.floor(lookup_num/(self.hard_pity+1))
        guaranteed = lookup_num % 2
        if guaranteed == 0:
            guaranteed = False
        else:
            guaranteed = True
        return [num_wishes, pity, guaranteed]

    def __init__(self, soft_pity_dist: dict[int, float] = {}, base_five_star_rate=-1, copies_max=7, db_file="") -> None:
        self.tablename = "analytical_solutions_character"

        if base_five_star_rate == -1:
            base_five_star_rate = BASE_CHARACTER_FIVE_STAR_RATE

        if db_file == "":
            self.db_file = database.get_default_db()

        # soft_pity_dist - dictionary (empty for default option)
        if soft_pity_dist == {}:
            # technically pity starts at 74 but this a more accurate way of estimation for some reason
            # still looking into why
            self.soft_pity_dist = DEFAULT_CHARACTER_BANNER_SOFT_PITY
        else:
            self.soft_pity_dist = soft_pity_dist

        self.soft_pity_beginning = min(self.soft_pity_dist.keys())
        self.hard_pity = max(self.soft_pity_dist.keys())
        self.soft_pity_dist.update(
            {i: base_five_star_rate for i in range(0, max(self.soft_pity_beginning, 0))})
        self.soft_pity_dist[self.hard_pity] = 1

        self.max_wishes_required = (copies_max)*self.hard_pity*2
        self.max_lookup = self.max_wishes_required*(self.hard_pity+1)*2
        # "hard pity" in this case only gives a guaranteed 5 star not guaranteed rateup
        # note that this is different from constellations for characters there is max c6 but 7 copies to get there
        self.copies_max = copies_max
        self.hashtable = {}

        db_file = database.get_default_db()
        if exists(db_file):
            self.load_hashtable()
        else:
            conn = sqlite3.connect(db_file)
            with conn:
                database.init_db(conn)
        self.calculate_and_write_all_solutions()

    def store_if_solution_doesnt_exist(self, num_wishes: int, pity: int, guaranteed: bool, solution: dict) -> None:
        lookup_num = self.lookup_num_generator(num_wishes, pity, guaranteed)
        if lookup_num not in self.hashtable:
            self.hashtable.update({lookup_num: solution})

    def solution_from_database(self, lookup: int):
        conn = sqlite3.connect(self.db_file)
        vals_solution = database.get_entry_by_primary_key_analytical(self.tablename, conn,lookup)
        vals_solution = list(vals_solution)
        keys_solution = [i for i in range(0,len(vals_solution))]
        dict_solution = {keys_solution[i]:vals_solution[i] for i in range(0,len(vals_solution)) }
        return dict_solution

    def specific_solution(self, num_wishes: int, pity: int, guaranteed: bool, current_copies: int) -> dict[int, float]:
        lookup = self.lookup_num_generator(num_wishes, pity, guaranteed)
        if self.database_is_full():
            return self.solution_from_database(lookup)
        elif lookup != -1 and lookup in self.hashtable:
            temp = self.hashtable[lookup]
            result = {i: temp[i] for i in range(0, self.copies_max+1)}
            return result

        if num_wishes == 0:
            result = {i: 0 for i in range(0, self.copies_max+1)}
            result[0] = 1
            self.store_if_solution_doesnt_exist(
                num_wishes, pity, guaranteed, result)
            return result
        # I don't know that its necessary for this base case but sometimes it seemed to glitch out and this is 1000% correct
        elif num_wishes == self.max_wishes_required:
            result = {i: 0 for i in range(0, self.copies_max+1)}
            result[self.copies_max] = 1
            self.store_if_solution_doesnt_exist(
                num_wishes, pity, guaranteed, result)
            return result
        elif current_copies >= self.copies_max:
            return {i: 0 for i in range(0, self.copies_max+1)}

        pity_val = self.soft_pity_dist[pity]
        # basic scheme is that we always have some no_five_star which isn't upgraded (i.e. no increase to higher num of copies)
        # but is multiplied by the inverse of the upgraded (getting a 5 star) portion so that when added with an upgraded portion the sum is 1
        # this process seems to logically describe what we would expect and also matches fairly well with the statistical data that I have created
        if pity < self.hard_pity:
            temp = self.specific_solution(
                num_wishes-1, pity+1, guaranteed, current_copies)
            no_five_star = multiply_dictionary_entries(temp, 1-pity_val)
        else:
            no_five_star = {i: 0 for i in range(0, self.copies_max+1)}
        if guaranteed == True:
            five_star = multiply_dictionary_entries(upgrade_dictionary(
                self.specific_solution(num_wishes-1, 0, False, current_copies+1)), pity_val)
            result = add_dictionary_entries([no_five_star, five_star])
        elif guaranteed == False:
            five_star_win = multiply_dictionary_entries(upgrade_dictionary(self.specific_solution(
                num_wishes-1, 0, False, current_copies+1)), pity_val*0.5)
            five_star_lose = multiply_dictionary_entries(self.specific_solution(
                num_wishes-1, 0, True, current_copies), pity_val*0.5)
            result = add_dictionary_entries(
                [no_five_star, five_star_win, five_star_lose])

        self.store_if_solution_doesnt_exist(
            num_wishes, pity, guaranteed, result)
        # TODO add an extra dictionary for after max constellations/refinements so that we can track for after
        # it will be a probability dictionary that counts up the extra wishes as the percent of time you have that many additional wishes remaining
        # should be possible and also work. Need to alter the helper function for this though
        return result
    
    def calculate_and_write_all_solutions(self) -> None:
        if len(self.hashtable) >= self.max_lookup:
            return
        incomplete_lookups = {i for i in range(0, self.max_lookup)}
        for val in self.hashtable:
            incomplete_lookups.discard(val)

        while len(incomplete_lookups) > 0:
            random_lookup = incomplete_lookups.pop()
            settings = self.lookup_num_to_setting(random_lookup)
            self.specific_solution(
                settings[0], settings[1], settings[2], 0)

        self.update_analytical_db()

    def probability_on_copies_to_num_wishes(self, probability_desired, copies_desired, pity=0, guaranteed=False):
        # takes as input the probability desired for however many copies desired (or more copies). optionally can do for a specific pity or guaranteed
        # returns the number or wishes required to achieve that probability for the number of copies (or more copies) with pity and guaranteed
        # in some ways an inverse function for specific solution by swapping num wishes with probabilities
        for i in range(0, self.max_wishes_required):
            current_probability = 0
            current_solution = self.specific_solution(i, pity, guaranteed, 0)
            for j in range(copies_desired, self.copies_max+1):
                current_probability += current_solution[j]
            if current_probability >= probability_desired:
                return i
        # we should never get here but just in case
        return self.max_wishes_required

    def database_is_full(self):
        conn = sqlite3.connect(self.db_file)
        count = database.count_entries_in_table(self.tablename, conn)
        # we just care that its mostly full since its more efficient to estimate if its full then fill in on the off chance it isnt
        if count >= self.max_lookup*.99:
            return True
        else:
            return False


class AnalyticalWeapon:
    def update_analytical_db(self) -> int:
        # converting to sets now
        analytical_sets = []
        for key in self.hashtable.keys():
            # convert to tuple in a way for proper storage
            current_list = tuple([key]+[self.hashtable[key][i]
                                 for i in self.hashtable[key].keys()])
            analytical_sets.append(current_list)

        with sqlite3.connect(self.db_file) as conn:
            database.update_data_in_table(
                analytical_sets, self.tablename, conn)
        return 0

    def load_hashtable(self) -> None:
        # stored in db is prioritized over files
        if database.check_db(self.db_file):
            conn = database.get_db_connection(self.db_file)
            data = database.table_data_to_hashtable(
                self.tablename, conn)
            self.hashtable.update(data)

    def lookup_num_generator(self, num_wishes: int, pity: int, guaranteed: bool, fate_points: int) -> int:
        # malformed cases
        if num_wishes < 0 or num_wishes > self.max_wishes_required:
            return -1
        elif pity > self.hard_pity or pity < 0:
            return -1
        elif not (guaranteed == True or guaranteed == False):
            return -1
        elif fate_points < 0 or fate_points > self.fate_points_required:
            return -1
            # just a good way to ensure there is no collision and to have an invertible function
            # mod 1261 gives num_wishes, mod 1261*91 gives pity, mod 1261*91*2 gives guaranteed at least for character banner
        lookup_num = num_wishes+(self.max_wishes_required+1) * \
            pity+(self.hard_pity+1)*(self.max_wishes_required+1)*guaranteed + \
            (self.hard_pity+1)*(self.max_wishes_required+1)*2*fate_points
        return lookup_num

    def lookup_num_to_setting(self, lookup_num: int) -> list[int, int, bool, int]:
        # exact inverse of lookup_num_generator
        num_wishes = lookup_num % (self.max_wishes_required+1)
        lookup_num = math.floor(lookup_num/(self.max_wishes_required+1))
        pity = lookup_num % (self.hard_pity+1)
        lookup_num = math.floor(lookup_num/(self.hard_pity+1))
        guaranteed = lookup_num % 2
        if guaranteed == 0:
            guaranteed = False
        else:
            guaranteed = True
        lookup_num = math.floor(lookup_num/2)
        fate_points = lookup_num % 3
        return [num_wishes, pity, guaranteed, fate_points]

    def __init__(self, soft_pity_dist: dict[int, float] = {}, base_five_star_rate=-1, fate_points_required=-1, copies_max=5, db_file="") -> None:
        self.tablename = "analytical_solutions_weapon"
        if base_five_star_rate == -1:
            base_five_star_rate = BASE_WEAPON_FIVE_STAR_RATE

        if db_file == "":
            self.db_file = database.get_default_db()

        if fate_points_required == -1:
            self.fate_points_required = BASE_MAXIMUM_FATE_POINTS

        # soft_pity_dist - dictionary (empty for default option)
        if soft_pity_dist == {}:
            # technically pity starts at 74 but this a more accurate way of estimation for some reason
            # still looking into why
            self.soft_pity_dist = DEFAULT_WEAPON_BANNER_SOFT_PITY
        else:
            self.soft_pity_dist = soft_pity_dist

        self.soft_pity_beginning = min(self.soft_pity_dist.keys())
        self.hard_pity = max(self.soft_pity_dist.keys())
        self.soft_pity_dist.update(
            {i: base_five_star_rate for i in range(0, max(self.soft_pity_beginning, 0))})
        self.soft_pity_dist[self.hard_pity] = 1

        self.copies_max = copies_max
        self.max_wishes_required = (copies_max)*self.hard_pity*3
        self.max_lookup = self.max_wishes_required*(self.hard_pity+1)*2
        # "hard pity" in this case only gives a guaranteed 5 star not guaranteed rateup
        # note that this is different from constellations for characters there is max c6 but 7 copies to get there
        self.hashtable = {}

        db_file = database.get_default_db()
        if exists(db_file):
            self.load_hashtable()
        else:
            conn = sqlite3.connect(db_file)
            with conn:
                database.init_db(conn)
        self.calculate_and_write_all_solutions()

    def store_if_solution_doesnt_exist(self, num_wishes: int, pity: int, guaranteed: bool, fate_points: int, solution: dict) -> None:
        lookup_num = self.lookup_num_generator(
            num_wishes, pity, guaranteed, fate_points)
        if lookup_num not in self.hashtable:
            self.hashtable.update({lookup_num: solution})

    def solution_from_database(self, lookup: int):
        conn = sqlite3.connect(self.db_file)
        vals_solution = database.get_entry_by_primary_key_analytical(self.tablename, conn,lookup)
        vals_solution = list(vals_solution)
        keys_solution = [i for i in range(0,len(vals_solution))]
        dict_solution = {keys_solution[i]:vals_solution[i] for i in range(0,len(vals_solution)) }
        return dict_solution

    def specific_solution(self, num_wishes: int, pity: int, guaranteed: bool, fate_points: int, current_copies: int) -> dict[int, float]:
        lookup = self.lookup_num_generator(
            num_wishes, pity, guaranteed, fate_points)
        if self.database_is_full():
            return self.solution_from_database(lookup)
        elif lookup != -1 and lookup in self.hashtable:
            temp = self.hashtable[lookup]
            result = {i: temp[i] for i in range(0, self.copies_max+1)}
            return result

        if num_wishes == 0:
            result = {i: 0 for i in range(0, self.copies_max+1)}
            result[0] = 1
            self.store_if_solution_doesnt_exist(
                num_wishes, pity, guaranteed, fate_points, result)
            return result
        # I don't know that its necessary for this base case but sometimes it seemed to glitch out and this is 1000% correct
        elif num_wishes == self.max_wishes_required:
            result = {i: 0 for i in range(0, self.copies_max+1)}
            result[self.copies_max] = 1
            self.store_if_solution_doesnt_exist(
                num_wishes, pity, guaranteed, fate_points, result)
            return result
        elif current_copies >= self.copies_max:
            return {i: 0 for i in range(0, self.copies_max+1)}

        pity_val = self.soft_pity_dist[pity]
        # basic scheme is that we always have some no_five_star which isn't upgraded (i.e. no increase to higher num of copies)
        # but is multiplied by the inverse of the upgraded (getting a 5 star) portion so that when added with an upgraded portion the sum is 1
        # this process seems to logically describe what we would expect and also matches fairly well with the statistical data that I have created
        if pity < self.hard_pity:
            temp = self.specific_solution(
                num_wishes-1, pity+1, guaranteed, fate_points, current_copies)
            no_five_star = multiply_dictionary_entries(temp, 1-pity_val)
        else:
            no_five_star = {i: 0 for i in range(0, self.copies_max+1)}
        if fate_points == 2:
            five_star_desired = multiply_dictionary_entries(upgrade_dictionary(
                self.specific_solution(num_wishes-1, 0, False, 0, current_copies+1)), pity_val)
            result = add_dictionary_entries([no_five_star, five_star_desired])
        elif guaranteed == True:
            five_star_desired = multiply_dictionary_entries(upgrade_dictionary(self.specific_solution(
                num_wishes-1, 0, False, 0, current_copies+1)), pity_val*0.5)
            five_star_other_rateup = multiply_dictionary_entries(self.specific_solution(
                num_wishes-1, 0, False, fate_points+1, current_copies), pity_val*0.5)
            result = add_dictionary_entries(
                [no_five_star, five_star_desired, five_star_other_rateup])
        elif guaranteed == False:
            five_star_desired = multiply_dictionary_entries(upgrade_dictionary(self.specific_solution(
                num_wishes-1, 0, False, 0, current_copies+1)), pity_val*0.375)
            five_star_other_rateup = multiply_dictionary_entries(self.specific_solution(
                num_wishes-1, 0, False, fate_points+1, current_copies), pity_val*0.375)
            five_star_non_rateup = multiply_dictionary_entries(self.specific_solution(
                num_wishes-1, 0, True, fate_points+1, current_copies), pity_val*0.25)
            result = add_dictionary_entries(
                [no_five_star, five_star_desired, five_star_other_rateup, five_star_non_rateup])

        self.store_if_solution_doesnt_exist(
            num_wishes, pity, guaranteed, fate_points, result)

        return result

    def calculate_and_write_all_solutions(self) -> None:
        incomplete_lookups = {i for i in range(0, self.max_lookup)}
        for val in self.hashtable:
            incomplete_lookups.discard(val)

        if len(self.hashtable) <= self.max_lookup:
            while len(incomplete_lookups) > 0:
                random_lookup = incomplete_lookups.pop()
                settings = self.lookup_num_to_setting(random_lookup)
                self.specific_solution(
                    settings[0], settings[1], settings[2], settings[3], 0)

            self.update_analytical_db()

    def probability_on_copies_to_num_wishes(self, probability_desired, copies_desired, pity=0, guaranteed=False, fate_points=0):
        # takes as input the probability desired for however many copies desired (or more copies). optionally can do for a specific pity or guaranteed
        # returns the number or wishes required to achieve that probability for the number of copies (or more copies) with pity and guaranteed
        # in some ways an inverse function for specific solution by swapping num wishes with probabilities
        for i in range(0, self.max_wishes_required):
            current_probability = 0
            current_solution = self.specific_solution(
                i, pity, guaranteed, 0, fate_points)
            for j in range(copies_desired, self.copies_max+1):
                current_probability += current_solution[j]
            if current_probability >= probability_desired:
                return i
        # we should never get here but just in case
        return self.max_wishes_required

    def database_is_full(self):
        conn = sqlite3.connect(self.db_file)
        count = database.count_entries_in_table(self.tablename, conn)
        # we just care that its mostly full since its more efficient to estimate if its full then fill in on the off chance it isnt
        if count >= self.max_lookup*.99:
            return True
        else:
            return False


import base64
from .models import *
from io import BytesIO
from matplotlib import pyplot
def bar_graph_for_statistics(solution, banner_type,statistics_type, numwishes, pity, guaranteed,fate_points) ->str:
    if statistics_type == "calcprobability":
        return bar_graph_for_calcprobability(solution,banner_type,numwishes, pity, guaranteed,fate_points)
    elif statistics_type == "calcnumwishes":
        return ""
    return ""

def bar_graph_for_calcprobability(solution, banner_type, numwishes, pity, guaranteed, fate_points) -> str:
    values = [float(solution[key]) for key in solution.keys()]
    pyplot.switch_backend('AGG')
    fig, ax = pyplot.subplots(figsize=(10, 6))
    guaranteed_text = "with" if guaranteed else "without"
    if banner_type == "character":
        x_labels = ["X"]
        for i in range(0,7):
            x_labels.append("C"+str(i))
        fig.suptitle('Wish Probability Breakdown for: {} Wishes, {} Pity, {} Guaranteed'.format(numwishes, pity, guaranteed_text))
        fig.supylabel('Portion Resuling in Specified Constellation')
    elif banner_type == "weapon":
        x_labels = ["X"]
        for i in range(1,6):
            x_labels.append("R"+str(i))
        fig.suptitle('Wish Probability Breakdown for: {} Wishes, {} Pity, {} Guaranteed, {} Fate Points'.format(numwishes, pity, guaranteed_text, fate_points))
        fig.supylabel('Portion Resuling in Specified Refinement')

    bars= pyplot.bar(x_labels , values)
    ax.bar_label(bars)
    min_ylim = -0.1
    max_ylim = 1.1
    pyplot.ylim(min_ylim,max_ylim)
    pyplot.tight_layout()

    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph