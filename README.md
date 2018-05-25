# Flask Users API

## Prerequisites

This uses `datetime`, `secrets`, `flask`, `flask_sqlalchemy`, and `flask_bcrypt`. The former two are part of the Python standard library. The latter will need to be installed. To do so, simply run `pip install flask`, `pip install flask_sqlalchemy`, and `pip install flask_bcrypt`.

This is hardcoded for an sqlite database. To use, you will need to install sqlite. On a Debian-based system, run `sudo apt-get install sqlite3`.

## Setup

Run python in the application directory. Import the database object and initialize the database with the following commands.

    >>> from users import db
    >>> db.create_all()

Exit python, with `exit()`. Ensure the database file, `users.db`, has been created; `ls` should show to ensure the database file, `users.db`, has been created. You can even jump into sqlite to check the presence of the `user` table(s). In your terminal, run sqlite with `sqlite3 users.db`

    sqlite> .tables
    user
    sqlite>

Exit sqlite with `Ctrl-D`.

## Start

Now you are ready to start your server with the following command.

    python users.py

It will run in debug mode.

## Use

Hitting the following endpoints with the given request methods will perform the described actions.

* `/users` (`GET`) : Return all users
* `/user/new` (`POST`) : Create a new user
* `/user/<id>` (`GET`) : Return a single user with id <id>
* `/user/promote/<id>` (`PUT`) : Give admin status to user with id <id>
* `/user/demote/<id>` (`PUT`) : Remove admin status from user with id <id>
* `/user/delete/<id>` (`DELETE`) : Delete user with id <id>
