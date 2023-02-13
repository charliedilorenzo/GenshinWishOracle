#### TODO

- checkout installed apps <https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-INSTALLED_APPS>

## New Stuff

- add graphs
  - for analysis results
  - for project primos
- add proper current days into update mechanism for project primos
- add extra data of percent extra wishes to analytical (search the TODO for note on idea of how)
- add social apps login
- make outputs list of form field names but cannot be filled out
- add wish simulator
- pin point exactly when to delete the wish in session part
- good container from boostrap for content block  class="container mb-3 mt-3"
- endblock title for endblock after block title
- add warnings for unfilled fields in:
  - project primos
  - analyze
  - banners

- in settings SESSION_COOKIE_AGE = 60 *60* 24 * 30
- add import to project primos

- add better rerouting of errors in project primo
  - try using "from django.shortcuts import redirect"

- starglitter back setting for calculating additional wishes
- banner creator: - make sure to check proper amount of 5 stars and 4 stars
- user setting for autoimport every time

- IMPROVE ANALYTICAL by adding a function to find single solution in a complete database
- pytest better analytical.py coverage
- figure out why there are two databases: one in mainstuff and one in the main dir
- add constants for main dir or something? for database i assume?
- add tests to proj future wishes
- when changing pity need to wipe the database of analytical entries relevant

- improve looks:
  - character banner / weapon banner (can probably reuse)
  - character banner creators / weapon banner creators (can probably reuse)
  - analysis input character / weapon
- fix organization for css stuff
- find proper icon for genshin wish oracle

## structure

For testing:

extra pity important properties:

- same as without pity up until soft_pity - current_pity

guaranteed important properties:

- double probability of rateup relative to non-guaranteed at least for 90 first
