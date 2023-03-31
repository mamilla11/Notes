\c notes_db
CREATE SCHEMA IF NOT EXISTS notes;
ALTER ROLE tester SET search_path TO notes,public;

CREATE TABLE IF NOT EXISTS notes.role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS notes.user (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(64) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    email VARCHAR(64) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    created timestamp with time zone
);

CREATE TABLE IF NOT EXISTS notes.note (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created timestamp with time zone,
    modified timestamp with time zone,
    FOREIGN KEY(user_id) REFERENCES notes.user (id)
);

CREATE TABLE IF NOT EXISTS notes.user_role (
    user_id INTEGER,
    role_id INTEGER,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES notes.user(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES notes.role(id) ON DELETE CASCADE
);

-- Add roles --
INSERT INTO notes.role (name) VALUES ('admin'), ('user');

-- Create default admin --
INSERT INTO notes.user (first_name, last_name, email, password, created)
VALUES (
    'Super',
    'User',
    'admin@mail.com',
    'sha256$nqHxhwFCxNTqhii9$78f3e7c16eca7d31ba7cadd366b02069387a2014fe3275a2eef1079887c46224',
    current_timestamp
);
    
-- Assign the 'admin' role to the new user
INSERT INTO notes.user_role (user_id, role_id)
VALUES (
    (SELECT id FROM notes.user WHERE email = 'admin@mail.com'),
    (SELECT id FROM notes.role WHERE name = 'admin')
);

-- Add two notes to the new user
INSERT INTO notes.note (user_id, content, created, modified)
VALUES
(
    (SELECT id FROM notes.user WHERE email = 'admin@mail.com'),
    'First Note',
    current_timestamp,
    current_timestamp
),
(
    (SELECT id FROM notes.user WHERE email = 'admin@mail.com'),
    'Second Note',
    current_timestamp,
    current_timestamp
);


