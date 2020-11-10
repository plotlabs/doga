﻿# Doga

**A headless CMS created in Flask.**


# Files

StackEdit stores your files in your browser, which means all your files are automatically saved locally and are accessible **offline!**

## Pre-requisites

The python packages required to run the app are given in the requirements.txt file and can be installed using the command:

```bash
    pip install -r requirements.txt
```
* on an Ubuntu system you might need to run the following command before you can install dependencies:

```bash
	sudo apt-get install python-dev
```

## Execution

The app should be started first using the command:

```bash
	sh start.sh
```
The app can be started using the command:

```bash
	python runserver.py
```
By default the app will run on 0.0.0.0:8080.
This can be edited in the **runserver.py** file.

## Databases
The default database is SQLite. A default sqlite file named **test.db** is
created in the **/tmp** folder in the system.

## Admin APIs

The following APIs are available to register and login as admin users:

 1. Register Admin Users
	**Endpoint**
	`/admin/admin_profile`-
	**Method-** POST(Create)
	**Request JSON**:
		```json
		data = {
    	"email":"email@webpage.com",
    	"password": "password",
    	"name": "admin_name"
		}

 2. Login Admin User
	**Endpoint**
	`/admin/login`
	**Method-** POST (Login)
	```json
	data = {
		{
    "email":"email@webpage.com",
    "password": "password"
	}
	```

The following APIs are available for creating and managing content types and
databases, these are restricted by a **jwt**, the token for the same is
generated when the admin user created, logs-in:

 1. Get all content types
	**Endpoints:**
 	-  /admin/content/types
 	-  /admin/content/types/content_type_name
 	**Method-** GET

 2. Create/Edit content type
	**Endpoint:**
	-   /admin/content/types
	**Method-** POST(Create), PUT(Edit)
	**Request JSON**:

 	```json
		data = {
			"table_name": "table_name",
			"connection_name": "user defined connection name",
			"columns": [
				{
					"name": "column_name",
					"type": "column_type",
					"nullable": "True/False",
					"unique": "True/False",
					"default": "value" or "",
					"foreign_key": "foreign key table name"
				}	,
				{}.....
			]
		}
	```
**Using JWT with content**
**If you want to integrate JWT with the content**

In the Request body-
- Set jwt_required as True
- Set filter_keys as list of columns to use while issuing token
- Set expiry key to set custom expiry time for tokens giving a unit and a value

**Request JSON**:

	```json
			data = {
			"table_name": "table_name",
			"connection_name": "user defined connection name",
			"base_jwt OR restrict_by_jwt": true,
			"filter_keys": ["column_name_1","column_name_2"],
			"expiry": {
				"unit" : "weeks/days/hours/minutes/seconds/microseconds/milliseconds",
				"value" : "integer value"
			}
			"columns": [
				{
					"name": "column_name",
					"type": "column_type",
					"nullable": "True/False",
					"unique": "True/False",
					"default": "value" or "",
					"foreign_key": "foreign key table name"
				},
				{}.....
			]
		}
	}
	```

**If you want to authenticate content APIs using JWT**

In the request body-
- Set jwt_restricted as True

**Request JSON**:

	```json
	data = {
		"table_name": "table_name",
		"connection_name": "user defined connection name",
		"jwt_restricted": true,
		"columns": [
			{
				"name": "column_name",
				"type": "column_type",
				"nullable": "True/False",
				"unique": "True/False",
				"default": "value" or "",
				"foreign_key": "foreign key table name"
			},
			{}.....
		]
	}
	```

 3. Delete content type
	**Endpoint-** /admin/content/types/content_type_name
	**Method-** DELETE

 4. Add new DB connection

	**Endpoint-** /admin/dbinit/
 	**Method-** POST
	**Request JSON**:

	 ```json
		{
				"database_type": "mysql/postgresql",
				"connection_name": "custom_connection_name",
				"username": "",
				"password": "",
				"host": "",
				"database_name": ""
		}
	```

## User APIs

The CRUD APIs for the content types added by the user are automatically created with the following endpoints:

 1. GET - db_name/table_name/, db_name/table_name/id
 2. POST - db_name/table_name
 3. PUT -db_name/table_name/id
 4. DELETE - db_name/table_name/id
