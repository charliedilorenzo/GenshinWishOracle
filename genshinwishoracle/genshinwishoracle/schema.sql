CREATE TABLE IF NOT EXISTS analytical_solutions_character(
    lookup INT8 PRIMARY KEY,
    X REAL,
    C0 REAL,
    C1 REAL, 
    C2 REAL,
    C3 REAL,
    C4 REAL,
    C5 REAL,
    C6 REAL
);
CREATE TABLE IF NOT EXISTS analytical_solutions_weapon(
    lookup INT8 PRIMARY KEY,
    X REAL,
    R1 REAL,
    R2 REAL, 
    R3 REAL,
    R4 REAL,
    R5 REAL
);

CREATE TABLE IF NOT EXISTS character_banners(
    banner_name TEXT PRIMARY KEY,
    rateup_five_star TEXT,
    rateup_four_star1 TEXT,
    rateup_four_star2 TEXT,
    rateup_four_star3 TEXT
);
CREATE TABLE IF NOT EXISTS weapon_banners(
    banner_name TEXT PRIMARY KEY,
    rateup_five_star1 TEXT NOT NULL,
    rateup_five_star2 TEXT NOT NULL,
    rateup_four_star1 TEXT,
    rateup_four_star2 TEXT,
    rateup_four_star3 TEXT,
    rateup_four_star4 TEXT,
    rateup_four_star5 TEXT
);

-- CREATE TABLE IF NOT EXISTS user_settings(
--     setting_name TEXT PRIMARY KEY,
--     setting_value
-- );