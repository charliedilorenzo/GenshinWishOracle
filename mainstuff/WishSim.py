import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import io
import os
import re
from os.path import exists
from NoStreamObj import NoStdStreams
import consts
from helpers import y__random_under_one
import userinput
import math
import consts
import time
import helpers


def main(user_data, dumb_mode = True):
  #defaults
  standard_five_stars = helpers.get_banner_of_type(user_data["banner_type"])
  four_stars = consts.FOUR_STAR_CHARACTERS+consts.FOUR_STAR_WEAPONS
  ru_four_stars = userinput.RU_FOUR_STARS
  ru_five_stars = userinput.RU_FIVE_STARS

  #temp
  if ("ru_five_stars" in user_data.keys()):
    ru_five_stars = user_data["ru_five_stars"]

  #pity, etc
  current_pity = user_data["current_pity"]
  current_guaranteed = user_data["current_guaranteed"]

  #pulls
  num_fates = user_data["num_fates"]
  num_primos = user_data["num_primos"]
  num_starglitter = user_data["num_starglitter"]
  num_genesis = user_data["num_genesis"]

  total_pulls = math.floor((num_primos+num_genesis)/160)+num_fates + math.floor(num_starglitter/5)

  #desired
  desired_five_stars = 0
  desired_five_star = user_data["desired_five_star"]
  desired_ru = user_data["desired_ru"]
  if user_data["banner_type"] == "weapon":
    if (desired_ru <= 0 or desired_ru > 5):
      desired_ru = 5
  else:
      if (desired_ru <= 0 or desired_ru > 7):
        desired_ru = 7


  simulator = WishSim(ru_four_stars,four_stars,ru_five_stars,standard_five_stars, desired_five_star=desired_five_star, banner_type=user_data["banner_type"])
  simulator.print_interesting_stats()
  print()
  [wishes_used, five_stars_acquired, ru_count] = simulator.roll(total_pulls,desired_five_stars,desired_ru,False,set_pity= current_pity,set_guaranteed= current_guaranteed)

  indent = consts.INDENT
  assessment = ru_count >= desired_ru
  # dumb_mode = False
  print()
  if (dumb_mode):
    #now we add dumb stuff to cmd output
    print("Goal Achieved? ")
    print()
    print()
    sys.stdout.write(indent+indent+"drumroll please ")
    sys.stdout.flush()
    # https://stackoverflow.com/questions/17220128/display-a-countdown-for-the-python-sleep-function
    for i in range(0,5):
      sys.stdout.write("."+' ')
      sys.stdout.flush()
      time.sleep(.38)
    time.sleep(.5)
    print()
    print()
    if (assessment):
      sys.stdout.write(indent+indent+"YES")
      sys.stdout.flush()
      time.sleep(.8)
      sys.stdout.write("!!!!!")
      sys.stdout.flush()
    else:
      sys.stdout.write(indent+indent+"no")
      sys.stdout.flush()
      time.sleep(.8)
      sys.stdout.write("....")
      sys.stdout.flush()
    time.sleep(2)
  else:
    if assessment:
      print(indent, indent, "Goal Achieved")
    else:
      print(indent, indent, "Goal NOT Achieved")
  print()
  simulator.print_interesting_stats(after=True)
  print(consts.INDENT,"Desired Number of Rateups: ", str(desired_ru))
  print()
  print(simulator.five_tally)
  return [wishes_used, five_stars_acquired, ru_count]
