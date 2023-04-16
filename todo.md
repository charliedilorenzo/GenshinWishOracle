#### TODO

- checkout installed apps <https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-INSTALLED_APPS>

### immediate testing

- change the typo on the left of the graph for primos
- prefer percentages
- might consider dates at the bottom
- for wishing simulator direct the user to make banners if they dont have any
- "Please log in if you'd like to access more features." - get rid of it for the screen in user home
- from types import UnionTyping
- fix graph labelling Wish Probability Breakdown for None Wishes, None Pity, without Guaranteeds
- from typing Any, Dict, Iterator, List, Union
- think of some stuff that chatgpt might be able to solve for me
- views tests
- add tests for users
- fix user tests for new primogem record / snapshot
- add tests to primogemrecord / primogemsnapshot
- actually properly test the new analytical classes
- test for import user data
- manually test creating a new user

### immediate features

- think of some stuff that chatgpt might be able to solve for me
- fix user creation / password reset process
- fix can't edit banner name?
- add user limits for anything that will create a permanently stored object in database
  - 5 banners of each type per user
  - 100 primogem records
    - add export csv for primogem records
  - look for other things that users can generate other than users that have storage
- use add_banner method of Profile places
- make redirect from loginrequiredmixin work
- add desired five star for weapon banner wish simulator
- add graph to probability to numwishes with the wish values for the constellation as the y axis and alternative amounts of wishes as the x axis
- add over the max for wish statistics for over the max (1000 right now?)
- fix date-decidable in project primos for jan 1
  - make a bool field for choosing via banner or manually?
- fix register view
- rework database?

- add "advanced statistics" where you can drag and drop up to 2 banners for character and weapons each in order to see odds of that stuff
  - start smaller with just 1 banner of each and you can choose order for probability
  - then upgrade to two characters + 1 weapon
  - then upgrade to two character and 2 weapon, since two weapons would be intertwined

### tests

- additional tests
  - database tests
  - analytical tests
  - forms tests
  - views tests
  - forms tests
- analytical make sure that the probability increase is equal up until soft pity
- analystical make sure that for guaranteed its double probability up until average wish or so or some similar property
- add tests to proj future wishes

### make pretty

- add the user to the URI for the character banners
- add number of wishes to the sidebar per profile?
- make many to many selector a drag menu
- improve no banner page
- for banners make the arrow in the many to many bigger
  - in widgets.css with classes: selector chooser, selector add, selector remove
- make the banner creation / update selector not have the choose all and the remove all
- trash icon for delete button
- little write note with pen for edit button
- make dropdown favicon href
- make dropdown app name href
- add a little button to stop the autosaving when coming from project primos
- finish adding import data helper to all other parts of views
  - method or class
- improve looks:
  - character banner / weapon banner (can probably reuse)
  - character banner creators / weapon banner creators (can probably reuse)
  - analysis input character / weapon
- fix organization for css stuff
- find proper icon for genshin wish oracle

## optimizations for later

- user setting for autoimport every time?
- find the most realistic pity distribution
- get rid of hash table from analytical?
- add extra data of percent extra wishes to analytical (search the TODO for note on idea of how)
- import analytical database
- add an option to overlay projected primos on top of existing primogem records
- improve the accurary of four star distribution for wish sim

### Before making into website

- change 'domain' in views.py for users for password reset
- add social apps login
- add reset password
- ?
- fix the user support account for the to genshinwishoracle@gmail.com in the google auth zone
- change OAUTH here <https://github.com/settings/applications/new>

- in settings SESSION_COOKIE_AGE = 60 *60* 24 * 30

- starglitter back setting for calculating additional wishes

- add constants for main dir or something? for database i assume?

### Super Stretch

- allow change of pity distribution:
  - when changing pity need to wipe the database of analytical entries relevant
  -
- logrithmically seeking for probability to num wishes is likely useless since the space is only ~2000 big so it will reduce from 2000 operations to 10 operations (maybe) which probably isnt that big a deal in this case
- project primos UPDATE_IDENTIFIER for last update
