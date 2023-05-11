import genshinwishoracle.forms as forms
from users.models import Profile
import math
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

def add_list_entries(list_of_lists: list[list[float]]) -> list[float]:
    
    new_list = [0 for i in range(0,len(list_of_lists[0]))]
    desired_length = len(list_of_lists[0])
    for lst in list_of_lists:
        if len(lst) != desired_length:
            raise KeyError("All lists must be the same length")
        for i in range(0,len(lst)):
            new_list[i]+=lst[i]
    return new_list


def scalar_list(lst: list[float], factor: float) -> list[float]:
    # assumes that the lst have the same keys
    new_list = [item*factor for item in lst]
    return new_list


def upgrade_list(lst: list[float]) -> list[float]:
    # for a dictionary assumed to have keys that are ascending integers starting at 0, throws error if they are not
    # returns a new dictionary that the value for every key moved up to that key+1 except the final entry which is the previous key's value plus its current
    if len(lst) == 0 or len(lst) == 1:
        return lst
    new_list = []
    temp1 = lst[0]
    new_list.append(0)
    for i in range(1, len(lst)-1):
        temp2 = lst[i]
        new_list.append(temp1)
        temp1 = temp2
    new_list.append(temp1+lst[i+1])
    return new_list

def import_user_data(profile: Profile, form_type = None):
    # fields in general:
    # ["numwishes","numcopies","minimum_probability","character_pity", "character_guaranteed", "weapon_pity","weapon_guaranteed", "weapon_fate_points"]
    dictionary =  profile.__dict__
    required_fields = set(["numwishes","character_pity", "character_guaranteed", "weapon_pity","weapon_guaranteed", "weapon_fate_points"])
    result = {param_name: param_value for param_name, param_value in dictionary.items() if param_name in required_fields}
    result["numwishes"] = math.floor(profile.calculate_pure_primos()/160)
    if form_type and issubclass(form_type,forms.AnalyzeStatisticsToProbability):
        result.pop("numwishes")
    if form_type and issubclass(form_type,forms.AnalyzeStatisticsCharacter):
        result = {key:val for key,val in result.items() if not key.startswith("weapon")}
    if form_type and issubclass(form_type,forms.AnalyzeStatisticsWeapon):
        result = {key:val for key,val in result.items() if not key.startswith("character")}
    return result

def within_epsilon_or_greater(value_to_test, target, epsilon=0.0000001):
    if value_to_test > target:
        return True
    difference = abs(value_to_test-target)
    if difference <= epsilon:
        return True
    else:
        return False

# Just makes it simpler to read since we log in the same place every time and redirect the same way every time
class PersonalizedLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'