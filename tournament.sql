-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP VIEW IF EXISTS games_won;
DROP VIEW IF EXISTS games_tied;
DROP VIEW IF EXISTS games_played;
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
                       -- If player_2 has id = 0, means that it's been a skipped round
					   player_2 INTEGER DEFAULT 0
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


CREATE VIEW games_won AS
        SELECT 
        p.id AS player_id,  
        COALESCE(w.amount, 0) AS won
        FROM  players AS p 
        LEFT JOIN (
            SELECT player, count(*)::INTEGER as amount FROM outcomes WHERE player_outcome = '1' GROUP BY player 
            ) as w ON p.id = w.player;

CREATE VIEW games_tied AS
        SELECT 
        p.id AS player_id,  
        COALESCE(t.amount, 0) AS tied
        FROM  players AS p 
        LEFT JOIN (
            SELECT player, count(*)::INTEGER as amount FROM outcomes WHERE player_outcome = '0.5' GROUP BY player 
            ) as t ON p.id = t.player;

CREATE VIEW games_played AS
        SELECT 
            p.id AS player_id,  
            COALESCE(g.amount, 0) AS played
            FROM  players AS p 
            LEFT JOIN (
                SELECT player, count(*)::INTEGER as amount FROM outcomes GROUP BY player 
                ) as g ON p.id = g.player;                          


