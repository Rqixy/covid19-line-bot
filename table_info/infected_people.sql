CREATE TABLE IF NOT EXISTS infected_people (
    id SERIAL,
    new_people INTEGER NOT NULL,
    severe_people INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    infected_day TEXT NOT NULL,
    created_at TEXT NOT NULL
);