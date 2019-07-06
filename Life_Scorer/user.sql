CREATE TABLE users (
    id integer primary key,
    username text unique not null,
    password text not null,
    email text
);

CREATE TABLE tokens (
    id integer primary key,
    user_id integer,
    token text,
    token_expiry integer,
    FOREIGN KEY(user_id) REFERENCES users(id)
);