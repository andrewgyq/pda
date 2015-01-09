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
git add .

git commit -m "information"

git push -u origin master

-------------------------------------------------
django deployment：
sudo apt-get remove --purge apache2 apache2-utils
sudo apt-get install apache2

sudo apt-get install libapache2-mod-wsgi
sudo django-admin.py startproject pda

sudo /etc/init.d/apache2 restart

sys.path.append(r'/home/ubuntu/pda')

apache2.conf
LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so
WSGIScriptAlias / /home/ubuntu/pda/pda/wsgi.py
WSGIPythonPath /home/ubuntu/pda
<Directory /home/ubuntu/pda/pda>
<Files wsgi.py>
Require all granted
</Files>
</Directory>





