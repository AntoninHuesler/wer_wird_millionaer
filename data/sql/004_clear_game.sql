DELETE FROM players;
DELETE FROM sqlite_sequence WHERE name = 'players';
VACUUM;
