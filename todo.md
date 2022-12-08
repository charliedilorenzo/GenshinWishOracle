#### TODO

### CURRENT

- django
  - gui

## Refactoring

- proj_future_wishes

## New Stuff

- django
  - gui
- figure out why there are two databases: one in mainstuff and one in the main dir
- add constants for main dir or something?
- readd proj future wishes
- add tests to proj future wishes
- add user settings to db
- when changing pity need to wipe the database of analytical entries relevant

## structure

- input user data
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

- banner creator
  - store and make your own banners
  - ru four stars
  - ru five stars
  - add when the banner starts and ends
    - when it ends is important

- starglitter back setting

- wishing probabilities calculator
  - allow to select created banner
  - character banner
  - weapon banner

- get amount of wishes required for at least n probability p amount of times

- primogem projector
  - allow to select created banner
  - possibly add weird welkin / bp settings

- wishing simulator
  - allow to select created banner
  - this will be shit and low priority

extra pity important properties:

- same as without pity up until soft_pity - current_pity

guaranteed important properties:

- double probability of rateup relative to non-guaranteed at least for 90 first
