1.5-webfaction
==============

Opinionated django project template with recipe/script for deployment to webfaction. Django version:1.5. Server: Apache/Mod_WSGI. Assets: Webfaction nginx. Frontend: Bootstrap 2.x. DB: Webfaction Postgres. Secrets stored in environment variable.  Uses virtualenv.  Python version 2.x



# Django 1.5 quickstart for  Webfaction deployment
<!-- Uncomment this in your real project (and delete )
# {{ project_name|title }} Django Project

From [Django 1.4 project template for fast webfaction deployment](https://github.com/django-quickstart/1.5-webfaction)
 -->


## About

This is a template for starting Django 1.5 projects and deploying to webfaction.  It is opinionated and configured for the things that I like and repetitively end up adding before deployment.  It will not work with 1.4, but should work with 1.6.   

THIS IS A WORK IN PROGRESS AS OF 12/28/2013.  I AM IN THE PROCESS OF PORTING THIS OVER FROM MY HEROKU TEMPLATE.


## Quickstart Template Features ##
#####Logical default file tree
- Global assets, fixtures, applib directory.
- Project template and misc directories by default.
- Collects static and media into `assets/{static-destination,media}` respectively.

#####Deployment best practices by default
- Uses virtualenv and virtualenvwrapper.
- Uses pip and `requirements.txt`.
- Uses git.
- Uses environment variables for secrets.
- Includes a .gitignore for the usual junk.

#####Sane settings.py configurations by default
* Timezone set to UTC.
* Discourages storing credentials and secrets in the repository.
* Encourages storing credentials and secrets in environment variables 
* Uses `env['DJANGO_ENV']` to configure settings for each environment `['PRODUCTION', 'TEST', 'DEV']` in a single settings.py file that gets stored in repo
* Tolerates the use of `local_settings.py` file, by default only in DEV.

#####Encourages simple separation of apps by type: 
* Unmodified 3rd party apps installed to virtualenv site-packages 
* Modified 3rd party apps placed in `applib/` directory, applib/ added to path
* Apps specific to project to be created in `project_name/[app_name]` directory

#####Ready for Webfaction Deployment
* Instructions for setting up webfaction app
* Instructions for setting up webfaction env variables
* Instructions for setting up webfaction static
* Setup to use sendgrid for email delivery
* Uses AutoEnv to keep .env parity without needing heroku toolbelt

#####Common apps already installed with reasonable default configuration
* Django admin activated by default.
* allauth
* south
!!* django-storages for static/media on s3
!!* django-folder-storages to keep static/media in separate silos

####Other Goodies
* Simple 404 and 500 error templates.
* Bootstrap 2.x driven base.html
* Automatically builds a README with installation notes.

####Template
* Twitter Bootstrap based template included
* JQuery included
* AllAuth login signup manage links already in header
* JS in footer for faster page loading
* Google universal analytics code in base.html, commented out

###Template blocks cascade
* js > extra-js, css > extra-css, head > extra-head
* any use of an extra-[foo] block should include call to super
* `block content` is inside of a `block canvas` allowing for app level layouts while still using common `block content` idiom without a call to super at the page level
* expects base.html > app-base.html > view.html series of cascades


## Prerequisites ##

- [Webfaction account](http://www.webfaction.com/services/hosting?affiliate=blooksllc) 
- python2 >= 2.7, pip, virtualenv, 
- git, autoenv
- postgres


### First time system config/installation stuff.

``` bash
easy_install pip
pip install virtualenv, virtualenvwrapper
```

###Installing Postgres###
TODO


###Setting up AutoEnv###
To get environment variables working, this guide uses [autoenv](https://github.com/kennethreitz/autoenv)

I haven't been able to get autoenv working via pip, but the git installation method works for me:
``` bash
git clone git://github.com/kennethreitz/autoenv.git ~/.autoenv
echo 'source ~/.autoenv/activate.sh' >> ~/.bashrc
source ~/.bashrc
``` 

###Creating utility aliases (optional)
Adding the following to your ```~/.bash_aliases``` file can save a lot of repetitive and verbose keystrokes.  
``` bash
alias drpm ='python manage.py'
alias drpmr = 'python manage.py runserver 0.0.0.0:5000'
alias [project-name] = 'cd /[path]/[to]/[projectname]/ && source ~/ve/[project-name]/bin/activate'
```
Reload without restarting your terminal with
``` bash
source ~/.bash_aliases
```

These are based on the shortcuts I use when working with heroku: I intentionally keep django as 'd', foreman as 'f', and heroku as 'heroku' to make sure running commands locally is easy and remotely is hard.  It's very easy to type 'hrpm' when you mean 'frpm.'  Requiring the extra layer of thought can stop you from accidentally deleting your production database.

To add or edit aliases
``` bash
nano ~/.bash_aliases
``` 



# Installation #
## Preparing for a new project

There is some wait time while pip installs requirements and while running the first set of tests, these steps can be delayed until waiting for tasks to complete.

* Gather domain credentials
* Setup a django app in webfaction
* Setup a postgres db in webfaction



## Start the new project
### Setting up the local project environment
Create Virtualenv
``` bash
virtualenv --no-site-packages --distribute ~/ve/[project-name]
source ~/ve/[project-name]/bin/activate
``` 

Install Django
``` bash
pip install "django>=1.5,<1.6"
``` 

Start a project.
``` bash
django-admin.py startproject --template https://github.com/django-quickstart/1.5-webfaction/zipball/master --extension py,md,gitignore,dist,html [project-name]
cd [project-name]
touch virtenv_is_[project-name]
```

Remove the cruft 
``` bash
rm TODOS.txt LICENSE requirements.old.txt
``` bash


Install base requirements.
``` bash
pip install -r requirements.txt
```
NOTE: the requirements.txt provided in this repo has no versions.  requirements.old.txt has the latest versions that have been used and tested together.  

(Optional) Check for newer versions
Note that this command isn't instant, it can take a few seconds to start showing output.  This is normal.
``` bash
pip freeze | cut -d = -f 1 | xargs -n 1 pip search | grep -B2 'LATEST:'
pip install [package] --upgrade
``` 

Create local .env file
``` bash
cp sample.env .env && rm sample.env
``` 
NB there are other ways to manage dev environment variables, see discussion below.  

Validate
``` bash
python manage.py validate
```

Create DB
``` bash
sudo -u postgres createuser user -P
...
Enter pass
n
y
y
...
sudo -u postgres createdb -O user [project-name]
```


### Local changes script
Syncdb and migrate
``` bash
python manage.py syncdb && python manage.py migrate
``` 

Collect static
``` bash
python manage.py collectstatic --noinput
```

Run Tests
``` bash
python manage.py test
```

Fire up local/dev server
``` bash
python manage.py runserver 0.0.0.0:5000
``` 



## Deploying
### Preparing for first deploy
Unlike in the heroku quickstart, we can't deploy to webfaction by just doing a git push, and webfaction doesn't by default host a git repo for each of your apps (as of this writing on 12/28/13)

Thus, the process to get git setup and get each deploy up to the webfaction server takes more steps than getting it live on a heroku server.

Create git repo on github, or your preferred git host (without a readme or a gitignore)

Initialize an empty Git repository in your directory
``` bash
git init
```

Add your files
``` bash
git add .
git commit -m "initial commit"
``` 

Link your local directory to the upstream/origin
``` bash
git remote add origin https://github.com/[username]/[repo name].git
```

Now push your files up to github
``` bash
git push -u origin master
```

Get webfaction rolling:

* Setup a domain
* Follow webfactions instructions to create a django app and database:  
[http://docs.webfaction.com/software/django/getting-started.html](http://docs.webfaction.com/software/django/getting-started.html)
* SSH into your webfaction shell, cd to the app, clone your repo
* Go back to the control panel and create a static-file app symlinked to the assets folder

Configure Environment Variables
``` bash
heroku config:set DJANGO_ENV="PRODUCTION" DJANGO_DEBUG="false" 
heroku config:set AWS_ACCESS_KEY_ID=[KEY] AWS_SECRET_ACCESS_KEY=[KEY] 
```




### Regular Deploy Script
Run All Tests
``` bash
python manage.py test
```

Freeze Pip state
``` bash
pip freeze > requirements.txt
```

Commit Changes
``` bash
git add .
git commit -m "message"
```

Push repo to heroku
``` bash
git push 
```

SSH into webfaction, navigat to the app directory
Update app code, database schema, static files
``` bash
apache2/bin/stop
git pull
python2.7 manage.py syncdb && python2.7 manage.py migrate
python2.7 manage.py collectstatic
apache2/bin/start
```

Go see your site in action

That's it, the webfaction app is now configured and deployed.  


## Housekeeping
* Login to admin and set site, so emails don't come from example.com


# Options, considerations, and commands worth discussing
## Deploying
### Procfile settings
Not relevant on webfaction

## Working Locally
### Option 1: ENV Variables and vanilla manage.py - Not recommended
Set DEV environment variables, use standard django runserver command
``` bash
export DJANGO_DEBUG=True
export DJANGO_ENV=DEV

python manage.py runserver 0.0.0.0:5000
``` 
Not preferred because: 1) less dev-prod parity 2a) environment variables set like this aren't confined to the virtual environment 2b) they aren't maintained between virtenv sessions either (unless you set them in virtenv wrapper) 3) linux environment variables set with export aren't shared between shell sessions


### Option 2: Heroku Foreman - Preferred
Use .env file for environment variables, foreman spools up processes from the Procfile
``` bash
cp sample.env .env
foreman start
...
18:29:37 web.1  | started with pid 29000
18:29:38 web.1  | 2012-12-05 23:29:38 [29002] [INFO] Starting gunicorn 0.16.1
18:29:38 web.1  | 2012-12-05 23:29:38 [29002] [INFO] Listening at: http://0.0.0.0:5000 (29002)
18:29:38 web.1  | 2012-12-05 23:29:38 [29002] [INFO] Using worker: sync
18:29:38 web.1  | 2012-12-05 23:29:38 [29005] [INFO] Booting worker with pid: 29005
...
``` 
Preferred because creates closet dev-prod parity.  Automatically spools up worker nodes if they are declared in the procfile.

However, sometimes you want the runserver.  Run management and other commands via foreman -- given the way settings.py switches, this is required for anything that imports settings.py.  Of further advantage, Dev and production mental models are identical.  
``` bash
foreman run python manage.py [command]
foreman run python manage.py runserver 0.0.0.0:5000
``` 

### Option 3: VirtualenvWrapper PostActivate
http://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv

### Option 4: autoenv - Preferred when not using heroku
TODO
http://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv


## Working with VirtEnv
Put in home directory so VirtualBox symlink doesn't have issues
``` bash
virtualenv --no-site-packages --distribute ~/ve/[project-name]
source ~/ve/[project-name]/bin/activate
deactivate
``` 

For future reference, note where the virtenv is stored
``` bash
touch virtenv_is_[project-name]
```

Getting a specific python version
http://stackoverflow.com/questions/1534210/use-different-python-version-with-virtualenv
``` bash
virtualenv -p /usr/bin/python2.6
... or with wrapper ...
mkvirtualenv -p python2.6 env
``` 



## Working with PIP
Install from requirements.txt
``` bash
pip install -r requirements.txt
```

Freezing to reequirements.txt
``` bash
pip freeze > requirements.txt
```

Checking for later versions of packages
``` bash
pip freeze | cut -d = -f 1 | xargs -n 1 pip search | grep -B2 'LATEST:'
``` 

Auto update packages
``` bash
pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U
``` 

Upgrading a package
``` bash
pip install --upgrade [package] 
``` 

Uninstalling a package
``` bash
pip uninstall [package]
``` 



## Setting up databases
### Local Postgres DB
For dev/prod parity it is recommended that postgres be used locally as well as remotely
``` bash
sudo -u postgres createdb [whatever]
```

### Postgres on Heroku
Not relevant for webfaction




## Setting Environment Variables
### Locally Option 1 -- Not recommended
(see working locally above)
Setting and Verifying
``` bash
export DJANGO_ENV=DEV
echo $DJANGO_ENV
```

Deleting
``` bash
unset DJANGO_ENV
```
### Locally Option 2 -- recommended
(see working locally above)
Use a .env file and foreman


### On Heroku (Production and Staging/Testing)
Not relevant for webfaction


### On Webfaction
TODO


## Updating database with [South][south]
1. Make changes to your models
2. `$ ./manage.py schemamigration [appname] --auto`
3. `$ ./manage.py migrate [appname]`
4. [commit & push changes to heroku]
5. `$ heroku run ./manage.py migrate [appname]`


# Testing
http://www.tdd-django-tutorial.com
http://pycon-2012-notes.readthedocs.org/en/latest/testing_and_django.html

#Frontend
## Bootstrap

Getting latest version of bootstrap
``` bash
cd assets/assets
wget http://twitter.github.com/bootstrap/assets/bootstrap.zip && unzip bootstrap && rm bootstrap.zip 


wget  --no-check-certificate https://github.com/addyosmani/jquery-ui-bootstrap/zipball/v0.23 && unzip v0.23
cp -r addyosmani-jquery-ui-bootstrap-cf2a77b/ jquery-ui-bootstrap
```

Bootstrap resources
- http://bootsnipp.com
- http://fontcustom.com/


## Template Setup

In Base.html remember to
- Set Page Title base
- Set google analytics variables, uncomment google analytics section

In file directory
- Add favicons to assets/assets/ico

## Notes and Niceties
([psycopg2](http://initd.org/psycopg/) is a PostgreSQL adapter for Python.
mysql-python is a MySQL adapter for Python)

To make `.manage.py` executable if you don't want to type `python manage.py ...` all the time.
``` bash
chmod +x manage.py
```



## Things done on purpose and why
### Secret_key not put into environment variable

I think it is more work and more error prone to keep this as an env variable.  If this ever gets out of sync on a node the certs/cookies signed by that node will be incompatible with the rest of the system.   
``` python
#With fallback -- OK
SECRET_KEY = environ.get('SECRET_KEY', SECRET_KEY)
#Without fallback -- Better
SECRET_KEY = environ.get('SECRET_KEY')
#Just not doing it -- Best
```

### Requirements not split into ENV specific files
Some setups create a requirements file for _dev, _test, _prod, _common, and even go as far as to keep these in a separate folder. This is purposefully not done. 

The upsides of a single requirements.txt: 
1) It keeps closer dev/prod parity
2) If the packages aren't imported in production, they don't take up RAM
3) No extra steps required after pip freeze > requirements.txt
4) When something goes wrong in staging/test environment that works in dev, removes a debugging step

