# Standing

This is the web interface for the Standing iOS app for ludic resistance.

Read more about the app and its background here: http://whatsthehubbub.nl/projects/standing/


# Installation Guide

## Set up a Django project (on OS X)
1. Install homebrew, by getting the commandline tools: https://developer.apple.com/downloads and then do the install homebrew here: http://mxcl.github.com/homebrew/
2. Open Terminal.app
3. Check python is installed by typing `python`
4. Install pip if you don't have it `sudo easy_install pip`
5. Use pip to install virtualenv: `sudo pip install virtualenv`
6. Find a fresh place to checkout the project: git@github.com:whatsthehubbub/victoryboogiewoogie.git use the Mac client: http://mac.github.com/
7. In the terminal `cd` to where you just checked out the project, for instance: `cd ~/Documents/projects/sake/victorycheckout`
8. Create a virtual environment if you don't have one yet: `virtualenv venv --distribute`
9. Start a virtual environment: `source venv/bin/activate`
10. Install all the necessary packages: `pip install -r requirements.txt`
11. If you have never done so, setup the database: `python manage.py syncdb`, follow the instructions you get and note down the username and password that give you /admin access to the django site
12. Because we use *south* to create the tables for the application (and to update after model changes) you need to run: `python manage.py migrate`
13. Start the server with `python manage.py runserver` and go to your django at http://127.0.0.1:8000/admin
13.1 If you want your server to be accessible from other machines, start your server with `python manage.py runserver 0.0.0.0:8000`. You will need to figure out your external hostname yourself.
[Optional]
14. Start redis with `redis-server /usr/local/etc/redis.conf`
15. Start rq with `python manage.py rqworker high default low` (requires redis)

To restart the server simply repeat steps 9 and 13.
To be up to date again always do: 9, 10, 12, 13.


## Install CodeKit (front-end)
1. Download from Incident57: http://incident57.com/codekit/
2. Start app and add the Standing directory as a new project
