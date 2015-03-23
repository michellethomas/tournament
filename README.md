#Swiss-system Tournament

Contains an implementation of a Swiss-system tournament. The test file creates players, matches, and pairs players for the tournament. 


##Instructions

###Create the tournament database
Run "psql -f tournament.sql" to create the tournament database and associated tables.

###Run Tests
To run tests, run "python tournament_test.py".

###Use the module
To use tournament.py:
- create a python file and import tournament ("from tournament import *")
- call the functions to create a tournament

To see an example, refer to the functions in tournament_test.py.


##File Descriptions

tournament.py - interacts with the tournament database to add and remove players, add matches, get player standings, and pair players

tournament.sql - contains the table defenitions for the tournament database

tournament_test.py - test cases for tournament.py
