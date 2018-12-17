CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    unique ( name )
    );
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    points INTEGER,
    categories_id INTEGER, 
    recurring integer, 
    display integer default 1,
    attributes text,
    description text,
    FOREIGN KEY(categories_id ) REFERENCES categories(id)
);
CREATE TABLE log(
    id integer primary key, 
    task_id integer, 
    qty integer, 
    note text,
    date text,
    time text,
    attributes text,
    FOREIGN KEY(task_id) REFERENCES tasks(id)
    );
