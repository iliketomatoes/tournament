-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP VIEW IF EXISTS standings;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS outcomes;
DROP TABLE IF EXISTS matches;



CREATE TABLE players ( 
                        id SERIAL PRIMARY KEY,
                        name TEXT NOT NULL,
                        registration_date DATE DEFAULT CURRENT_DATE
                        );

CREATE TABLE matches ( 
                       id SERIAL PRIMARY KEY,
					   time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
					   player_1 INTEGER,
					   player_2 INTEGER 
                       );

CREATE TABLE outcomes ( 
                        match_id INTEGER REFERENCES matches(id) ON DELETE CASCADE,
                        player INTEGER NOT NULL,
                        -- Won: 1 point
                        -- Lost: 0 point
                        -- Tied: 0.5 point
                        player_outcome REAL,
                        PRIMARY KEY (match_id, player),
                        CHECK (player_outcome = 0 OR player_outcome = 1 OR player_outcome = 0.5)
                        );


CREATE VIEW standings AS
        SELECT 
        p.id, 
        p.name, 
        m.won
        FROM  players AS p
        LEFT JOIN (
            SELECT player, count(*)::INTEGER as won FROM outcomes WHERE player_outcome = '1' GROUP BY player 
            )  as m ON p.id = m.player;

