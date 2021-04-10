![Logo](https://i.ibb.co/C23m7NR/Logo-Makr-2jjctm.png)

**NewsFeed**, A user friendly, personalized news feed portal

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
Set admin by createsuperuser
```
(venv) x@x:~/newsfeed/newsfeed_portal$ python manage.py createsuperuser
```
Provide your preffered username, email, password, confirm password

Then run the server locally by runserver command
```
(venv) x@x:~/newsfeed/newsfeed_portal$ python manage.py runserver
```
If static files didn't loaded properly use collectstatic
```
(venv) x@x:~/newsfeed/newsfeed_portal$ python manage.py collectstatic
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

**REST API Documentation**
**Instruction for generating SHA-256 Signature for all the REST APIs**
- Go to the directory where hash.py file exists. 
- Run the hash.py with the following command and get timestamp and signature key in output
```
(venv) x@x:~/newsfeed/newsfeed_portal/portal$ python hash.py
TIMESTAMP: 1618077886
KEY: c29319231fb11edb337aac86507d790d0c9e8b9d0d32e68d9eddb19757f88a12
```
- You can use the timestamp and signature key until the key expiration time. 
- Once the expiration time is over the signature will be expired and you have to generate another signature key.


**Sample input for ReadListDelete API**
```
{
    "readlist_id":8,
    "timestamp":"1618070826",
    "key":"959ba765383746581e54cedbe7050cecc06e8301ccc771229b3c4897d454a0b9"
}
```
command to acces the API with curl:
```
curl -d 'readlist_id=9&timestamp=1618070826&key=959ba765383746581e54cedbe7050cecc06e8301ccc771229b3c4897d454a0b9' http://localhost:8000/readListDelete
```
Success Response:
```
{
    "status":1,
    "result":["ReadList item successfully Deleted!!"]
}
```
Failure Response:
1. readlist_id failure
```
{
    "status":0,
    "result":["readlist_id doesn't exist"]
}
```
2. timestamp or signature key failure
```
{
    "status":0,
    "result":["Authentication Failure"]
}
```
3. Signature Expired
```
{
    "status":0,
    "result":["Signature Expired"]
}
```






