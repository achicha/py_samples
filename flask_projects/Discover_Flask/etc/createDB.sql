-- delete old tables
DROP TABLE IF EXISTS posts;

-- posts table
CREATE TABLE IF NOT EXISTS posts (post_id SERIAL PRIMARY KEY, title CHAR(300), description CHAR(1000));
