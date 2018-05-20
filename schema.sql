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
    FOREIGN KEY(categories_id ) REFERENCES categories(id)
);
CREATE TABLE log ( 
        id integer primary key, 
        task_id integer,
        qty integer,
        Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
        FOREIGN KEY(task_id) REFERENCES tasks(id)
        );
