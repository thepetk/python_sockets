# Pyhon Sockets Project
Simple mechanism which parses socket's data and saves it to db.

## Requirements
For sockets project you will need docker to run a container.

## Pre Installation Notes

* Create a root project folder and get inside. On linux:
```
mkdir your_folders_name
cd your_folders_name
```
* Clone project's source code from gihubb.

### Installation

* Create database on PostgreSQL:
```
>>> CREATE DATABASE sockets_db;
```
* Create venv on project folder and install requirements:
```
$ python3 -m venv venv
$ pip3 install -r requirements.txt
```
* Run necessary db migrations;
```
$ flask db init
$ flask db migrate
$ flask db upgrade
```

* Now you can run project via uwsgi or via docker container.

## Usage

Make command comes with a useful "default" command which explains every available command:
```
Python sockets make commands
----------------------------
Commands available:
    make run		# Starts a Flask development server with local variables.
	
run:
	flask run
```

## Contributing

Pull requests are welcome. Feel free to take this code for your own project.

## Troubleshooting

For any problems please open an issue to my repo.

May the force be with you,
### Theofanis A. Petkos, Software Engineer.