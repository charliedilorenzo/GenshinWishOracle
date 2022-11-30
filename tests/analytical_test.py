import pytest
import os
# from mainstuff.analytical import AnalyticalRecursiveTest
# from analytical import AnalyticalRecursiveTest
from mainstuff.analytical import AnalyticalRecursiveTest


class TestClass:
    def test_lookups_are_invertible(self):
        print("WJASSUP")
        print(os.getcwd())
        analytical_object = AnalyticalRecursiveTest({})
        for i in range(0, analytical_object.max_wishes_required):
            wish_num = i
            for j in range(0, 90):
                pity = j
                for k in range(0, 1):
                    if k == 0:
                        guaranteed = False
                    else:
                        guaranteed = True
                    lookup = analytical_object.lookup_num_generator(
                        wish_num, pity, guaranteed)
                    reverse = analytical_object.lookup_num_to_setting(lookup)
                    if not (wish_num == reverse[0] and pity == reverse[1] and guaranteed == reverse[2]):
                        assert 0
            assert 1
