drop table if exists notes_table;
create table notes_table (
    id integer primary key autoincrement,
    title string not null
);

drop table if exists note_table;
create table note_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stackid INTEGER,
    title string not null,
    body string,
    FOREIGN KEY(stackid) REFERENCES notes_table(id) /* fk at end */
); 
