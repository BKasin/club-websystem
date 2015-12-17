# About this project

The aim of the project is to build a new website for the CSUSB Information Security Club. It will provide a central place to manage club membership, club events and RSVPs, projects and project sign-ups, etc. We are building this loosely according to the original database diagram located on Google Drive here (you must have the free [Draw.IO](https://www.draw.io) plugin installed first): [New Multi-club Website - Data Model](https://drive.google.com/file/d/0B2eX_I6RM9VBVVdONXYyRGpzSWs/view?usp=sharing). If you would like write-access to this diagram, contact Kenneth Johnson.

## Key goals

* Easy to contribute to - At any time, an interested person should be able to easily clone the repo, use this Readme to setup a development environment, and begin contributing right away. So keep this Readme up-to-date.
* Easy to manage - The administration of the website content should be intuitive, even for future club officers who may not have any web development or programming experience.
* Well-documented - This codebase will be handed down to future students, so it must be self-explanatory. Use code comments liberally.
* Secure - As a cybersecurity club, our website must have security included from the beginning. So while programming, keep your hacker hat on!
* Cross-platform and mobile-friendly - While programming, test your code on multiple browsers, operating systems, and devices.
* Supports multiple clubs - While it is currently used only by the InfoSec Club, it originally was intended as a multi-club codebase, with independent front-ends (templates, static content) for each club. Let's keep it that way, in case a club wants to join in the future.

## Developers

* Kenneth Johnson, [*securedirective*](https://github.com/securedirective) - *lead developer*
* Patrick Gillespie, [*Alofoxx*](https://github.com/Alofoxx)
* Juan Nevares, [*JuanNevares*](https://github.com/JuanNevares)
* Brendan Higgins, [*BrendanHiggins*](https://github.com/BrendanHiggins)

To get involved, follow the instructions below under the Development heading.


# Technology used

## Platform

* To ensure future club members can easily maintain this project, the popular [Python](https://docs.python.org/2.7/) programming language was chosen (at this time we're using Python 2.7, but we'll convert to Python 3 eventually).

## Python packages (installed with pip)

* For a web framework, we chose the well-supported [Django](https://docs.djangoproject.com/en/1.8/intro/overview/) because, compared to other frameworks and micro-frameworks, a lot of needed functionality comes ready out of the box. Primarily, Django provides our user authentication, routing of HTTP requests directly to Python functions, and abstracting the database models with its built-in [ORM](https://en.wikipedia.org/wiki/Object-relational_mapping). It also includes built-in protections for many security mistakes, such as cross-site request forgery.
* [django-registration-redux](https://django-registration-redux.readthedocs.org/en/latest/) extends Django's authentication features to also make new user sign-ups easy.
* [django-versatileimagefield](http://django-versatileimagefield.readthedocs.org/en/latest/overview.html) is a drop-in replacement for Django's ImageField that will automatically generate the desired resolutions for an image.
  * This depends on [Pillow](http://pillow.readthedocs.org/en/latest/) for the actual image processing.
* [django-admin-bootstrapped](https://github.com/django-admin-bootstrapped/django-admin-bootstrapped) customizes the adiministration pages of Django (/admin) to use Bootstrap.
* [django-crispy-forms](http://django-crispy-forms.readthedocs.org/en/latest/) provides a "crispy" template tag that will render forms using Bootstrap. It also allows quite a bit of form layout customization from Python instead of using HTML.
* [django-mailer](https://github.com/pinax/django-mailer/) stores all outgoing emails in the database instead of sending them right away. This way, any send failures don't cause the page rendering to fail. Also, it allows us to batch and retry failed emails.
  * This depends on [lockfile](http://pythonhosted.org/lockfile/) for managing file locks in a platform-independ way.
* [html2text](http://alir3z4.github.io/html2text/) is used in the our custom email template engine to generate a plaintext (markdown-like) version of an email if none is provided.
* [CommonMark-py](https://github.com/rolandshoemaker/CommonMark-py) (official package name is *commonmark*) provides a Python renderer for markdown code using the [CommonMark specifications](http://spec.commonmark.org/0.22/), instead of the older and somewhat vague Markdown specs.
* [django-wiki](http://django-wiki.readthedocs.org/en/latest/) (official package name is simply *wiki*) provides a simple wiki with image upload support and document revision tracking. This also depends on several packages:
  * [django-sekizai](http://django-sekizai.readthedocs.org/en/latest/)
    * [django-classy-tags](http://django-classy-tags.readthedocs.org/en/latest/) provides a class-based way of declaring new template tags.
  * [Pillow](http://pillow.readthedocs.org/en/latest/) for image processing.
  * [django-nyt](https://github.com/benjaoming/django-nyt) provides a "notifications" menu that is customizable by individual users, based on which notifications they wish to subscribe to.
  * [django-mptt](http://django-mptt.github.io/django-mptt/) adds support for Modified Preorder Tree Traversal, a technique for storing hierarchical data in a database.
  * [six](http://pythonhosted.org/six/) allows a single codebase to run on Python 2 and 3.
  * [sorl-thumbnail](http://sorl-thumbnail.readthedocs.org/en/latest/) adds template tags for loading image thumbnails.
  * [Markdown](http://pythonhosted.org/Markdown/) is a Python implementation of John Gruber’s Markdown, in contrast to the Commonmark specification we use elsewhere on the website.

## Front-end

* We follow the latest [HTML5](http://www.w3schools.com/html/html5_intro.asp) and [CSS3](http://www.w3schools.com/css/css3_intro.asp) standards.
* [Bootstrap](http://getbootstrap.com/) provides mobile-friendly pages that are responsive to browser sizes.
* [FullCalendar](http://fullcalendar.io/) provides a Javascript calendar much like Google Calendar.
* [jQuery](http://learn.jquery.com/about-jquery/) makes many of our Javascript tasks much easier. It is also required by Bootstrap and FullCalendar.
* [Commonmark.js](https://github.com/jgm/commonmark.js) is used for rendering CommonMark client-side, using only Javascript.
* [Lodash, modern build](https://lodash.com/) provides some extra Javascript functionality used in our split-view CommonMark editor.
* [Autosize](http://www.jacklmoore.com/autosize/) is also used in the split-view CommonMark editor for resizing the TEXTAREA as necessary to contain all the CommonMark code without using scrollbars.
* [CSS Toggle](https://ghinda.net/css-toggle-switch/bootstrap.html) is used in the event creating/editing form to theme the HTML Input checkmarks and option buttons into nice colorful sliders.


# Development

## Forking the repository

See [Fork a Repo](https://help.github.com/articles/fork-a-repo/) and [Pull Requests](https://help.github.com/articles/using-pull-requests/).

## Setting up your development environment

Install the following Linux packages. __Note:__ Package names and methods of installing them may be different for different distributions of Linux.

* python2
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

Install all required python dependencies:

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

## Passwords

For development purposes only, the Django superuser is `root` with a password of `pw`. You can log into the main site or the /admin site using these credentials. To be consistent, use the same password for any other accounts used for development.


# Production

## Web server

[Need details]

## Setting up the production environment

The production server must at least contain these requirements:

* nginx
* python v2.7.x
* virtualenv for python2
* libjpeg-dev
* a virtual environment setup with the packages listed in `requirements.txt`

For email to work in production, you must add django-mailer to the server's crontab. Since django-mailer puts all outbound email into the database instead of immediately sending it, we use its `send_mail` command to actually send out the emails. Any email that fails will be changed to priority `deferred`. The `retry_deferred` command will mark all deferred emails as medium priority, so the next pass of `send_mail` will attempt to send them again.

As an example, to send mail each 5 minutes and queue the failed emails for retry each 20 minutes, add this to the server's crontab:

    0,5,10,15,20,25,30,35,40,45,50,55  * * * * (< path to venv >/mailer send_mail --cron 1)
    1,21,41                            * * * * (< path to venv >/mailer retry_deferred --cron 1)