class WishSim:

  def __init__(self, ru_four_stars, four_stars, ru_five_stars, five_stars, desired_five_star = None, banner_type = "character"):
    #these are always initialized same
    self.five = "5⭐⭐⭐⭐⭐"
    self.four = "4⭐"
    self.rateup_count = 0
    # these can be reassigned with roll()
    self.guaranteed = False
    self.pity = 0
    self.epitomized_path_progress = 0 
    
    #info given in arguments
    self.ru_four_stars = ru_four_stars
    self.four_stars = four_stars
    self.ru_five_stars = ru_five_stars
    self.standard_five_stars = five_stars
    self.desired_five_star = desired_five_star
    self.banner_type = banner_type 

    # choices based on the banner
    if banner_type == "weapon":
        self.prob_at_value = consts.PROB_FIVE_STAR_AT_WISH_NUM_WEAPONS
        self.rate_up_prob = .75
        #these are too messy to fix if there are too many
        if (len(self.ru_five_stars) < 2):
          self.ru_five_stars = self.ru_five_stars+(len(self.ru_five_stars) < 2)*["Generic 5 Star"]
        if (len(self.ru_four_stars) < 5):
          self.ru_four_stars = self.ru_four_stars+["Generic 4 Star " + str(i) for i in range(0, 5-len(self.ru_four_stars))]
    else:
      banner_type = "character"

    if banner_type == "character":
      self.prob_at_value = consts.PROB_FIVE_STAR_AT_WISH_NUM_CHARACTERS
      self.rate_up_prob = .5
      self.desired_five_star = self.ru_five_stars[0]
      if (len(self.ru_five_stars) < 1):
        self.ru_five_stars = self.ru_five_stars+(len(self.ru_five_stars) < 1)*["Generic 5 Star"]
      if (len(self.ru_four_stars) < 3):
        self.ru_four_stars = self.ru_four_stars+["Generic 4 Star " + str(i) for i in range(0, 3-len(self.ru_four_stars))]

    #these can be inferred now
    self.soft_pity = min(self.prob_at_value.keys())
    self.hard_pity = max(self.prob_at_value.keys())

    self.four_guaranteed = False
    self.four_pity = 0
    self.number_pulled = 0
    self.five_tally = { i : 0 for i in (list(set(self.ru_five_stars + self.standard_five_stars))) }
    self.four_tally = { i : 0 for i in (list(set(self.ru_four_stars + self.four_stars))) }
    self.num_wishes = 0
    self.rolling_results = {"Wishes Used": 0, "5⭐ total": 0,"Rate_up 5⭐s": 0, "4⭐ total": 0, "Desired Rateups Obtained": 0}

  def print_for_char(self, char):
    if (char in self.five_tally.keys()):
      print(char + " #: " + str(self.five_tally[char]))
    elif (char in self.four_tally.keys()):
      print(char + " #: " + str(self.four_tally[char]))
    else:
      print("Character not found.")

  def num_five_stars_pulled(self):
    sum = 0
    for i in self.five_tally.keys():
      sum += self.five_tally[i]
    return sum

  def num_four_stars_pulled(self):
    sum = 0
    for i in self.four_tally.keys():
      sum += self.four_tally[i]
    return sum
  
  def ru_count(self):
      return self.five_tally[self.desired_five_star]

  def reset_pulls(self):
    self.guaranteed = False
    self.four_guaranteed = False
    self.pity = 0
    self.four_pity = 0
    self.number_pulled = 0
    self.five_tally = { i : 0 for i in (list(set(self.ru_five_stars + self.standard_five_stars))) }
    self.four_tally = { i : 0 for i in (list(set(self.ru_four_stars + self.four_stars))) }
    self.rateup_count = 0
    self.rolling_results = {"Wishes Used": 0, "5⭐ total": 0,"Rate_up 5⭐s": 0, "4⭐ total": 0}

  def print_interesting_stats(self, after=False):
    indent = consts.INDENT
    print()
    print("Some Interesting Statistics:")
    print(indent, "Current Number of Wishes Remaining: ", str(self.num_wishes))
    print(indent, "Current Five Star Pity: ", str(self.pity))
    print(indent, "Current Guaranteed Status: ", str(self.guaranteed))
    print()
    if (after):
      print(indent, "Wishes Used: ", str(self.rolling_results["Wishes Used"]))
      print(indent, "4⭐ total: ", str(self.rolling_results["4⭐ total"]))
      print(indent, "5⭐ total: ", str(self.rolling_results["5⭐ total"]))
      print(indent, "Rate_up 5⭐s: ", str(self.rolling_results["Rate_up 5⭐s"]))
      if self.banner_type == "weapon":
        print(indent, "Desired Rateups Obtained: ", str(self.rolling_results["Desired Rateups Obtained"]))

  def generate_five_star(self, silenced = False):
    # this is to check if we win 50/50, it will still run if we have guaranteed but it will not overwrite
    if (y__random_under_one(self.rate_up_prob)):
      self.guaranteed = True
    if (self.epitomized_path_progress >= 2):
      choice = self.desired_five_star
      self.epitomized_path_progress=0
      self.guaranteed = False
      self.rateup_count+=1
    elif (self.guaranteed):
      choice = random.choice(self.ru_five_stars)
      if (choice == self.desired_five_star):
        self.rateup_count+=1
        self.epitomized_path_progress=0
      else:
        self.epitomized_path_progress+=1
      self.guaranteed = False
    else:
      choice = random.choice(self.standard_five_stars)
      self.epitomized_path_progress+=1
      self.guaranteed = True
    self.five_tally[choice] +=1
    if not silenced:
      print(self.five+choice+" - Rolls Left: "+str(self.num_wishes)+" - Pity: "+str(self.pity))
    self.pity = 0
    self.four_pity = 0

  def generate_four_star(self, silenced = False):
    if (y__random_under_one(self.rate_up_prob)):
      self.four_guaranteed = True
    if (self.four_guaranteed):
      choice = random.choice(self.ru_four_stars)
      if not silenced:
        print(self.four+choice+" - Rolls Left: "+str(self.num_wishes)+" - Pity: "+str(self.pity))
      self.four_tally[choice] +=1
      self.four_guaranteed = False
    else:
      choice = random.choice(self.four_stars)
      if not silenced:
        print(self.four+choice+" - Rolls Left: "+str(self.num_wishes)+" - Pity: "+str(self.pity))
      self.four_tally[choice] +=1
      self.four_guaranteed = True
    self.four_pity = 0

  def roll(self, num_wishes, five_stars_desired, guaranteed_desired, silenced = False, set_pity = 0,set_guaranteed=False,set_epitomized_path = 0 ):
    #cap them out, just in case
    self.guaranteed=set_guaranteed
    self.pity = set_pity
    self.epitomized_path_progress = 0 
    if (self.banner_type == "character"):
      if (five_stars_desired <= 0 or five_stars_desired > 14):
        five_stars_desired = 14
      if (guaranteed_desired <= 0 or guaranteed_desired > 7):
        guaranteed_desired = 7
    else:
      if (five_stars_desired <= 0 or five_stars_desired > 30):
        five_stars_desired = 30
      if (guaranteed_desired <= 0 or guaranteed_desired > 5):
        guaranteed_desired = 5
    begin_wishes = num_wishes
    self.num_wishes = num_wishes
    five_stars_acquired = 0
    while (five_stars_desired > five_stars_acquired and guaranteed_desired > self.rateup_count  and self.number_pulled < begin_wishes and self.ru_count() < 15 and five_stars_acquired < 30):
      self.num_wishes -= 1
      self.pity+=1
      self.four_pity +=1
      self.number_pulled+=1
      # 5 star block - different rates for different pity leves
      if (y__random_under_one(0.006) and self.pity < self.soft_pity):
        self.generate_five_star(silenced=silenced)
        five_stars_acquired+=1
        continue
      if (self.pity >= self.soft_pity):
        if (y__random_under_one(self.prob_at_value[self.pity])):
          self.generate_five_star(silenced=silenced)
          five_stars_acquired+=1
          continue
      #this shouldnt ever be run but just in case
      if (self.pity >= self.hard_pity):
        self.generate_five_star(silenced=silenced)
        five_stars_acquired+=1
        continue

      # 4 star block - not too sure about the values here, but I don't think most people mind
      if (self.four_pity >= 10):
        self.generate_four_star(silenced=silenced)
        continue
      elif (self.four_pity == 9):
        if (y__random_under_one(.3688)):
          self.generate_four_star(silenced=silenced)
          continue
      else:
        if (y__random_under_one(.051)):
          self.generate_four_star(silenced=silenced)
          continue

    wishes_used = begin_wishes - self.num_wishes
    four_stars_acquired = self.num_four_stars_pulled()

    #update rolling results
    self.rolling_results["Wishes Used"] = self.rolling_results["Wishes Used"]+wishes_used
    self.rolling_results["5⭐ total" ] = self.rolling_results["5⭐ total" ]+five_stars_acquired
    self.rolling_results["Rate_up 5⭐s" ] = self.rolling_results["Rate_up 5⭐s" ] +self.ru_count()
    self.rolling_results["4⭐ total"] = self.rolling_results["4⭐ total"]+four_stars_acquired
    if self.banner_type == "weapon":
      self.rolling_results["Desired Rateups Obtained"] = self.rolling_results["Desired Rateups Obtained"]+self.rateup_count
    return [wishes_used, five_stars_acquired, self.rateup_count]