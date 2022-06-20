infected_people (
    id SERIAL NOT NULL,
    new_people INTEGER NOT NULL,
    severe_people INTEGER NOT NULL,
    deaths INTEGER NOT NULL,
    infected_day VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);