The downsides and risks of a single requirements.txt
1) Extra time for deploy/cold node startup while the server downloads the additional packages 
2) Unused packages take server disk space
3) Risk of mis-configuration silent failure in produciton


### Foreman(ruby) instead of Honcho(python)
As of 12/5/12 Honcho is ~Foreman written in python, less used, and a few features behind.  As it is a tool, and I haven't yet really had to dive into the guts, ruby seems fine to me for now.




## Configuration/settings samples
``` 
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    #'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
  }
}    
```   


## [Re]Sources

- [Part 1: The Basics &mdash; South v0.7 documentation](http://south.aeracode.org/docs/tutorial/part1.html)
- [Getting Started with Django on Heroku/Cedar | Heroku Dev Center](https://devcenter.heroku.com/articles/django)
- [Deploying Django to Heroku](http://offbytwo.com/2012/01/18/deploying-django-to-heroku.html)
- [PAAS bakeoff](http://appsembler.com/blog/paas-bakeoff-comparing-stackato-openshift-dotcloud-and-heroku-for-django-hosting-and-deployment/)
- [Rails like environs with django](http://www.elfsternberg.com/2009/10/14/rails-like-environments-with-django/)
- [Dev Guide to Django on Heroku](http://kencochrane.net/blog/2011/11/developers-guide-for-running-django-apps-on-heroku/)
- [south](http://south.aeracode.org/)
- [Django-Skel](https://github.com/rdegges/django-skel)
- [Django-prokect-skel](https://github.com/amccloud/django-project-skel)
- [Django-project-skel](https://github.com/seanbrant/django-project-skeleton)
- https://github.com/caktus/django-project-template
- https://gist.github.com/3266518
- http://www.12factor.net
- https://newrelic.com/docs/python/django-on-heroku-quick-start
- https://newrelic.com/docs/python/python-agent-and-heroku
- https://newrelic.com/docs/python/python-agent-and-gunicorn
- https://github.com/chrisfranklin/django-project-skel
- http://kencochrane.net/blog/2011/11/developers-guide-for-running-django-apps-on-heroku/


