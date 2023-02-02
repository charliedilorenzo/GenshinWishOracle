#### TODO

### CURRENT

- django
  - gui
  - checkout installed apps <https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-INSTALLED_APPS>

## New Stuff

- add wish simulator
- add extra data of percent extra wishes to analytical (search the TODO for note on idea of how)
- add social apps login

- in settings SESSION_COOKIE_AGE = 60 *60* 24 * 30
- add import to project primos

- add better rerouting of errors in project primo
  - try using "from django.shortcuts import redirect"
- add routing from project primos to analyze
- add proper current days into update mechanism for project primos
- starglitter back setting for calculating additional wishes
- add boring wish simulator
- banner creator: - make sure to check proper amount of 5 stars and 4 stars
- user setting for autoimport every time

- improve looks:
  - character banner / weapon banner (can probably reuse)
  - character banner creators / weapon banner creators (can probably reuse)
  - analysis input character / weapon
  - analysis results
    - add graph

- IMPROVE ANALYTICAL by adding a function to find single solution in a complete database
- pytest better analytical.py coverage
- figure out why there are two databases: one in mainstuff and one in the main dir
- add constants for main dir or something? for database i assume?
- add tests to proj future wishes
- when changing pity need to wipe the database of analytical entries relevant
- find proper icon for genshin wish oracle

## structure

For testing:

extra pity important properties:

- same as without pity up until soft_pity - current_pity

guaranteed important properties:

- double probability of rateup relative to non-guaranteed at least for 90 first
