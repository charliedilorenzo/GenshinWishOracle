from genericpath import exists
import math
import sqlite3
import matplotlib.ticker as mtick

from . import helpers as H
from . import database

# DEFAULT_CHARACTER_BANNER_SOFT_PITY = {73: 0.32, 74: 0.32, 75: 0.32, 76: 0.32, 77: 0.32, 78: 0.32, 79: 0.32, 
# 80: 0.32, 81: 0.32, 82: 0.32, 83: 0.32, 84: 0.32, 85: 0.32, 86: 0.32, 87: 0.32, 88: 0.32, 89: 1}
# DEFAULT_WEAPON_BANNER_SOFT_PITY = {62: 0.08, 63: 0.15, 64: 0.22, 65: 0.28, 66: 0.36, 67: 0.42, 68: 0.5,
#                                        69: 0.56, 70: 0.6, 71: 0.67, 72: 0.71, 73: 0.75, 74: 0.80, 75: 0.83, 76: 0.84, 77: 0.80, 78: 0.5, 79:1}

DEFAULT_CHARACTER_BANNER_SOFT_PITY = {73: .06, 74: .12, 75: .18, 76: .24, 77: .3, 78: .35,
                                          79: .4, 80: .45, 81: .5, 82: .55, 83: .6, 84: .65, 85: .65, 86: .5, 87: .5, 88: .25, 89: 1}

DEFAULT_WEAPON_BANNER_SOFT_PITY = {62: 0.08, 63: 0.15, 64: 0.22, 65: 0.28, 66: 0.36, 67: 0.42, 68: 0.5,
                                       69: 0.56, 70: 0.6, 71: 0.67, 72: 0.71, 73: 0.75, 74: 0.80, 75: 0.83, 76: 0.84, 77: 0.80, 78: 0.5, 79:1}

BANNER_TYPE_TO_PITY = {"character": DEFAULT_CHARACTER_BANNER_SOFT_PITY, "weapon": DEFAULT_WEAPON_BANNER_SOFT_PITY}

BASE_CHARACTER_FIVE_STAR_RATE = 0.006
BASE_WEAPON_FIVE_STAR_RATE = 0.006
BANNER_TYPE_TO_BASE_RATE = {"character": BASE_CHARACTER_FIVE_STAR_RATE, "weapon": BASE_WEAPON_FIVE_STAR_RATE}

BASE_MAXIMUM_FATE_POINTS = 2

EPSILON = 0.00000001
class DataPoint():
    def __init__(self, label, value) -> None:
        self.label = label
        self.value = value
    
    def __eq__(self, __value: object) -> bool:
        if self.label != __value.label:
            return False
        elif self.value != __value.value:
            return False
        return True
class Statistic:
    def __init__(self, values: list[float],banner_type: str,formatted = False):
        self.place_values = 4
        self.values = values
        self.banner_type = banner_type
        if self.banner_type == "character":
            self.labels = ["X"]+["C{}".format(i) for i in range(0,7)]
            self.datapoints = [DataPoint(self.labels[i], self.values[i]) for i in range(0,8)]
        elif self.banner_type == "weapon":
            self.labels = ["X"]+["R{}".format(i) for i in range(1,6)]
            self.datapoints = [DataPoint(self.labels[i], self.values[i]) for i in range(0,6)]
        if formatted:
            self.values = ["%.{}f".format(self.place_values) % item for item in self.values]
        self.banner_type = banner_type.capitalize()
    
    def get_formated_dictionary(self) -> dict:
        # formatted_dictionary = [("%.{}f".format(self.place_values) % float(val)) for val in self.values]

        formatted_dictionary = {}
        for i in range(0, len(self.values)):
            formatted_dictionary[self.labels[i]] = ("%.{}f".format(self.place_values) % float(self.values[i]))
        return formatted_dictionary

    def get_data_points(self) -> list[DataPoint]:
        return self.datapoints

