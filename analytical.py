from re import L
from functools import wraps
from genericpath import exists
import math


def add_dictionary_entries(list_of_dicts: list[dict[int, float]]) -> dict[int, float]:
    # assumes that the dictionary have the same keys
    new_dict = {key: 0 for key in list_of_dicts[0]}
    for dict in list_of_dicts:
        for key in list_of_dicts[0]:
            new_dict[key] += dict[key]
    return new_dict


def multiply_dictionary_entries(dictionary: dict[int, float], factor: float) -> dict[int, float]:
    # assumes that the dictionary have the same keys
    new_dict = {}
    for key in dictionary:
        new_dict[key] = factor*dictionary[key]
    return new_dict


def upgrade_dictionary(dictionary: dict[int, float]) -> dict[int, float]:
    # for a dictionary assumed to have keys that are ascending integers starting at 0
    # returns a new dictionary that the value for every key moved up to that key+1 except the final entry which is the previous key's value plus its current
    new_dict = {}
    temp1 = dictionary[0]
    for i in range(1, len(dictionary)-1):
        temp2 = dictionary[i]
        new_dict[i] = temp1
        temp1 = temp2
    new_dict[i+1] = temp1+dictionary[i+1]
    new_dict[0] = 0
    return new_dict


class AnalyticalRecursiveTest:
    def convert_to_breakdown_file(self, new_file_name, pity, guaranteed):
        with open(new_file_name, "w") as f:
            # descriptive preamble
            f.write("Trials = Analytical    SKIP\n")
            f.write("pity = {}, guaranteed = {}    SKIP\n".format(pity, guaranteed))
            breakdown_columns = ["Wishes Available", "X"]
            for i in range(0, self.copies_max):
                breakdown_columns.append("C"+str(i))

            f.write(",".join(breakdown_columns) + "    SKIP\n")
            for i in range(0, self.max_wishes_required):
                num_wishes = i
                solution = self.specific_solution(
                    num_wishes, pity, guaranteed, 0, periodic_interval=10000)
                solution = [str(solution[i]) for i in range(0, len(solution))]
                f.write(str(i) + "," + ",".join(solution) + "\n")

    def create_hashtable(self) -> None:
        base_cases = {}
        base_case = [str(0) for i in range(0, self.copies_max+1)]
        base_case[0] = str(1)
        for i in range(0, (self.hard_pity+1)):
            base_cases[self.lookup_num_generator(0, i, False)] = base_case
            base_cases[self.lookup_num_generator(0, i, True)] = base_case

        with open(self.filename, 'w') as f:
            write_string = str(0) + "," + ",".join(base_case) + "\n"
            f.write(write_string)
            for i in range(1, 229502):
                if i in base_cases:
                    # the breakdown will be listed after the key
                    write_string = str(i) + "," + ",".join(base_cases[i])
                    f.write(write_string)
                write_string = str(i) + ", -1\n"
                f.write(write_string)

    def load_hashtable(self) -> None:
        with open(self.filename, 'r') as f:
            for line in f:
                current_line = line.split(',')
                # unsolved situations are listed as "key, -1" so we can just check for 2 length to see if there is content for the line
                if len(current_line) == 2:
                    continue
                else:
                    key = int(current_line.pop(0))
                    breakdown = [float(current_line[i].strip()) for i in range(
                        0, len(current_line))]
                    self.hashtable[key] = breakdown

    def lookup_num_generator(self, num_wishes: int, pity: int, guaranteed: bool) -> int:
        # malformed cases
        if num_wishes < 0 or num_wishes > self.max_wishes_required:
            return -1
        elif pity > 90 or pity < 0:
            return -1
        elif not (guaranteed == True or guaranteed == False):
            return -1
        # just a good way to ensure there is no collision and to have an invertible function
        lookup_num = num_wishes+(self.max_wishes_required+1) * \
            pity+(self.hard_pity+1)*(self.max_wishes_required+1)*guaranteed
        return lookup_num

    def lookup_to_setting(self, lookup_num: int) -> list[int, int, bool]:
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

    def __init__(self, filename: str, soft_pity_dist: dict[int, float], copies_max=7) -> None:
        # soft_pity_dist - dictionary (empty for default option)
        self.max_wishes_required = 1260
        if soft_pity_dist == {}:
            # technically pity starts at 74 but this a more accurate way of estimation for some reason
            # still looking into why
            self.soft_pity_dist = {73: .06, 74: .12, 75: .18, 76: .24, 77: .3, 78: .35,
                                   79: .4, 80: .45, 81: .5, 82: .55, 83: .6, 84: .65, 85: .65, 86: .5, 87: .5, 88: .25, 89: 0.5, 90: 1}
            self.hard_pity = max(self.soft_pity_dist.keys())
            self.soft_pity_dist.update(
                {i: 0.006 for i in range(0, min(self.soft_pity_dist.keys()))})
            self.soft_pity_dist[self.hard_pity] = 1
        else:
            self.soft_pity_dist = soft_pity_dist
            self.hard_pity = max(self.soft_pity_dist.keys())
        # "hard pity" in this case only gives a guaranteed 5 star not guaranteed rateup
        self.filename = filename
        # note that this is different from constellations for characters there is max c6 but 7 copies to get there
        self.copies_max = copies_max
        self.hashtable = {}

        if exists(filename):
            self.load_hashtable()
        else:
            self.create_hashtable()
        # in my experience unneccessary since finding all solutions takes around 30 seconds - 2 minutes
        # still important to have though I feel
        self.incomplete_lookups = {i for i in range(0, 229502)}
        for val in self.hashtable:
            self.incomplete_lookups.discard(val)

        self.fileiscomplete = False
        # TODO why does hashtable seem to have more entries sometimes?
        if len(self.hashtable) >= 229502:
            self.fileiscomplete = True
        self.solutions_found_count = len(self.hashtable)

    def write_current_hash_table(self) -> None:
        # we write the file new every time since its easier
        # so thats why we don't do it super often
        with open(self.filename, 'w') as f:
            for i in range(0, 229502):
                if i in self.hashtable:
                    string_version_of_entry = [
                        str(self.hashtable[i][key]) for key in self.hashtable[i]]
                    write_string = str(i) + "," + \
                        ",".join(string_version_of_entry) + "\n"
                    f.write(write_string)
                else:
                    write_string = str(i) + ", -1\n"
                    f.write(write_string)
        if len(self.hashtable) == 229502:
            self.fileiscomplete = True

    def store_if_solution_doesnt_exist(self, num_wishes: int, pity: int, guaranteed: bool, solution: dict, write_periodically=False, periodic_interval=10000) -> None:
        lookup_num = self.lookup_num_generator(num_wishes, pity, guaranteed)
        if lookup_num in self.hashtable:
            pass
        else:
            self.hashtable.update({lookup_num: solution})
            # self.hashtable[lookup_num] = solution
            self.solutions_found_count += 1
            self.incomplete_lookups.discard(lookup_num)
            if write_periodically:
                # do every once in a while so its a little more efficient
                if self.solutions_found_count % periodic_interval == 0:
                    # print("CURRENTLY WRITING DO NOT CANCEL")
                    self.write_current_hash_table()
                    # print()
                    # print()
                    # print("WRITING COMPLETE YOU MAY NOW CANCEL")

    def specific_solution(self, num_wishes: int, pity: int, guaranteed: bool, current_copies: int, write_periodically=False, periodic_interval=10000) -> dict[int, float]:
        lookup = self.lookup_num_generator(num_wishes, pity, guaranteed)
        if lookup != -1 and lookup in self.hashtable:
            temp = self.hashtable[lookup]
            result = {i: temp[i] for i in range(0, self.copies_max+1)}
            return result
        if num_wishes == 0:
            result = {i: 0 for i in range(0, self.copies_max+1)}
            result[0] = 1
            self.store_if_solution_doesnt_exist(
                num_wishes, pity, guaranteed, result, write_periodically=write_periodically, periodic_interval=periodic_interval)
            return result
        # I don't know that its necessary for this base case but sometimes it seemed to glitch out and this is 1000% correct
        elif num_wishes == self.max_wishes_required:
            result = {i: 0 for i in range(0, self.copies_max+1)}
            result[self.copies_max] = 1
            self.store_if_solution_doesnt_exist(
                num_wishes, pity, guaranteed, result, write_periodically=write_periodically, periodic_interval=periodic_interval)
            return result
        elif current_copies >= self.copies_max:
            return {i: 0 for i in range(0, self.copies_max+1)}

        pity_val = self.soft_pity_dist[pity]
        # basic scheme is that we always have some no_five_star which isn't upgraded (i.e. no increase to higher num of copies)
        # but is multiplied by the inverse of the upgraded (getting a 5 star) portion so that when added with an upgraded portion the sum is 1
        # this process seems to logically describe what we would expect and also matches fairly well with the statistical data that I have created
        if pity < 90:
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
            num_wishes, pity, guaranteed, result, write_periodically=True, periodic_interval=periodic_interval)

        return result

    def calculate_and_write_all_solutions(self, periodic_interval=10000) -> None:
        if len(self.hashtable) >= 229502:
            self.fileiscomplete = True
        if not self.fileiscomplete:
            while len(self.incomplete_lookups) > 0:
                random_lookup = self.incomplete_lookups.pop()
                settings = self.lookup_to_setting(random_lookup)
                self.specific_solution(
                    settings[0], settings[1], settings[2], 0, periodic_interval=periodic_interval)

            self.write_current_hash_table()

    def probability_on_copies_to_num_wishes(self, probability_required, copies_required, pity=0, guaranteed=False):
        for i in range(0, self.max_wishes_required):
            current_probability = 0
            current_solution = self.specific_solution(i, pity, guaranteed, 0)
            for j in range(copies_required, self.copies_max+1):
                current_probability += current_solution[j]
            if current_probability >= probability_required:
                return i

# # FOR TESTING LOOKUPS
# for i in range(0, self.max_wishes_required):
#     wish_num = i
#     for j in range(0, 90):
#         pity = j
#         for k in range(0, 1):
#             if k == 0:
#                 guaranteed = False
#             else:
#                 guaranteed = True
#             lookup = test.lookup_num_generator(wish_num, pity, guaranteed)
#             reverse = test.lookup_to_setting(lookup)
#             if not (wish_num == reverse[0] and pity == reverse[1] and guaranteed == reverse[2]):
#                 print("ERROR")
#                 print(wish_num, pity, guaranteed)
#                 print(reverse[0], reverse[1], reverse[2])
#                 print()
