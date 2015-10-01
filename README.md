# About this project

The aim of the project is to develop a central codebase that multiple CSUSB student clubs (currently the ACM, IEEE, and InfoSec clubs) can use for years to build and maintain their individual websites. It will provide a central database for storing information on club events, club membership, attendance, etc. To ensure future club members can easily maintain this project, the popular [__Python__](https://docs.python.org/3/) programming language was chosen.

This specific repository is attempt #3 at getting this project off the ground. Previous repositories located at <https://github.com/CSE-Club/Website-Project> and <https://github.com/InfoSec-CSUSB/Website-Project> are no longer maintained.

A little at a time, we are building this loosely according to the original database diagram located on Google Drive here (you must have the free [Draw.IO](https://www.draw.io) plugin installed first): [New Multi-club Website - Data Model](https://drive.google.com/file/d/0B2eX_I6RM9VBVVdONXYyRGpzSWs/view?usp=sharing). If you would like write-access to this diagram, contact Kenneth Johnson.

(Fill in details on the codebase later)

# Requirements

The production server must at least contain these requirements:

* nginx
* python v2.7.x
* virtualenv for python2
* libjpeg-dev
* a virtual environment setup with the packages listed in `requirements.txt`

# Developers

* Kenneth Johnson, [*securedirective*](https://github.com/securedirective) - *lead developer*
* Patrick Gillespie, [*Alofoxx*](https://github.com/Alofoxx)
* Juan Nevares, [*JuanNevares*](https://github.com/JuanNevares)
* Brendan Higgins, [*BrendanHiggins*](https://github.com/BrendanHiggins)

# Getting involved

## Setting up your environment

Install the following Linux packages. __Note:__ Package names and methods of installing them may be different for different distributions of Linux.

* python2 (2.7.x)... we will port everything to python 3.4.x later
* python2-virtualenv
* python2-pip
* git

Make a directory and clone the repository into it:

    mkdir ~/club-websystem
    cd ~/club-websystem
    git clone git@github.com:Alofoxx/club-websystem.git ./

Before you do anything else, create a virtual environment and activate it:

    virtualenv --python=python2 ./
    source bin/activate

Install all required python dependencies (make sure your virtual environment is activated first!):

    pip install -r requirements.txt

## Ongoing collaboration

Each development day should start by activating your virtual environment and pulling any recent commits from the team.

    cd ~/club-websystem/src
    source ../bin/activate

When you pull the recent commits, you have two choices...

1. Pulling the latest database from the repo will overwrite any changes you may have made. If you would rather keep the data in your database and simply use migrations to upgrade the models, do this as your `git pull`:

        mkdir -p ~/tmp
        mv {./,~/tmp/}db.sqlite3
        git pull
        mv {~/tmp/,./}db.sqlite3

2. The database in the repo usually has the latest migrations. If you want to dump your copy of the database in favor of the one in the repo, just perform `git pull`. But this will give an error if your copy has changed, so just move it out of the way first:

        mv -i db.sqlite3{,.bak}
        git pull

After pulling recent changes, you should apply the latest migrations:

    python manage.py showmigrations
    python manage.py migrate

Then, collect the various static files into the `static_in_env` folder:

    python manage.py collectstatic

For development use only, Django provides a simple webserver that you can start with the following command. In production, we'll use `apache` or `nginx` instead.

    python manage.py runserver 0.0.0.0:8000

If you want to test email features within your development environment, you can start Python's debug SMTP server and see the emails in the terminal without actually needing a working email server:

    python -m smtpd -n -c DebuggingServer localhost:1025

Then configure your clubwebsystem/settings/local.py accordingly:

    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025

# Passwords

For development purposes only, the django superuser is `root` with a password of `password123`. You can log into the main site or the /admin site using these credentials. To be consistent, use the same `password123` for any other accounts used for development.

# Working within the Nitrous development server

Using the Linux 'tmux' tool, so all collaborators can use the same terminal:
- Check if there is a screen running:
  - tmux list-sessions
- If it is, attach to it by number:
  - tmux attach
- If not, run a new one:
  - tmux
  - cd code/club-websystem
  - source .env/bin/activate
  - cd src
  - python manage.py runserver 0.0.0.0:3000
- To see who is connected to the tmux session:
  - tmux list-clients
- Exit from the screen session:
  - Type *Ctrl+B*, followed by the *d* key
- To get help on 'tmux' type *Ctrl+B*, followed by the *?* key

Using the Linux 'screen' tool, so all collaborators can use the same terminal:
- Check if there is a screen running:
  - screen -r
- If it is, attach to it by number:
  - screen -x [idnumber]
- If not, run a new one:
  - screen
  - cd code/club-websystem
  - source .env/bin/activate
  - cd src
  - python manage.py runserver 0.0.0.0:3000
- Exit from the screen session:
  - Type *Ctrl+A*, followed by the *d* key
- To get help on 'screen' type *Ctrl+A*, followed by the *?* key
