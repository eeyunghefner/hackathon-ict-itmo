create table roles (
  id SERIAL primary key,
  name VARCHAR(50) NOT null
);

create table authorization_details (
  id SERIAL primary key,
  password_hash VARCHAR(255) NOT NULL
);

CREATE table hackathon_status (
  id SERIAL primary key,
  name VARCHAR(50) NOT null
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    university VARCHAR(255),
    phone VARCHAR(20),
    role_id INT NOT NULL REFERENCES roles(id) ON DELETE restrict,
    authorization_details_id int not null references authorization_details(id) on delete cascade,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE hackathons (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    theme VARCHAR(255) NOT NULL,
    format VARCHAR(50) NOT NULL,
    description TEXT,
    rules TEXT,
    status_id INT REFERENCES hackathon_status(id) ON DELETE SET null,

    registration_start_date TIMESTAMP NOT NULL,
    registration_end_date TIMESTAMP NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,

    max_participants INT CHECK (max_participants > 0),
    max_teams INT CHECK (max_teams > 0),
    max_team_size INT DEFAULT 5,

    created_by INT REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    hackathon_id INT NULL REFERENCES hackathons(id) ON DELETE CASCADE,
    captain_id INT NULL REFERENCES users(id) ON DELETE SET NULL, -- Капитан должен быть пользователем
    max_members INT, -- Может переопределять общий лимит хакатона, если NULL - берется из hackathons.max_team_size
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, hackathon_id) -- Уникальное название команды в рамках одного хакатона
);

CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    team_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    hackathon_id INT NOT NULL REFERENCES hackathons(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, hackathon_id)
);

-- Таблица участников команд (связь многие-ко-многим)
CREATE TABLE team_members (
    team_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (team_id, user_id) -- Пользователь может быть только в одной команде на хакатоне (логика должна проверять это на уровне приложения или через триггер)
);

CREATE TABLE team_requests (
    id SERIAL PRIMARY KEY,
    team_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(team_id, user_id)
);

CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    capacity INT NOT NULL
);

CREATE TABLE room_bookings (
    id SERIAL PRIMARY KEY,
    room_id INT NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
    created_by INT NULL REFERENCES users(id) ON DELETE SET NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    hackathon_id INT NOT NULL REFERENCES hackathons(id) ON DELETE CASCADE,
    room_id INT NOT NULL REFERENCES rooms(id) ON DELETE RESTRICT,
    title TEXT NOT NULL,
    description TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Тестовые данные

-- ROLES
INSERT INTO roles (name) VALUES
('admin'),
('organizer'),
('participant');


-- AUTHORIZATION DETAILS
-- Test password for seeded users: password123
INSERT INTO authorization_details (password_hash) VALUES
('pbkdf2_sha256$100000$ABEiM0RVZneImaq7zN3u_w$umGCViBGdu25Ilh0rwtLMy3LgeunGkO1M5rvYAVVhEY'),
('pbkdf2_sha256$100000$EREiIjMzRERVVWZmd3eIiA$GAQFeX3ZtUwf0xmkTn-7gzUCzbnxAUaXzHExpAO_F4I'),
('pbkdf2_sha256$100000$IiIzM0REVVVmZnd3iIiZmQ$_kz-2FGgvwqdUazrY_eAO7JZsaz4tENLmahR00OBPUU'),
('pbkdf2_sha256$100000$MzNERFVVZmZ3d4iImZmqqg$MYNd07TzrZ5oE58SK_Cjm9zAu2D6DH4tIyWUrJiC5bQ'),
('pbkdf2_sha256$100000$RERVVWZmd3eIiJmZqqq7uw$MCe5qyD1PrEqkTWRiq1cmdGZuxXXvp477MAEOjU9gB0'),
('pbkdf2_sha256$100000$VVVmZnd3iIiZmaqqu7vMzA$x7pX9p4QdepOYim6zUdwQ_poUT_4l1Vf6_9f8YFEwFM');


-- HACKATHON STATUS
INSERT INTO hackathon_status (name) VALUES
('draft'),
('published'),
('archived'),
('in_progress'),
('finished');


-- USERS
INSERT INTO users (email, full_name, university, phone, role_id, authorization_details_id)
VALUES
('admin@test.com', 'Admin User', 'ITMO University', '+123456789', 1, 1),
('organizer@test.com', 'Organizer User', 'ITMO University', '+123456780', 2, 2),
('alice@test.com', 'Alice Johnson', 'ITMO University', '+111111111', 3, 3),
('bob@test.com', 'Bob Smith', 'MSU', '+222222222', 3, 4),
('charlie@test.com', 'Charlie Brown', 'SPbSU', '+333333333', 3, 5),
('david@test.com', 'David Wilson', 'HSE', '+444444444', 3, 6);


-- HACKATHONS
INSERT INTO hackathons (
    title,
    theme,
    format,
    description,
    rules,
    status_id,
    registration_start_date,
    registration_end_date,
    start_date,
    end_date,
    max_participants,
    max_teams,
    max_team_size,
    created_by
)
VALUES
(
    'AI Hackathon',
    'Artificial Intelligence',
    'online',
    'Hackathon focused on artificial intelligence',
    'Build AI solutions and present a working prototype.',
    2,
    NOW(),
    NOW() + INTERVAL '10 days',
    NOW() + INTERVAL '15 days',
    NOW() + INTERVAL '17 days',
    100,
    20,
    5,
    2
),
(
    'FinTech Hackathon',
    'Financial Technology',
    'offline',
    'Build innovative financial technologies',
    'Teams should create a fintech MVP and pitch it to the jury.',
    2,
    NOW(),
    NOW() + INTERVAL '7 days',
    NOW() + INTERVAL '12 days',
    NOW() + INTERVAL '14 days',
    80,
    15,
    4,
    2
);


-- TEAMS
INSERT INTO teams (name, description, hackathon_id, captain_id, max_members)
VALUES
('CodeMasters', 'AI developers', 1, 3, 5),
('BugHunters', 'Backend and QA team', 1, 4, 5),
('FinGurus', 'Fintech product team', 2, 3, 4);


-- APPLICATIONS
INSERT INTO applications (team_id, hackathon_id, status)
VALUES
(1, 1, 'pending'),
(2, 1, 'approved'),
(3, 2, 'pending');


-- TEAM MEMBERS
INSERT INTO team_members (team_id, user_id)
VALUES
-- CodeMasters
(1, 3),
(1, 5),

-- BugHunters
(2, 4),
(2, 6),

-- FinGurus
(3, 3),
(3, 4);

-- TEAM REQUESTS
INSERT INTO team_requests (team_id, user_id, status)
VALUES
(1, 4, 'pending'),
(2, 5, 'pending');

-- ROOMS
INSERT INTO rooms (name, capacity)
VALUES
('Auditorium A', 200),
('Lecture Hall B', 120),
('Conference Room C', 40);

-- ROOM BOOKINGS
INSERT INTO room_bookings (room_id, created_by, start_time, end_time)
VALUES
(1, 2, '2026-05-10 10:00:00', '2026-05-10 14:00:00'),
(2, 2, '2026-05-10 12:00:00', '2026-05-10 15:30:00');

-- EVENTS
INSERT INTO events (hackathon_id, room_id, title, description, start_time, end_time)
VALUES
(1, 3, 'Opening Ceremony', 'Opening speech and kickoff', '2026-05-10 10:00:00', '2026-05-10 11:00:00'),
(1, 3, 'Team Introductions', 'Short presentations by teams', '2026-05-10 11:30:00', '2026-05-10 12:30:00');
