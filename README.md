# Binomi

The hassle that comes with looking for a Room-mate is a situation that many people can relate to.
You want to find a Room-mate with whom you can get along with, and it's a difficult process to find one.

Binomi is working on solving this problem. It is a platform that connects people that are looking for a roommate based on their preferences.



## Built With
- Flask
- Python3
- CSS
- HTML
- JQUERY
- MySQL
## Getting Started
### Prerequisites
Installing Python3
```bash
  sudo apt install python3
```
Installing Flask and other related libraries 
```bash
  sudo pip install -U Flask

  sudo pip install flask-login

  git clone https://github.com/wtforms/flask-wtf
  sudo pip install -e ./flask-wtf

  sudo pip install flask_uploads

```

Installing Werkzeug
```bash
  sudo pip install -U Werkzeug
```
Installing JQUERY
```bash
  sudo npm install jquery
```
Installing MySQL
```bash
  sudo apt install mysql-server
  sudo mysql_secure_installation
```

### Deploymment
First create the user and the database.
```bash
  sudo mysql -uroot -p < ./setup_mysql_dev.sql
```
Create the tables in the database.
```bash
 echo quit | BINOMI_MYSQL_USER=binomi_dev BINOMI_MYSQL_PWD=binomi_dev_pwd BINOMI_MYSQL_HOST=localhost BINOMI_MYSQL_DB=binomi_dev_db BINOMI_TYPE_STORAGE=db ./console.py
```
Enable the APIs
```bash
  BINOMI_MYSQL_USER=binomi_dev BINOMI_MYSQL_PWD=binomi_dev_pwd BINOMI_MYSQL_HOST=localhost BINOMI_MYSQL_DB=binomi_dev_db BINOMI_TYPE_STORAGE=db python3 -m api.v1.app
```
Execute the Flask app "Binomi" and access the website through the url given after executing the following command.
```bash
  BINOMI_MYSQL_USER=binomi_dev BINOMI_MYSQL_PWD=binomi_dev_pwd BINOMI_MYSQL_HOST=localhost BINOMI_MYSQL_DB=binomi_dev_db BINOMI_TYPE_STORAGE=db python3 -m web_dynamic.binomi
```

### Usage

The website contains profiles of people who are looking for roOmmates, you can navigate the website looking for roomMates without creating an account.

You have to create an account to post your profile.

Account Creation
![login](https://i.imgur.com/FchvvDq.png)

Create a profile
![profile](https://i.imgur.com/PQEiqfp.png)

Browsing profiles filtered by location
![browsing](https://i.imgur.com/4Lqgeoq.png)



## Authors

- [@yousseffabid](https://github.com/yousseffabid)
- [@youssefjell](https://github.com/YoussefJell)
- [@Akram Jerbi](https://github.com/Aleph235)
