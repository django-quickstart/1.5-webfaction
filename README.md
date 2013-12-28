1.5-webfaction
==============

Opinionated django project skeleton with recipe/script for rapid deployment to webfaction. Django version:1.5. Server: Apache/Mod_WSGI. Assets: Webfaction nginx. Frontend: Bootstrap 2.x. DB: Webfaction Postgres. Secrets stored in environment variable.  Uses virtualenv.  Python version 2.x



# Django 1.4 & 1.5 project template for fast Webfaction deployment
<!-- Uncomment this in your real project (and delete )
# {{ project_name|title }} Django Project

From [Django 1.4 project template for fast webfaction deployment](https://github.com/django-quickstart/1.5-webfaction)
 -->


## About

This is a template for starting Django 1.4 projects and rapidly deploying to webfaction.  It is opinionated and configured for the things that I like and repetitively end up adding before deployment.  It works with 1.5 but has not been thoroughly tested with 1.5.   

While this quickstart is what I use personally, it is not promised to be complete or bug free.


## Skel Template Features ##
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
- python2 >= 2.7, pip, virtualenv, git, autoenv


### First time system config/installation stuff.

``` bash
easy_install pip
pip install virtualenv, virtualenvwrapper, autoenv
brew install postgresql
```

###Creating utility aliases
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
### First time setups steps
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
foreman run python manage.py validate
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
foreman run python manage.py syncdb && foreman run python manage.py migrate
``` 

Collect static
``` bash
foreman run python manage.py collectstatic --noinput
```

Run Tests
``` bash
foreman run python manage.py test
```

Fire up local/dev server
``` bash
foreman start
#... or ...
foreman run python manage.py runserver 0.0.0.0:8000
``` 



## Deploying
### Preparing for first deploy
Create git repo
``` bash
git init
... 
Initialized empty Git repository in ...
...
git add .
git commit -m "initial commit"
```

Create heroku app
``` bash
heroku create [appname]
```

Add addons: sendgrid for email and postgress for database
``` bash
heroku addons:add sendgrid:starter
heroku addons:add heroku-postgresql:dev
heroku addons:add pgbackups:auto-month
heroku addons:add newrelic:standard
heroku addons:add scheduler:standard
```

Promote database to DATABASE_URL
``` bash
heroku config
...
HEROKU_POSTGRESQL_[color]_URL: postgress://x:y@z.com:XXXX/ABCDEFGHIJ
...
heroku pg:promote HEROKU_POSTGRESQL_[color]
``` 

Configure Environment Variables
``` bash
heroku config:set DJANGO_ENV="PRODUCTION" DJANGO_DEBUG="false" 
heroku config:set AWS_ACCESS_KEY_ID=[KEY] AWS_SECRET_ACCESS_KEY=[KEY] 
```


### Regular Deploy Script
Run All Tests
``` bash
foreman run python manage.py test
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
git push heroku master
```

Sync and migrate the remote DB
``` bash
heroku run python manage.py syncdb && heroku run python manage.py migrate
```

Collect remote static
If you haven't configured AWS correctly, this is going to break loudly
``` bash
heroku run python manage.py collectstatic --noinput
```

Go see your site in action
``` bash
heroku open
heroku logs --tail
```

That's it, you're configured and deployed.  Now go build something awesome.


## Housekeeping
- Login to admin and set site, so emails don't come from example.com

### Getting custom domain set up
https://devcenter.heroku.com/articles/custom-domains
https://devcenter.heroku.com/articles/avoiding-naked-domains-dns-arecords

If you set up one of heroku's [adjective]-[item]-[number] app names, rename to your domain
``` bash
heroku apps:rename [domain]
```
Note that if you change this via the website you'll have to move around the git remotes and do a checkout: https://devcenter.heroku.com/articles/renaming-apps


Add the domain
``` bash
heroku domains:add www.[domain].com
```

Setup CNAME for www to [appname].herokuapp.com
Setup forwarding for naked domain to www.[domain].com

Wait ~15-60 minutes

Alternatively, the zerigo DNS app is another way to set this up that may be preferred.


# Options, considerations, and commands worth discussing
## Deploying
### Procfile settings

Dev only runserver.
``` 
web: python manage.py runserver "0.0.0.0:$PORT"
``` 

Standard #1: production setup gunicorn server
``` 
python manage.py run_gunicorn 0.0.0.0:$PORT -w 3
``` 

Standard #2: newrelic and gunicorn  **Recommended starting setup**
https://newrelic.com/docs/python/django-on-heroku-quick-start
``` 
web: newrelic-admin run-program python manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3
``` 

Standard #3: newrelic, gunicorn, and celery scheduler/worker
https://newrelic.com/docs/python/django-on-heroku-quick-start
Note: This setup doesn't include celerybeat, instead use the heroku scheduler.  
``` 
web: newrelic-admin run-program python manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3
# worker: newrelic-admin run-program python manage.py celeryd -E --loglevel=INFO
``` 



NB: The following Advanced setups use gevent to process requests asynchronously.  This can yield substantial performance improvements, but can also make debugging substantially more complicated.  They also include both a celery scheduler and worker -- there should never be more than one scheduler instance.  I have not used or confirmed that these settings work -- they are here for reference.

Advanced, with newrelic, gunicorn, gevent, and celery worker
from https://github.com/seanbrant/django-project-skeleton
``` 
web: newrelic-admin run-program gunicorn [project_name].wsgi -w 4 -b 0.0.0.0:$PORT -k gevent --max-requests 250
# scheduler: newrelic-admin run-program python manage.py celeryd -B -E --loglevel=INFO
# worker: newrelic-admin run-program python manage.py celeryd -E --loglevel=INFO
``` 


Advanced with newrelic, gunicorn, gevent, celery scheduler and worker
https://github.com/rdegges/django-skel/
``` 
web: newrelic-admin run-program gunicorn -c gunicorn.py.ini wsgi:application
# scheduler: python manage.py celery worker -B -E --maxtasksperchild=1000
# worker: python manage.py celery worker -E --maxtasksperchild=1000
``` 




## Working Locally
### Option 1: ENV Variables and vanilla manage.py - Not recommended
Set DEV environment variables, use standard django runserver command
``` bash
export DJANGO_DEBUG=True
export DJANGO_ENV=DEV

python manage.py runserver 0.0.0.0:8000
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
foreman run python manage.py runserver 0.0.0.0:8000
``` 

### Option 3: VirtualenvWrapper PostActivate
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

Checking for later versions fo packages
``` bash
pip freeze | cut -d = -f 1 | xargs -n 1 pip search | grep -B2 'LATEST:'
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
Adding a db to your plan
``` bash
heroku addons:add heroku-postgresql:dev
```

Getting info on your dbs
``` bash
heroku pg:info
``` 

Promoting a db to DATABASE_URL
``` bash
heroku config
...
HEROKU_POSTGRESQL_[color]_URL: postgress://x:y@z.com:XXXX/ABCDEFGHIJ
...
heroku pg:promote HEROKU_POSTGRESQL_[color]_URL
heroku config
...
HEROKU_POSTGRESQL_[color]_URL: postgress://x:y@z.com:XXXX/ABCDEFGHIJ
DATABASE_URL:                  postgress://x:y@z.com:XXXX/ABCDEFGHIJ
...
```




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
Seeing environment variables on heroku
``` bash
heroku config
```

Setting an environment variable on heroku
``` bash
heroku config:add DJANGO_ENV=PRODUCTION
```

Deleting an environment variable on heroku
``` bash
heroku config:remove DJANGO_ENV
```


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
2) Unused packages take server space
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


