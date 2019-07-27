# Doga

A headless CMS created in Flask.


# Files

StackEdit stores your files in your browser, which means all your files are automatically saved locally and are accessible **offline!**

## Pre-requisites

The python packages required to run the app are given in the requirements.txt file and can be installed using the command:

    pip install -r requirements.txt

## Execution

The app can be started using the command:

    python runserver.py
 
 By default the app will run on 0.0.0.0:8080.
 This can be edited in the **runserver.py** file.

## Databases
The default database is SQLite. A default sqlite file named **test.db** is created in the **/tmp** folder in the system.

## Admin APIs

The following APIs are available for creating and managing content types and databases:

 1. Get all content types
 Endpoint- /admin/content/types
 Method- GET
	
 2. Create/Edit content type
Endpoint- /admin/content/types
 Method- POST(Create), PUT(Edit)
 Request JSON:
 ```
	data = {
		"table_name": "table_name",
		"connection_name": "user defined connection name",
		"columns": [
			{
				"name": "column_name",
				"type": "column_type",
				"nullable": "True/False",
				"unique": "True/False", 
				"foreign_key": "foreign key table name"
			},
			{}.....
		]
	}
```
 3. Delete content type
Endpoint- /admin/content/types/content_type_name
 Method- DELETE
 
 4. Add new DB connection
 Endpoint- /admin/dbinit/
 Method: POST
 Request JSON:
 ```
	{
			"type": "mysql/postgres",
			"connection_name": "custom_connection_name",
			"username": "",
			"password": "",
			"host": "",
			"database_name": ""
	}
```

## User APIs

The CRUD APIs for the content types added by the user are automatically created with the following endpoints:

 1. GET - /table_name/, /table_name/id
 2. POST - /table_name
 3. PUT - /table_name/id
 4. DELETE - table_name/id

