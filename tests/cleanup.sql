SET session_replication_role = replica;
SET CONSTRAINTS ALL DEFERRED;

DELETE FROM notes.user;
DELETE FROM notes.role;
DELETE FROM notes.note;
DELETE FROM notes.user_role;

SET CONSTRAINTS ALL IMMEDIATE;
SET session_replication_role = DEFAULT;
