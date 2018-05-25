# Flask Users API

## Prerequisites

This uses `datetime`, `secrets`, `flask`, `flask_sqlalchemy`, and `flask_bcrypt`. The former two are part of the Python standard library. The latter will need to be installed. To do so, simply run `pip install flask`, `pip install flask_sqlalchemy`, and `pip install flask_bcrypt`.

This is hardcoded to use sqlite database, although SQLAlchemy can be configured for other options. I'll describe how to set up sqlite. You will need sqlite on your machine; let's install sqlite3. You may already have it; if it's installed, the command `sqlite3 -version` will return a version number, as illustrated below.

    `$ sqlite3 -version`
    `2.8.17`

If it is not present, the above command will throw an error at you, and you can install it with `sudo apt-get install sqlite3` on a Debian-based system.

## Setup

Run python in the application directory. Import the database object and initialize the database with the following commands.

    >>> from users import db
    >>> db.create_all()

Exit python, with `exit()`, and verify that the database file, `users.db`, has been created; `ls` should list the file. You can even jump into sqlite to check the presence of the `user` table. In your terminal, run sqlite with `sqlite3 users.db`

    sqlite> .tables
    user

Exit sqlite with `Ctrl-D`.

## Start

Now you are ready to start your server with the following command.

    python users.py

It will run in debug mode. Nagivating to `localhost:5000` in your browser will show the message `The API is ready!`. Now you can hit the endpoints with your favorite application. [Postman](https://www.getpostman.com/) is a great option.

## Use

A user object looks like this:

    {
        "public_id": "c58824ff6c6c3d52d83c",
        "first_name": "Jane"
        "last_name": "Doe"
        "username": "myUsername"
        "email": "email@ddr.ess",
        "admin": false,
        "join_date": "Sat, 05 Nov 1955 10:09:18 GMT",
    }

Hitting the following endpoints with the given request methods will perform the described actions.

* `/users` (`GET`) : Return all users
* `/user/new` (`POST`) : Create a new user
* `/user/<id>` (`GET`) : Return a single user with public_id `<id>`
* `/user/promote/<id>` (`PUT`) : Give admin status to user with public_id `<id>`
* `/user/demote/<id>` (`PUT`) : Remove admin status from user with public_id `<id>`
* `/user/delete/<id>` (`DELETE`) : Delete user with public_id `<id>`
