# tournament
Udacity - implementation of a Swiss-system tournament

## Description
The goal of the Swiss pairings system is to pair each player with an opponent who has won the same number of matches, or as close as possible.

## Requirements
If you want to run the program you have to have [Python ~2.7](https://www.python.org/)
and [PostgreSQL](http://www.postgresql.org/) installed on your machine.

## Set Up

For an initial set up please follow these 3 steps:

1. Install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/).

2. Clone the [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm/tree/master/vagrant).

3. Inside the *vagrant* folder from the above-mentioned repository, replace the files inside the *tournament* folder with the files you can find in this present repository - [Github Link](https://github.com/iliketomatoes/tournament).


## Usage

Launch the Vagrant VM from inside the *vagrant* folder with:

`vagrant up`

`vagrant ssh`

Execute the following commands to create the necessary tables inside the database:

`cd /vagrant/tournament`

`psql tournament`

`\i tournament.sql`

Execute the following command to run the test and see the output from your console:

`python tournament_test.py`


## Extra credit goals

* Prevent rematches between players.

* Don’t assume an even number of players. If there is an odd number of players, assign one player a “bye” (skipped round). A bye counts as a free win. A player should not receive more than one bye in a tournament.

* Support games where a draw (tied game) is possible. This will require changing the arguments to reportMatch.

### Test description

In order to check if extra credits were achieved, the test suite implements the simulation of:

1. A tournament with an odd number of enrolled players.
2. A tournament with an even number of enrolled players.

Where, in both cases, tied games are allowed, players can't rematch among each other, players can't receive more than 1 Bye-round each.