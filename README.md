# Flask Users API

## Prerequisites

This `datetime`, `secrets`, `jwt`, `functools`, `flask`, `flask_sqlalchemy`, and `flask_bcrypt`. The former two are part of the Python standard library. The latter three may need to be installed. To do so, simply run `pip install flask`, `pip install flask_sqlalchemy`, and `pip install flask_bcrypt` as needed.

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

It will run in debug mode. Navigating to `localhost:5000` in your browser will show the message `The API is ready!`. Now you can hit the endpoints with your favorite application&mdash;[Postman](https://www.getpostman.com/) is a great option.

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
* `/user/deactivate/<id>` (`PUT`) : Deactivate user with public_id `<id>`
* `/user/activate/<id>` (`PUT`) : Activate user with public_id `<id>`
* `/user/delete/<id>` (`DELETE`) : Delete user with public_id `<id>`

### Example

1. Hit ``/user/new` with the JSON data

```json
{
	"username":"someUser",
	"first_name":"John",
	"last_name":"Doe",
	"password":"password",
	"email":"example@example.com"
}
```

2. Then `/users` will return all users in JSON format as shown here.

```json
{
    "users": [
        {
            "active": true,
            "admin": false,
            "email": "example@example.com",
            "first_name": "John",
            "join_date": "Fri, 25 May 2018 17:17:37 GMT",
            "last_name": "Doe",
            "public_id": "adfb33008a8ded5b08fd",
            "username": "someUser"
        }
    ]
}
```

3. You can see that someUser has the `public_id` of `adfb33008a8ded5b08fd`, thus this single user can be accessed at `/user/adfb33008a8ded5b08fd`, which returns the user in JSON.

```json
{
    "user": {
        "active": true,
        "admin": false,
        "email": "example@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "name": "someUser",
        "public_id": "adfb33008a8ded5b08fd"
    }
}
```
4. Get token at endpoint `/login`, which returns

```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNvbWVVc2VyIiwicHVibGljX2lkIjoiYWRmYjMzMDA4YThkZWQ1YjA4ZmQiLCJleHAiOjE1Mjc1MTQxNzl9.DUtX4KRxheIaeNkBSykDqOl7wsv_h0oOl2vK2i0CdZQ"
}
```

5. Now we can do powerful things like promote, activate, deactivate, and delete users by simply hitting the endpoint  `user/adfb33008a8ded5b08fd/promote` with our token from step 4 in the header: key `x-access-token`, value `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InNvbWVVc2VyIiwicHVibGljX2lkIjoiYWRmYjMzMDA4YThkZWQ1YjA4ZmQiLCJleHAiOjE1Mjc1MTQxNzl9.DUtX4KRxheIaeNkBSykDqOl7wsv_h0oOl2vK2i0CdZQ` to promote someUser. Doing so returns a confirmation message.

```json
{
    "message": "User (adfb33008a8ded5b08fd) promoted!"
}
```

6. Now, the endpoint `/user/adfb33008a8ded5b08fd` returns

```json
{
    "user": {
        "active": true,
        "admin": true,
        "email": "example@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "name": "someUser",
        "public_id": "adfb33008a8ded5b08fd"
    }
}
```

Notice someUser's admin status is changed.
