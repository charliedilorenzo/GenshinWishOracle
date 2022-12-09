
# def convert_to_breakdown_file(self, new_file_name, pity, guaranteed):
#     with open(new_file_name, "w") as f:
#         # descriptive preamble
#         f.write("Trials = Analytical    SKIP\n")
#         f.write("pity = {}, guaranteed = {}    SKIP\n".format(pity, guaranteed))
#         breakdown_columns = ["Wishes Available", "X"]
#         for i in range(0, self.copies_max):
#             breakdown_columns.append("C"+str(i))

#             f.write(",".join(breakdown_columns) + "    SKIP\n")
#             for i in range(0, self.max_wishes_required):
#                 num_wishes = i
#                 solution = self.specific_solution(
#                     num_wishes, pity, guaranteed, 0, periodic_interval=10000)
#                 solution = [str(solution[i])
#                             for i in range(0, len(solution))]
#                 f.write(str(i) + "," + ",".join(solution) + "\n")

# def load_hashtable_from_filename(self) -> None:
#     with open(self.filename, 'r') as f:
#         for line in f:
#             current_line = line.split(',')
#             # unsolved situations are listed as "key, -1" so we can just check for 2 length to see if there is content for the line
#             if len(current_line) == 2:
#                 continue
#             else:
#                 key = int(current_line.pop(0))
#                 breakdown = [float(current_line[i].strip()) for i in range(
#                     0, len(current_line))]
#                 self.hashtable[key] = breakdown

# def write_current_hash_table_to_filename(self) -> None:
#     # REPLACED BY "update_analytical_db" DEPRECATED
#     # we write the file new every time since its easier
#     # so thats why we don't do it super often
#     with open(self.filename, 'w') as f:
#         for i in range(0, self.max_lookup):
#             if i in self.hashtable:
#                 string_version_of_entry = [
#                     str(self.hashtable[i][key]) for key in self.hashtable[i]]
#                 write_string = str(i) + "," + \
#                     ",".join(string_version_of_entry) + "\n"
#                 f.write(write_string)
#             else:
#                 write_string = str(i) + ", -1\n"
#                 f.write(write_string)
#     if len(self.hashtable) == self.max_lookup:
#         self.fileiscomplete = True

# def create_hashtable(self) -> None:
#     base_cases = {}
#     base_case = [str(0) for i in range(0, self.copies_max+1)]
#     base_case[0] = str(1)
#     for i in range(0, (self.hard_pity+1)):
#         base_cases[self.lookup_num_generator(0, i, False)] = base_case
#         base_cases[self.lookup_num_generator(0, i, True)] = base_case

#     with open(self.filename, 'w') as f:
#         write_string = str(0) + "," + ",".join(base_case) + "\n"
#         f.write(write_string)
#         for i in range(1, self.max_lookup):
#             if i in base_cases:
#                 # the breakdown will be listed after the key
#                 write_string = str(i) + "," + ",".join(base_cases[i])
#                 f.write(write_string)
#             write_string = str(i) + ", -1\n"
#             f.write(write_string)
