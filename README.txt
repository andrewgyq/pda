install:
python 2.7
mongodb 
-------------------------------------------------
dependencies:
sudo pip install django
sudo pip install pymongo
sudo pip install oauth2
sudo pip install nltk
sudo python -m nltk.downloader -d /usr/share/nltk_data all
sudo pip install requests
sudo pip install numpy
sudo pip install lda

sudo apt-get install python-dev
sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev
sudo apt-get install libxml2-dev libxslt-dev
sudo pip install image
sudo pip install newspaper
------------------------------------------------
create：
django-admin.py startproject pda

python manage.py migrate

python manage.py runserver

------------------------------------------------
mongodb：
mongodb dbpath  
	/var/lib/mongodb

backup mongodb 
	mongodump -h 127.0.0.1 -d weibo

Error couldn't connect to server
	sudo rm -rf /var/lib/mongodb/mongod.lock
	sudo service mongodb restart
--------------------------------------------------
github：

sudo apt-get git

git config --global user.name "andrewgyq"
git config --global user.email "514362283@qq.com"

git init
git add .
git commit -m "first commit"
git remote add origin https://github.com/andrewgyq/pda.git
git push -u origin master


git add .
git commit -m "information"
git push -u origin master

-------------------------------------------------
django deployment：

sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi

/etc/apache2/apache2.conf
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
WSGIScriptAlias / /home/ubuntu/pda/pda/wsgi.py
WSGIPythonPath /home/ubuntu/pda
<Directory /home/ubuntu/pda/pda>
<Files wsgi.py>
Require all granted
</Files>
</Directory>

sudo /etc/init.d/apache2 restart





