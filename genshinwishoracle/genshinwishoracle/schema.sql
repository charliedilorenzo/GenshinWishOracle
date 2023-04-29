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