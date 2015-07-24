-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP VIEW standings;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;


CREATE TABLE players ( name TEXT,
                     registration_date DATE default CURRENT_DATE,
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

CREATE VIEW standings AS
        SELECT 
        p.id, 
        p.name, 
        (SELECT count(*) FROM matches RIGHT JOIN players
        	ON player_1 = id 
            WHERE 
                (player_1_result = 1) 
                OR 
                (player_2 = players.id AND player_2_result = 1)) 
        as won, 
        ( SELECT count(*) FROM matches, players 
            WHERE 
                ( player_1 = players.id AND player_1_result = 0.5 )
                OR 
                ( player_2 = players.id AND player_2_result = 0.5)) 
        as tied
        FROM  players AS p;

