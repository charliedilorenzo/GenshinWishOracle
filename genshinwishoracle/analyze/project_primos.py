import math
from datetime import datetime

def calc_days_into_update():
    # the start of 3.4 currently should be fine
    UPDATE_IDENTIFIER = datetime(2023,1,18)
    current = datetime.now()
    delta = current-UPDATE_IDENTIFIER
    days = delta.days
    # mod 42 since the standard update is 6 weeks long
    return days % 42 

def project_future_primos(current_primos, current_genesis_crystals,current_fates, current_starglitter, days_till_banner_end_date, welkin_moon = True, battlepass = False, abyss_stars = 27, current_days_into_update = -1):
    current_total_primos = current_primos+current_genesis_crystals+160*math.floor(current_starglitter/5) + 160*current_fates
    if (current_days_into_update == -1):

        # TODO FIX THIS and make it functional
        current_days_into_update = calc_days_into_update()
    day_in_month = datetime.now().day

    #primogems for daily commisions -60 per day- 2520 per update
    future_primos = days_till_banner_end_date*60
    #primogems for default of 27 stars abyss but can give more or less
    if abyss_stars > 36:
        abyss_stars = 36
    if abyss_stars < 0:
        abyss_stars = 0
    future_primos += 50*math.floor((abyss_stars)/3)*math.floor((day_in_month % 15+days_till_banner_end_date)/15)
    # TODO make this more precise, currently works kinda correctly but not accurate month per month
    #primogems from stardust exchange - 800 per month - ~1120 per update
    future_primos += 800*math.floor((day_in_month+days_till_banner_end_date)/30)
    #primogems from announcing next update: - 300 per update
    future_primos += 300*math.floor((current_days_into_update+days_till_banner_end_date)/42)
    #primogems from game update compensation: - 300 per update
    future_primos += 300*math.floor((current_days_into_update+days_till_banner_end_date)/42)
    #primogems from bug fixing: - 300 per update
    future_primos += 300*math.floor((current_days_into_update+days_till_banner_end_date)/42)
    #primogems from testing characters (assumes 2 banners) - 160 per update
    future_primos += 40*math.floor(((current_days_into_update % 21)+days_till_banner_end_date)/21)

    # TODO reevaluate amount from event wishes https://twitter.com/SaveYourPrimos/status/1500327010354094083/photo/1 https://gamerant.com/genshin-impact-13000-primogems-calculation-in-version-24/#:~:text=Every%20six%20weeks%2C%20Genshin%20Impact,translates%20to%20around%2060%20Wishes.
    #primogems from events - 1500
    future_primos += 1500*math.floor((current_days_into_update+days_till_banner_end_date)/42)

    # ~7460 total
    if(battlepass == True):
        # just assumes you get it all in time which might not be true
        # TODO change this assumption?
        future_primos += 1320*math.floor((current_days_into_update+days_till_banner_end_date)/42)
    if(welkin_moon == True):
        # primogems from welkin moon - 90 per day - 3780 per update
        future_primos += days_till_banner_end_date*90
    return future_primos+current_total_primos
