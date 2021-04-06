![Logo](https://i.ibb.co/C23m7NR/Logo-Makr-2jjctm.png)

**NewsFeed**


A user friendly, personalized news feed portal

- This is a personalized news feed portal fetches news with NewsAPI 
- A personalized feed is included for user modification 
- Used Sendgrid for sending emails 
- For mobile access, some APIs are exposed

**Setting Up**


OS: Ubuntu 18.04 LTS

At first, clone the project from terminal by renaming the folder(e.g. newsfeed) 
```
$ git clone https://gitlab.com/aqifcse/newsfeed.git
```
enter the project directory
```
$ cd newsfeed 
```
Setup virtualenv in your machine with Python 3.6.9 and create a virtual environment with in the project directorey
```
~/newsfeed$ virtualenv venv
```

activate the virtual environment
```
~/newsfeed$ source venv/bin/activate
```
Create a .env file
```
(venv) x@x:~/newsfeed$ vi .env
```
paste the following values in .env
```
EMAIL_USER=<your aws email smtp server userid>
EMAIL_HOST_PASSWORD=<your aws email smtp server host password>
```
Save the file and install all the packages from requirements.txt file using pip
```
(venv) x@x:~/newsfeed$ pip install -r requirements.txt
```
Go to project directory where manage.py exist and hit the makemigrations (Only for sqlite3) command
```
(venv) x@x:~/newsfeed$ cd newsfeed_portal/
(venv) x@x:~/newsfeed/newsfeed_portal$ python manage.py makemigrations
```
Then hit the migrate command for database migrations(both for sqlite3 and mysql)
```
(venv) x@x:~/newsfeed/newsfeed_portal$ python manage.py migrate
```
Then run the server locally by runserver command
```
(venv) x@x:~/newsfeed/newsfeed_portal$ python manage.py runserver
```
By default, the server will run in 8000 port. If you want to run the server to a different port (e.g 8080 port), then the command will be 
```
(venv) x@x:~/newsfeed/newsfeed_portal$ python manage.py runserver 8080
```
If you want to launch it from a aws-ec2 instance and make the project live the type following command adding runserver command with ip:port
```
(venv) x@x:~/newsfeed/newsfeed_portal$ python manage.py 0.0.0.0:8000&
```
Adding a '&' after port will make the server running after Ctrl+L and exit command in the terminal.
You can kill the process running on a specific port by the following command -
```
(venv) x@x:~/newsfeed/newsfeed_portal$ ps aux | grep -i manage
```
kill the running processes on a specific ip:port or port by kill command after getting the pid from the above command. For example, if the pid is 31626 the the command will look like
```
(venv) x@x:~/newsfeed/newsfeed_portal$ kill -9 31626
```

Done!!!!!






