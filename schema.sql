DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

DROP TABLE IF EXISTS drivers;
CREATE TABLE drivers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    first_name TEXT,
    last_name TEXT,
    bolt_id TEXT,
    uber_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

DROP TABLE IF EXISTS settlements;
CREATE TABLE settlements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    driver_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (driver_id) REFERENCES drivers(id)
);

DROP TABLE IF EXISTS expenses;
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    driver_id INTEGER,
    date TEXT NOT NULL,
    description TEXT NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (driver_id) REFERENCES drivers(id)
);

-- Dodanie przykładowego administratora
INSERT INTO users (username, password, role) VALUES ('admin', 'admin123', 'administrator');

-- Dodanie przykładowego kierowcy (najpierw użytkownik)
INSERT INTO users (username, password, role) VALUES ('driver1', 'driver1password', 'driver');
-- A następnie jego dane w tabeli drivers
INSERT INTO drivers (user_id, first_name, last_name, bolt_id, uber_id) VALUES (1, 'Jan', 'Kowalski', 'JK123', 'JK456');