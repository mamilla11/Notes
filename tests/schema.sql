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

-- Create default user --
INSERT INTO notes.user (first_name, last_name, email, password, created)
VALUES (
    'Regular',
    'User',
    'user@mail.com',
    'sha256$nqHxhwFCxNTqhii9$78f3e7c16eca7d31ba7cadd366b02069387a2014fe3275a2eef1079887c46224',
    current_timestamp
);
    
-- Assign the 'admin' role to admin
INSERT INTO notes.user_role (user_id, role_id)
VALUES (
    (SELECT id FROM notes.user WHERE email = 'admin@mail.com'),
    (SELECT id FROM notes.role WHERE name = 'admin')
);

-- Assign the 'user' role to user
INSERT INTO notes.user_role (user_id, role_id)
VALUES (
    (SELECT id FROM notes.user WHERE email = 'user@mail.com'),
    (SELECT id FROM notes.role WHERE name = 'user')
);

-- Add note to admin
INSERT INTO notes.note (user_id, content, created)
VALUES
(
    (SELECT id FROM notes.user WHERE email = 'admin@mail.com'),
    'I was written by an admin',
    current_timestamp
);

-- Add note to user
INSERT INTO notes.note (user_id, content, created)
VALUES
(
    (SELECT id FROM notes.user WHERE email = 'user@mail.com'),
    'I was written by a user',
    current_timestamp
);
