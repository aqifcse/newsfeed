**NewsFeed**
A user friendly, personalized news feed portal

![Logo](https://i.ibb.co/C23m7NR/Logo-Makr-2jjctm.png)

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

Install all the packages from requirements.txt file using pip
```
(venv) x@x:~/newsfeed$ pip install -r requirements.txt
```




