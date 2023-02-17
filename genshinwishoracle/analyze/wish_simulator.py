
import random 
from . import analytical
from . import models
def y__random_under_one(y):
    x = random.uniform(0, 1)
    return x <= y

class WishSim:
  def __init__(self, banner: models.Banner,desired_five_star ):
    #these are always initialized same
    self.five = "5⭐⭐⭐⭐⭐"
    self.four = "4⭐"
    self.rateup_count = 0

    # banner type specific info
    banner = banner.get_specified_banner_equivalent()
    self.banner_type = "character"
    if type(banner) == models.CharacterBanner:
        self.banner_type = "character"
        self.non_ru_five_stars = models.Character.objects.filter(rarity=5, limited=False)
        self.prob_at_value = analytical.DEFAULT_CHARACTER_BANNER_SOFT_PITY
        # TODO add five star rate?
        self.five_star_rate = analytical.BASE_CHARACTER_FIVE_STAR_RATE
        self.rate_up_prob = .5
    elif type(banner) == models.WeaponBanner:
        self.banner_type = "weapon"
        self.non_ru_five_stars = models.Weapon.objects.filter(rarity=5, limited=False)
        self.epitomized_path_progress = 0
        self.prob_at_value = analytical.DEFAULT_WEAPON_BANNER_SOFT_PITY
        # TODO add five star rate?
        self.five_star_rate = analytical.BASE_WEAPON_FIVE_STAR_RATE
        # TODO add fate point max
        self.epitomized_maximum = analytical.BASE_MAXIMUM_FATE_POINTS
        self.rate_up_prob = .75

    # rateups/non_rateups
    rateups = banner.rateups
    self.ru_five_stars = list(rateups.filter(rarity=5))
    self.ru_four_stars = list(rateups.filter(rarity=4))
    four_characters = models.Character.objects.filter(rarity=4, limited=False)
    four_weapons = models.Weapon.objects.filter(rarity=4, limited=False)
    self.non_ru_four_stars = list(four_characters.union(four_weapons))
    three_star_characters = models.Character.objects.filter(rarity=3, limited=False)
    three_star_weapons = models.Weapon.objects.filter(rarity=3, limited=False)
    self.three_stars = list(three_star_characters.union(three_star_weapons))
    self.desired_five_star = desired_five_star

    print(self.ru_five_stars)
    print(self.non_ru_five_stars)
    print(self.ru_five_stars)
    print(self.non_ru_four_stars)

    # these can be reassigned with roll()
    self.five_star_guaranteed = False
    self.five_star_pity = 0
    self.four_star_guaranteed = False
    self.four_star_pity = 0

    #these can be inferred now
    self.soft_pity = min(self.prob_at_value.keys())
    self.hard_pity = max(self.prob_at_value.keys())

    self.pulls_remaining = 0
    self.pulls = []

  def generate_five_star(self):
    # this is to check if we win 50/50, it will still run if we have guaranteed but it will not overwrite
    if (y__random_under_one(self.rate_up_prob)):
      self.five_star_guaranteed = True
    if (self.epitomized_path_progress >= self.epitomized_maximum):
      choice = self.desired_five_star
      self.epitomized_path_progress=0
      self.five_star_guaranteed = False
    elif (self.five_star_guaranteed):
      choice = random.choice(self.ru_five_stars)
      if (choice == self.desired_five_star):
        self.epitomized_path_progress=0
      else:
        self.epitomized_path_progress+=1
      self.five_star_guaranteed = False
    else:
      choice = random.choice(self.non_ru_five_stars)
      self.epitomized_path_progress+=1
      self.five_star_guaranteed = True
    self.five_star_pity = 0
    self.four_star_pity = 0
    self.pulls.append(choice)

  def generate_four_star(self):
    if (y__random_under_one(self.rate_up_prob)):
      self.four_star_guaranteed = True
    if (self.four_star_guaranteed):
      choice = random.choice(self.ru_four_stars)
      self.four_star_guaranteed = False
    else:
      choice = random.choice(self.non_ru_four_stars)
      self.four_star_guaranteed = True
    self.four_star_pity = 0
    self.pulls.append(choice)

  def roll(self, number_of_pulls: int, five_star_pity: int, five_star_guaranteed: bool, four_star_pity: int, four_star_guaranteed: bool, fate_points: int):
    #cap them out, just in case
    self.five_star_guaranteed = five_star_guaranteed
    self.five_star_pity = five_star_pity
    self.four_star_guaranteed = four_star_guaranteed
    self.four_star_pity = four_star_pity
    self.epitomized_path_progress = fate_points
    self.pulls_remaining = number_of_pulls
    while (self.pulls_remaining > 0):
        self.pulls_remaining -= 1
        self.five_star_pity+=1
        self.four_star_pity +=1
        # 5 star block - different rates for different pity leves
        if (y__random_under_one(self.five_star_rate) and self.five_star_pity < self.soft_pity):
            self.generate_five_star()
            continue
        elif (self.five_star_pity >= self.soft_pity):
            if (y__random_under_one(self.prob_at_value[self.five_star_pity])):
                self.generate_five_star()
                continue
        #this shouldnt ever be run but just in case
        elif (self.five_star_pity >= self.hard_pity):
            self.generate_five_star()
            continue

        # TODO WORK ON THESE VALUES
        # 4 star block - not too sure about the values here, but I don't think most people mind
        if (self.four_star_pity >= 10):
            self.generate_four_star()
            continue
        elif (self.four_star_pity == 9):
            if (y__random_under_one(.3688)):
                self.generate_four_star()
                continue
        else:
            if (y__random_under_one(.051)):
                self.generate_four_star()
                continue
        
        # generate a three star
        choice = random.choice(self.three_stars)
        self.pulls.append(choice)
        continue 
    return self.pulls