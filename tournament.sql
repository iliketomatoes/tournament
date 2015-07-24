-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;


CREATE TABLE players ( name TEXT,
                     time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     id SERIAL );

CREATE TABLE matches ( id SERIAL,
					 time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
					 player_1 INTEGER,
					 player_2 INTEGER,
					 -- Won: 1 point
					 -- Lost: 0 point
					 -- Tied: 0.5 point
					 player_1_result REAL,
					 player_2_result REAL );

