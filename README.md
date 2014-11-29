The backend of hplayer app, mainly focus on crawling useful data from some websites, saving them into local postgres and serving the mobile app.

## Features
 * Powered by Django on EC2 and Postgres
 * Crawl the video, audio and cartoon urls, pictures and names
 * Save the crawled data to postgres for later usage
 * Provide rest form api for retrieve and query data by mobile clients

## Quick Setup

#### 1. Create virtual environment

 * Upload the project to EC2 machine
 * Install virtualenv: sudo apt-get install python-virtualenv
 * Go to the project root directory and type: virtualenv env
 * Switch to the created virtual environment: source env/bin/activate

#### 2. Install postgres

 * Follow the postgres install and configuration part in this tutorial: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn
 * Then upgrade your user to be a superuser: ALTER USER myuser WITH SUPERUSER;
 * Create the 'hplayerdb' database: psql -U YOURUSERNAME template1 -c "CREATE DATABASE hplayerdb;"
 * Open your django project settings.py and modify the 'DATABASES' part.

 **NOTE:** Your created user must be a superuser to create a database. If something doesn't work, make sure the 'HOST' in the 'DATABASES' is populated with '127.0.0.1'.

#### 3. Install dependent libraries

 * Intall from the requirements.txt file: pip install -r requirements.txt
 * Go to django-separatedvaluesfield folder and type: python setup.py install
 * Swtich back to the project root folder and type: pythocdn manager.py makemigrations
 * Run the migrations: python manager.py migrate media

#### 4. Start the server locally
 * Start the server locally: python manager.py runserver
 
 #### 5. Start the server on EC2
 * Make sure apache2 is installed
 * Follow the apache part in this tutorial: https://www.digitalocean.com/community/tutorials/how-to-run-django-with-mod_wsgi-and-apache-with-a-virtualenv-python-environment-on-a-debian-vps
 * Start the server: sudo service apache2 restart