class AnalyzeGeneric:
    def update_analytical_db(self) -> int:
        # converting to sets now
        analytical_sets = []
        for key in self.hashtable.keys():
            # convert to tuple in a way for proper storage
            current_list = tuple([key]+self.hashtable[key])
            analytical_sets.append(current_list)

        with sqlite3.connect(self.db_file) as conn:
            database.update_data_in_table(
                analytical_sets, self.tablename, conn)
            
        with sqlite3.connect(self.db_file) as conn:
            self.database_size = database.count_entries_in_table(self.tablename, conn)
        return 0

    def load_hashtable(self) -> None:
        if database.check_db(self.db_file):
            with sqlite3.connect(self.db_file) as conn:
                if not database.check_table(self.tablename,conn):
                    database.create_data_tables(conn)
                data = database.table_data_to_hashtable(
                    self.tablename, conn)
                self.hashtable.update(data)
            with sqlite3.connect(self.db_file) as conn:
                self.database_size = database.count_entries_in_table(self.tablename, conn)

    def lookup_num_generator(self, num_wishes: int, pity: int, guaranteed: bool, fate_points: int) -> int:
        # malformed cases
        if num_wishes < 0 or num_wishes > self.max_wishes_required:
            return -1
        elif pity > self.hard_pity or pity < 0:
            return -1
        elif not (guaranteed == True or guaranteed == False):
            return -1
        elif fate_points < 0 or (fate_points > self.fate_points_required and self.banner_type == "weapon"):
            return -1
        # just a good way to ensure there is no collision and to have an invertible function
        # mod 1261 gives num_wishes, mod 1261*91 gives pity, mod 1261*91*2 gives guaranteed at least for character banner
        lookup_num = num_wishes + \
            (self.max_wishes_required+1) * pity + \
            (self.hard_pity+1)*(self.max_wishes_required+1)*guaranteed + \
            (self.hard_pity+1)*(self.max_wishes_required+1)*2*fate_points
        if lookup_num > self.max_lookup:
            raise Exception(f"Lookup number {lookup_num} is larger than max_lookup: {self.max_lookup}. In {self.banner_type} banner")
        return lookup_num

    def lookup_num_to_setting(self, lookup_num: int) -> list[int, int, bool, int]:
        # exact inverse of lookup_num_generator
        if lookup_num > self.max_lookup:
            raise Exception(f"Lookup number {lookup_num} is larger than max_lookup: {self.max_lookup}. In {self.banner_type} banner")
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
    
    def __init__(self, soft_pity_dist: dict[int, float], base_five_star_rate, fate_points_required, copies_max, banner_type) -> None:
        self.tablename = f'analytical_solutions_{self.banner_type}'
        self.banner_type = banner_type
        base_five_star_rate = base_five_star_rate
        self.fate_points_required = fate_points_required
        self.soft_pity_dist = soft_pity_dist
        self.copies_max = copies_max

        self.soft_pity_beginning = min(self.soft_pity_dist.keys())
        self.hard_pity = max(self.soft_pity_dist.keys())
        self.soft_pity_dist.update(
            {i: base_five_star_rate for i in range(0, max(self.soft_pity_beginning, 0))})
        self.soft_pity_dist[self.hard_pity] = 1

        # "hard pity" in this case only gives a guaranteed 5 star not guaranteed rateup
        # note that this is different from constellations for characters there is max c6 but 7 copies to get there
        self.hashtable = {}
        self.database_size = 0

    def store_if_solution_doesnt_exist(self, lookup_num: int, solution: list[float]) -> None:
        if lookup_num not in self.hashtable:
            self.hashtable.update({lookup_num: solution})

    def solution_from_database(self, lookup: int):
        with sqlite3.connect(self.db_file) as conn:
            vals_solution = database.get_entry_by_primary_key_analytical(self.tablename, conn,lookup)
            vals_solution = list(vals_solution)
            return vals_solution

    def specific_solution(self, num_wishes: int, pity: int, guaranteed: bool, fate_points: int, current_copies: int) -> dict[int, float]:
        pass

    def calculate_and_write_all_solutions(self) -> None:
        if not exists(self.db_file):
            database.init_db(self.db_file)
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

    def probability_on_copies_to_num_wishes(self, probability_desired, copies_desired, pity=0, guaranteed=False, fate_points=0,graph=False):
        # TODO ADD GRAPHS
        # takes as input the probability desired for however many copies desired (or more copies). optionally can do for a specific pity or guaranteed
        # returns the number or wishes required to achieve that probability for the number of copies (or more copies) with pity and guaranteed
        # in some ways an inverse function for specific solution by swapping num wishes with probabilities
        # all_lookups = [self.lookup_num_generator(i,pity,guaranteed,fate_points) for i in range(0, self.max_wishes_required):]
        lookups = self.get_all_lookups_vary_on_num_wishes(pity, guaranteed,fate_points)
        for i in range(0, len(lookups)):
            current_probability = 0
            current_solution = lookups[i][1:]
            print(lookups[i][0], current_solution)
            for j in range(copies_desired, self.copies_max+1):
                current_probability += current_solution[j]
            if H.within_epsilon_or_greater(current_probability, probability_desired, EPSILON):
                return i
        # we should never get here but just in case
        return self.max_wishes_required

    def database_is_full(self):
        # DO NOT ADD IN A QUERY TO DB HERE IT WILL SLOW EVERYTHING DOWN AND MAKE IT TERRIBLE
        count = self.database_size
        # we just care that its mostly full since its more efficient to estimate if its full then fill in on the off chance it isnt
        if count >= self.max_lookup*.99:
            return True
        else:
            return False
    
    def refresh_database_size(self):
        if exists(self.db_file):
            with sqlite3.connect(self.db_file) as conn:
                if database.check_table(self.tablename,conn):
                    self.database_size = database.count_entries_in_table(self.tablename, conn)
                else:
                    self.database_size = 0
        else:
            self.database_size = 0
        
    def get_statistic(self, num_wishes: int, pity: int, guaranteed: bool, fate_points: int, current_copies: int, formatted = True):
        solution = self.specific_solution(num_wishes, pity, guaranteed, fate_points, current_copies)
        return Statistic(solution,self.banner_type, formatted)
    
    def get_all_lookups_vary_on_num_wishes(self, pity: int, guaranteed: bool, fate_points: int) -> list:
        # given any combo of pity/guaranteed/fate_points, it will return all the lookups of wish nums 0 through max wish number
        # returns a hash table
        
        lookups_low = self.lookup_num_generator(0,pity,guaranteed,fate_points)
        lookups_high = self.lookup_num_generator(self.max_wishes_required,pity,guaranteed,fate_points)
        print(lookups_low,lookups_high)
        print(self.lookup_num_to_setting(lookups_low))
        # because of how lookups work we can get away with using the low and the high only and then searching in between
        with sqlite3.connect(self.db_file) as conn:
            returned = database.get_all_lookups(self.tablename,conn,lookups_low, lookups_high)
        return returned
    

