#### TODO

### CURRENT

- django
  - gui
  - checkout installed apps <https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-INSTALLED_APPS>

## Refactoring

- proj_future_wishes

## New Stuff

make names more sane

- add proj future wishes
  - starglitter back setting for calculating additional wishes
- allow proj future wishes to have proper data and direct into weapon banner / character banner
- add the ability for banners to have end dates and for users to proj for the end of a specific banner

- add side bar for navigation

- get amount of wishes required for at least n probability p amount of times
  - call it probability to wishes

- add users and user personal data:
  - users banners
  - number of wishes
    - num primogems
    - num fates
    - num starglitter
    - num genesis
  - pity
    - for character banner
    - for weapon banner
  - guaranteed
    - for character banner
    - for weapon banner
  - welkin user
  - bp user

- add boring wish simulator

- banner creator: - make sure to check proper amount of 5 stars and 4 stars

- improve looks:
  - character banner / weapon banner (can probably reuse)
  - character banner creators / weapon banner creators (can probably reuse)
  - analysis input character / weapon
  - analysis results

- figure out why there are two databases: one in mainstuff and one in the main dir
- add constants for main dir or something?
- readd proj future wishes
- add tests to proj future wishes
- add user settings to db
- when changing pity need to wipe the database of analytical entries relevant

## structure

For testing:

extra pity important properties:

- same as without pity up until soft_pity - current_pity

guaranteed important properties:

- double probability of rateup relative to non-guaranteed at least for 90 first
