-- Table definitions for the tournament project.

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players ( id SERIAL PRIMARY KEY,
                     name TEXT);

CREATE TABLE matches ( id SERIAL PRIMARY KEY,
		     winner_id INT references players (id),
		     loser_id INT references players (id));

CREATE VIEW player_totals as
    select p.id, p.name, count(distinct m.id) as wins, count(distinct l.id) as losses, 
        count(distinct m.id) + count(distinct l.id) as total_matches
    from players p
    left join matches m on p.id = m.winner_id
    left join matches l on p.id = l.loser_id
    group by p.id, p.name
