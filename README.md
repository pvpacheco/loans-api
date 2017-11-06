# Loans API Code Challenge
This is an RESTful API through which a big bank can easily issue new loans and find out what the value and volume of outstanding debt are.

## Main Technologies:
Python 3, Flask-RESTful, SQLite 3, TDD

## Documentation:
https://documenter.getpostman.com/view/3076044/loans-api/77h6P84

## Deploy on Heroku:
https://obscure-castle-95284.herokuapp.com/loans

## Getting Started:
You can use above heroku deploy url and follow postman's documentation or run the server in your own enviroment. To do that, follow the instructions bellow:

<pre>
1. if not already available, install pipenv:
    brew install pipenv

2. install dependencies
    pipenv install

3. activate project's enviroment:
    pipenv shell

2. run api on http://127.0.0.1:8080:
    pipenv run waitress-serve app.main:app
</pre>

## Runing tests file
<pre>
1. simply run:
    nosetests
</pre>
