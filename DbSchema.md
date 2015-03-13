# Introduction #

The database schema for the application should be updated so that it is easier to maintain and expand.


# Details #

The most basic representation is that of an "expense" associated with a "user".
However, a third basic feature that is useful immediately is the "type" of expense.

If the database schema is expected to change over time, then it is also critical that the current schema version be tracked as well.

A simple, but [normalized](http://en.wikipedia.org/wiki/Database_normalization), schema for this data follows:

```
CREATE TABLE user(id INTEGER PRIMARY KEY, name TEXT);

CREATE TABLE expense_type(id INTEGER PRIMARY KEY, description TEXT);

CREATE TABLE expense(id              INTEGER PRIMARY KEY,
                     user_id         INTEGER,
                     expense_type_id INTEGER,
                     amount          REAL,
                     FOREIGN KEY(user_id) REFERENCES user(id),
                     FOREIGN KEY(expense_type_id) REFERENCES expense_type(id));

CREATE TABLE app_info(db_version INTEGER);

PRAGMA foreign_keys = ON;
```


# TODO #

  * Write a script to migrate old databases to the new schema.
  * Detect old database version on start and ask the user if they want to migrate.
  * Update SQL queries for the new schema.
  * Consider tables that may be added later (e.g. revenue, budget).