class AnalyzeCharacter(AnalyzeGeneric):
    def __init__(self,db_file="") -> None:
        self.banner_type = "character"
        banner_type = self.banner_type

        if db_file == "":
            self.db_file = database.get_default_db()
            db_file = database.get_default_db()
        else:
            self.db_file = db_file

        super().__init__(BANNER_TYPE_TO_PITY[banner_type],BANNER_TYPE_TO_BASE_RATE[banner_type],-1,7,banner_type)
        self.max_wishes_required = (self.copies_max)*(self.hard_pity+1)*2
        self.max_lookup = (self.max_wishes_required+1)*(self.hard_pity+1)*2

        self.refresh_database_size()
        if exists(db_file) and self.database_is_full():
            self.load_hashtable()
        elif exists(db_file):
            self.load_hashtable()
            self.calculate_and_write_all_solutions()
        else:
            database.init_db(db_file)
            self.calculate_and_write_all_solutions()
    

    def specific_solution(self, num_wishes: int, pity: int, guaranteed: bool, fate_points: int, current_copies: int) -> list[float]:
        lookup = self.lookup_num_generator(num_wishes, pity, guaranteed,fate_points)
        all_empty_list = [float(0) for i in range(0, self.copies_max+1)]
        if lookup != -1 and lookup in self.hashtable:
            temp = self.hashtable[lookup]
            return temp
        # elif self.database_is_full():
        #     return self.solution_from_database(lookup)

        if num_wishes == 0:
            result = all_empty_list
            result[0] = float(1)
            self.store_if_solution_doesnt_exist(
                lookup, result)
            return result

        pity_val = self.soft_pity_dist[pity]
        # basic scheme is that we always have some no_five_star which isn't upgraded (i.e. no increase to higher num of copies)
        # but is multiplied by the inverse of the upgraded (getting a 5 star) portion so that when added with an upgraded portion the sum is 1
        # this process seems to logically describe what we would expect and also matches fairly well with the statistical data that I have created
        no_five_star = all_empty_list
        if pity < self.hard_pity:
            no_five_star = H.scalar_list(self.specific_solution(
                num_wishes-1, pity+1, guaranteed, 0,  current_copies), 1-pity_val)
        five_star_win = all_empty_list
        five_star_lose= all_empty_list
        if guaranteed == True:
            five_star_win = H.scalar_list(H.upgrade_list(
                self.specific_solution(num_wishes-1, 0, False, 0, current_copies+1)), pity_val)
        elif guaranteed == False:
            five_star_win = H.scalar_list(H.upgrade_list(self.specific_solution(
                num_wishes-1, 0, False, 0, current_copies+1)), pity_val*0.5)
            five_star_lose = H.scalar_list(self.specific_solution(
                num_wishes-1, 0, True, 0, current_copies), pity_val*0.5)
    
        result = H.add_list_entries(
            [no_five_star, five_star_win, five_star_lose])

        self.store_if_solution_doesnt_exist(lookup, result)
        # TODO add an extra dictionary for after max constellations/refinements so that we can track for after
        # it will be a probability dictionary that counts up the extra wishes as the percent of time you have that many additional wishes remaining
        # should be possible and also work. Need to alter the helper function for this though
        return result

