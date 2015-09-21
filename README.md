# About this project

The aim of the project is to develop a central codebase that multiple CSUSB student clubs (currently the ACM, IEEE, and InfoSec clubs) can use for years to build and maintain their individual websites. It will provide a central database for storing information on club events, club membership, attendance, etc. To ensure future club members can easily maintain this project, the popular [__Python__](https://docs.python.org/3/) programming language was chosen.

This specific repository is attempt #3 at getting this project off the ground. Previous repositories located at <https://github.com/CSE-Club/Website-Project> and <https://github.com/InfoSec-CSUSB/Website-Project> are no longer maintained.

A little at a time, we are building this loosely according to the original database diagram located on Google Drive here (you must have the free [Draw.IO](https://www.draw.io) plugin installed first): [New Multi-club Website - Data Model](https://drive.google.com/file/d/0B2eX_I6RM9VBVVdONXYyRGpzSWs/view?usp=sharing). If you would like write-access to this diagram, contact Kenneth Johnson.

(Fill in details on the codebase later)

# Developers

* Kenneth Johnson, [*securedirective*](https://github.com/securedirective)
* Patrick Gillespie, [*Alofoxx*](https://github.com/Alofoxx)
* Juan Nevares, [*JuanNevares*](https://github.com/JuanNevares)
* Brendan Higgins, [*BrendanHiggins*](https://github.com/BrendanHiggins)

# Getting involved

## Requirements

* python2 (2.7.x)... we will port everything later to python 3.4.x
* python2-virtualenv
* python2-pip
* git

__Note:__ Package names may be different for different distributions of Linux...

## Setting things up

Make a directory and clone the repository into it:

    mkdir ~/club-websystem
    cd ~/club-websystem
    git clone git@github.com:Alofoxx/club-websystem.git ./

Before you do anything else, create a virtual environment and activate it:

    virtualenv --python=python2 ./
    source bin/activate

Install all required python dependencies (make sure your virtual environment is activated first!):

    pip install -r requirements.txt

Rebuild the files that we exclude from the repo:

    cd src
    python manage.py makemigrations
    python manage.py migrate

Collect the various static files into the /static_in_env folder:

    python manage.py collectstatic

Run the server

    python manage.py runserver 0.0.0.0:8000

## Ongoing work

Since the database model can change from time to time, we include the migrations file in the repo. Each time you run `git pull`, you should use the migrations to update your copy of the database, instead of simply overwriting your database with the copy in the repo.

Run these commands after each `git pull`:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py collectstatic

# Temporary development passwords

For development purposes only, the django superuser is `root` with a password of `password123`. You can log into the /admin side of the site or the main portion using these credentials.

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
