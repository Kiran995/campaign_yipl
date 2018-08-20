# SMS Campaign
This is an application that sends outbound messages to the phones. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development. 

## Prerequisites
- python3
- Kannel

## Installing
- Clone the repository  
`git clone git@github.com:Kiran995/campaign_yipl.git`

- Setup the pip package manager  
`apt install python3-pip`

- Install virtual environment package  
`pip install virtualenv`

- Create virtual environment (Campaign is the path where you are creating the virtual environment)  
`virtualenv Campaign`

- Activate virtual environment  
`source Campaign/bin/activate`
	
- Install from the requirements file  
`pip install -r requirements.txt`

- Create a database migration repository
`flask db init`

- Generate an initial migration
`flask db migrate`

- Then apply migration to the database
`flask db upgrade`
	
## Running the project
`python workers.py`  
`python app.py runserver d`

## Built With
- [Flask](http://flask.pocoo.org/) - Microframework for python
- [Postgresql](https://www.postgresql.org/) - Open source object-relational database system 
- [Kannel](https://www.kannel.org/) - Open source SMS gateway