class AnalyzeWeapon(AnalyzeGeneric):
    def __init__(self,db_file="") -> None:
        self.banner_type = "weapon"
        banner_type = self.banner_type
        self.tablename = f'analytical_solutions_{self.banner_type}'

        if db_file == "":
            self.db_file = database.get_default_db()
            db_file = database.get_default_db()
        else:
            self.db_file = db_file

        super().__init__(BANNER_TYPE_TO_PITY[banner_type],BANNER_TYPE_TO_BASE_RATE[banner_type],2,5,banner_type)

        # # different for weapon since its limited by fate points but guaranteed is still a different flag
        # max lookup will be larger than max wishes required because of this
        self.max_wishes_required = (self.copies_max)*(self.hard_pity+1)*(self.fate_points_required+1)
        self.max_lookup = (self.max_wishes_required+1)*(self.hard_pity+1)*(self.fate_points_required+1)*2


        # max_wishes_required = (copies_max)*(hard_pity+1)*(fate_points_required+1)
        # max_lookup = max_wishes_required*(hard_pity+1)*(fate_points_required+1)*2

        self.refresh_database_size()
        if exists(db_file) and self.database_is_full():
            self.load_hashtable()
        elif exists(db_file):
            self.load_hashtable()
            self.calculate_and_write_all_solutions()
        else:
            database.init_db(db_file)
            self.calculate_and_write_all_solutions()

    def specific_solution(self, num_wishes: int, pity: int, guaranteed: bool, fate_points: int, current_copies: int) -> list[float]:
        lookup = self.lookup_num_generator(
            num_wishes, pity, guaranteed, fate_points)
        all_empty_list = [float(0) for i in range(0, self.copies_max+1)]
        if lookup != -1 and lookup in self.hashtable:
            temp = self.hashtable[lookup]
            return temp
        # elif self.database_is_full():
        #     return self.solution_from_database(lookup)

        if num_wishes == 0:
            result = all_empty_list
            result[0] = float(1)
            self.store_if_solution_doesnt_exist(lookup, result)
            return result
        # I don't know that its necessary for this base case but sometimes it seemed to glitch out and this is 1000% correct
        elif num_wishes == self.max_wishes_required:
            result = all_empty_list
            result[self.copies_max-1] = 1
            self.store_if_solution_doesnt_exist(lookup, result)
            return result
        elif current_copies >= self.copies_max:
            return all_empty_list

        pity_val = self.soft_pity_dist[pity]
        no_five_star = all_empty_list
        # basic scheme is that we always have some no_five_star which isn't upgraded (i.e. no increase to higher num of copies)
        # but is multiplied by the inverse of the upgraded (getting a 5 star) portion so that when added with an upgraded portion the sum is 1
        # this process seems to logically describe what we would expect and also matches fairly well with the statistical data that I have created
        if pity < self.hard_pity:
            temp = self.specific_solution(
                num_wishes-1, pity+1, guaranteed, fate_points, current_copies)
            no_five_star = H.scalar_list(temp, 1-pity_val)
        
        five_star_desired = all_empty_list
        five_star_other_rateup = all_empty_list
        five_star_non_rateup = all_empty_list

        if fate_points == 2:
            five_star_desired = H.scalar_list(H.upgrade_list(
                self.specific_solution(num_wishes-1, 0, False, 0, current_copies+1)), pity_val)
        elif guaranteed == True:
            five_star_desired = H.scalar_list(H.upgrade_list(self.specific_solution(
                num_wishes-1, 0, False, 0, current_copies+1)), pity_val*0.5)
            five_star_other_rateup = H.scalar_list(self.specific_solution(
                num_wishes-1, 0, False, fate_points+1, current_copies), pity_val*0.5)
        elif guaranteed == False:
            five_star_desired = H.scalar_list(H.upgrade_list(self.specific_solution(
                num_wishes-1, 0, False, 0, current_copies+1)), pity_val*0.375)
            five_star_other_rateup = H.scalar_list(self.specific_solution(
                num_wishes-1, 0, False, fate_points+1, current_copies), pity_val*0.375)
            five_star_non_rateup = H.scalar_list(self.specific_solution(
                num_wishes-1, 0, True, fate_points+1, current_copies), pity_val*0.25)
        result = H.add_list_entries([no_five_star, five_star_desired, five_star_other_rateup, five_star_non_rateup])

        self.store_if_solution_doesnt_exist(lookup, result)

        return result


