#### TODO

- checkout installed apps <https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-INSTALLED_APPS>

## New Stuff

- views tests
- add tests for users
- manually test creating a new user
- fix user creation / password reset process
- add a little button to stop the autosaving when coming from project primos

- test views creating a new user
  - manually
- make many to many selector a drag menu

- split up the views for statistics into classes but keep a general omni view that they inherit from
- add tests to primogemrecord / primogemsnapshot
- finish adding import data helper to all other parts of views
  - method or class

- use add_banner method of Profile places
- test for import user data
- add the user to the URI for the character banners
- make dropdown favicon href
- make dropdown app name href
- add number of wishes to the sidebar per profile?
- make redirect from loginrequiredmixin work
- add desired five star for weapon banner wish simulator
- make the banner creation / update selector not have the choose all and the remove all
- trash icon for delete button
- little write note with pen for edit button
- add graph to probability to numwishes with the wish values for the constellation as the y axis and alternative amounts of wishes as the x axis
- for banners make the arrow in the many to many bigger
  - in widgets.css with classes: selector chooser, selector add, selector remove
- add options for over the max (1000 right now?)
- fix date-decidable in project primos for jan 1
  - make a bool field for choosing via banner or manually?
- fix register view
- improve no banner page
- add an option to overlay projected primos on top of
- additional tests
  - database tests
  - analytical tests
  - forms tests
  - views tests
  - forms tests

- user setting for autoimport every time?
- find the most realistic pity distribution
- get rid of hash table from analytical?
- add extra data of percent extra wishes to analytical (search the TODO for note on idea of how)
- import analytical database
- improve the accurary of four star distribution for wish sim

Before making into website:

- change 'domain' in views.py for users for password reset
- add social apps login
- add reset password
- ?
- fix the user support account for the to genshinwishoracle@gmail.com in the google auth zone
- change OAUTH here <https://github.com/settings/applications/new>

- in settings SESSION_COOKIE_AGE = 60 *60* 24 * 30

- starglitter back setting for calculating additional wishes
- banner creator: - make sure to check proper amount of 5 stars and 4 stars

- pytest better analytical.py coverage
- figure out why there are two databases: one in mainstuff and one in the main dir
- add constants for main dir or something? for database i assume?
- add tests to proj future wishes

- improve looks:
  - character banner / weapon banner (can probably reuse)
  - character banner creators / weapon banner creators (can probably reuse)
  - analysis input character / weapon
- fix organization for css stuff
- find proper icon for genshin wish oracle

- allow change of pity distribution:
  - when changing pity need to wipe the database of analytical entries relevant
  -
- logrithmically seeking for probability to num wishes is likely useless since the space is only ~2000 big so it will reduce from 2000 operations to 10 operations (maybe) which probably isnt that big a deal in this case
- project primos UPDATE_IDENTIFIER for last update

## structure

For testing:

extra pity important properties:

- same as without pity up until soft_pity - current_pity

guaranteed important properties:

- double probability of rateup relative to non-guaranteed at least for 90 first
