CREATE TABLE users (
    id integer primary key,
    username text unique not null,
    password text not null,
    email text
);