import base64
from .models import *
from io import BytesIO
from matplotlib import pyplot
def bar_graph_for_statistics(solution, **kwargs) ->str:
    statistics_type = kwargs.pop('statistics_type', None)
    banner_type = kwargs.pop('banner_type', "character").lower()
    if statistics_type == "calcprobability":
        numwishes = kwargs.pop('numwishes', None)
        pity = kwargs.pop('pity', None)
        guaranteed = kwargs.pop('guaranteed', None)
        fate_points = kwargs.pop('fate_points', None)
        return bar_graph_for_calcprobability(solution,banner_type, numwishes, pity, guaranteed, fate_points)
    elif statistics_type == "calcnumwishes":
        pity = kwargs.pop('pity', None)
        guaranteed = kwargs.pop('guaranteed', None)
        fate_points = kwargs.pop('fate_points', None)
        minimum_probability = kwargs.pop('minimum_probability', None)
        copies_requried = kwargs.pop('numcopies' , None)
        return bar_graph_calc_numwishes(solution, minimum_probability, copies_requried, pity, guaranteed, fate_points)
    return ""

def bar_graph_for_calcprobability(solution: Statistic, banner_type, numwishes, pity, guaranteed, fate_points) -> str:
    values = solution.get_formated_dictionary()
    values = [float(values[key]) for key in values.keys()]
    pyplot.switch_backend('AGG')
    fig, ax = pyplot.subplots(figsize=(10, 6))
    guaranteed_text = "with" if guaranteed else "without"
    x_labels = solution.labels
    if banner_type == "character":
        x_labels = solution.labels
        fig.suptitle('Wish Probability Breakdown for: {} Wishes, {} Pity, {} Guaranteed'.format(numwishes, pity, guaranteed_text))
        fig.supylabel('Percentage Resulting in Specified Constellation')
    elif banner_type == "weapon":
        fig.suptitle('Wish Probability Breakdown for: {} Wishes, {} Pity, {} Guaranteed, {} Fate Points'.format(numwishes, pity, guaranteed_text, fate_points))
        fig.supylabel('Portion Resuling in Specified Refinement')

    # fmt = '%.0f%%'
    # values = [value*10000 for value in values]
    yticks = mtick.PercentFormatter(1.0)
    ax.yaxis.set_major_formatter(yticks)
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

def bar_graph_calc_numwishes(solution, minimum_probability, copies_requried, pity, guaranteed, fate_points):
    # TODO ADD THIS
    return ""