import genshinwishoracle.forms as forms
from users.models import Profile
import math
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy

def add_dictionary_entries(list_of_dicts: list[dict[int, float]]) -> dict[int, float]:
    new_dict = {key: 0 for key in list_of_dicts[0]}
    for dict in list_of_dicts:
        for key in list_of_dicts[0]:
            if type(dict[key]) != float and type(dict[key]) != int:
                raise TypeError(
                    "Dictionary contains keys that are neither intergers nor floats")
            new_dict[key] += dict[key]
    return new_dict


def multiply_dictionary_entries(dictionary: dict[int, float], factor: float) -> dict[int, float]:
    # assumes that the dictionary have the same keys
    new_dict = {}
    for key in dictionary:
        new_dict[key] = factor*dictionary[key]
    return new_dict


def upgrade_dictionary(dictionary: dict[int, float]) -> dict[int, float]:
    # for a dictionary assumed to have keys that are ascending integers starting at 0, throws error if they are not
    # returns a new dictionary that the value for every key moved up to that key+1 except the final entry which is the previous key's value plus its current
    if len(dictionary.keys()) == 0:
        return dictionary
    elif len(dictionary.keys()) == 1:
        value = [dictionary[key] for key in dictionary.keys()][0]
        if type(value) != float and type(value) != int:
            raise TypeError(
                "Dictionary contains keys that are neither integers nor floats")
        else:
            return dictionary

    new_dict = {}
    temp1 = dictionary[0]
    for i in range(1, len(dictionary)-1):
        if type(temp1) != float and type(temp1) != int:
            raise TypeError(
                "Dictionary contains keys that are neither integers nor floats")
        temp2 = dictionary[i]
        new_dict[i] = temp1
        temp1 = temp2
    if type(temp1) != float and type(temp1) != int:
        raise TypeError(
            "Dictionary contains keys that are neither integers nor floats")
    elif type(dictionary[i+1]) != float and type(dictionary[i+1]) != int:
        raise TypeError(
            "Dictionary contains keys that are neither integers nor floats")
    new_dict[i+1] = temp1+dictionary[i+1]
    new_dict[0] = 0
    return new_dict

def import_user_data(profile: Profile, form_type):
    dictionary =  profile.__dict__
    required_fields = list(form_type.Meta.fields)
    result = {}
    if issubclass(form_type,forms.AnalyzeStatisticsCharacter):
        dictionary["pity"] = dictionary.pop("character_pity")
        dictionary["guaranteed"] = dictionary.pop("character_guaranteed")
    if issubclass(form_type,forms.AnalyzeStatisticsWeapon):
        dictionary["pity"] = dictionary.pop("weapon_pity")
        dictionary["guaranteed"] = dictionary.pop("weapon_guaranteed")
        dictionary["fate_points"] = dictionary.pop("weapon_fate_points")
    if issubclass(form_type,forms.AnalyzeStatisticsToProbability):
        dictionary["numwishes"] = math.floor(profile.calculate_pure_primos()/160)
    if issubclass(form_type,forms.AnalyzeStatisticsToNumWishes):
        required_fields.remove('numcopies')
        required_fields.remove('minimum_probability')
    for key in required_fields:
        result[key] = dictionary[key]
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