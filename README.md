# test_flask.github.io

for WIN:
    py -3 -m venv .venv
    .venv\scripts\activate

    python -m flask run

    pip install werkzeug etc..

    DB:
    python
    from app import db
    db.create_all()
    exit()

    GITignore:
    git status
    git rm -r --cached .venv/

# iantonova-cs50-turbo-pfoject.github.io
Personal Portfolio WEB app

https://www.youtube.com/watch?v=7jKsHOZk-IE&list=PLCC34OHNcOtolz2Vd9ZSeSXWc8Bq23yEz&index=12

# pip freeze
    alembic==1.7.5
    click==8.0.3
    colorama==0.4.4
    Flask==2.0.2
    Flask-Migrate==3.1.0
    Flask-SQLAlchemy==2.5.1
    Flask-WTF==1.0.0
    greenlet==1.1.2
    itsdangerous==2.0.1
    Jinja2==3.0.3
    Mako==1.1.6
    MarkupSafe==2.0.1
    SQLAlchemy==1.4.29
    Werkzeug==2.0.2
    WTForms==3.0.1

to start(macOS):
>export FLASK_APP=application.py
>export FLASK_ENV=development
>python3 -m flask run

to start(win):
>.venv\scripts\activate
>python -m flask run

to add to .gitignore(win+macOS):
>git status
>git rm -r --cached __pycache__

MIGRATE(macOS):
>python3 -m flask db 
>python3 -m flask db init
>python3 -m flask db migrate -m 'Initial Migration'
>python3 -m flask db upgrade 
MIGRATE(win):
>flask db migrate -m 'added password field

# (17) Add A Blog Post Model and Form 
The class Posts(db.Model) was created -> migrate
> python3 -m flask db migrate -m 'Add Routes Model'
> python3 -m flask db upgrade

# (14) - Using Hashed Passwords For Registration 
password_hash not in db yet -> migrate
> python3 -m flask db migrate -m 'added password field'
> python3 -m flask db upgrade 
add fields to add_user.html -> app.py

# 13) - Hashing Passwords With Werkzeug
flask shell
from app import Users
u = Users()
u.password = 'cat'          - set password
u.password                  - check if it returns
                arswer correct: Traceback (most recent call last):
                                File "<console>", line 1, in <module>
                                File "D:\Git\iantonova-cs50-turbo-pfoject.github.io\app.py", line 36, in password
                                    raise AttributeError('Password is not a readable attribute!')
                                AttributeError: Password is not a readable attribute!
u.password_hash             - hash needed
                arswer correct:             'pbkdf2:sha256:260000$JGToVqxU4olmStek$f02838ab020f993efe955c4c64c07800592edaf5eff8cc4caa357678047ed043'
u.veryfy_password('cat')    - more check: lets veryfy
                arswer correct: True
u.veryfy_password('catd')   - try another password
                arswer correct: False
u2 = Users()                - lets create another user (u2)
u2.password = 'cat'         - lets use same password
u2.password_hash            - hashes are diffrent (correct)
                arswer correct:     
                'pbkdf2:sha256:260000$xzDWKZ9DupKwgxoj$cc7c985c0bd536caaea06c33b05d340826161432f1dd2962359ac04c20f5508c'
exit()

