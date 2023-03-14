from django.test import TestCase

from ..models import Character


# class CharacterSetTest(TestCase):
#     def test_special_six_ssr_exists(self):
#         special_six_ssr =  ("Diluc", "Qiqi", "Keqing", "Mona", "Jean", "Tighnari")
#         for char in special_six_ssr:
#             sample = Character.objects.get(name=char)
#             self.assertEqual(sample.name, char)
#             self.assertEqual(sample.rarity, 5)
#             self.assertEqual(sample.limited, False)

#     def test_non_limited_five_stars(self):
#         sample = Character.objects.filter(rarity = 5, limited = False)
#         sample = set([item.name for item in sample])
#         expected = ("Diluc", "Qiqi", "Keqing", "Mona", "Jean", "Tighnari")
#         self.assertEqual(sample, expected)
        
#     def test_special_three_sr_exists(self):
#         special_three_sr =  ("Lisa", "Kaeya", "Amber")
#         for char in special_three_sr:
#             sample = Character.objects.get(name=char)
#             self.assertEqual(sample.name, char)
#             self.assertEqual(sample.rarity, 5)
#             self.assertEqual(sample.limited, False)

#     def test_limited_four_stars(self):
#         sample = Character.objects.filter(rarity = 4, limited = True)
#         sample = set([item.name for item in sample])
#         expected = ("Lisa", "Kaeya", "Amber")
#         self.assertEqual(sample, expected)



# test that there are 10 non-limited weapons
# test that ther are 5 three star weapons for each class (?) (there are three polearms only, recheck on that one weird sword too)