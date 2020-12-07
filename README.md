# [Doga](https://plotlabs.github.io/doga/)

**A headless CMS created in Flask.**

## Pre-requisites

The python packages required to run the app are given in the requirements.txt
file and can be installed using the command:

```bash
    pip install -r requirements.txt
```
* on an Ubuntu system you might need to run the following command before you
can install dependencies:

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
This can be edited in the **config.py** file.

## Databases
DOGA allows you to store your content on any to any Postgres, MySQL ad SQLite
database servers, upon specifying their HOST, PORT addresses along with your
login credentials for the same, and adding a connection to the system though
the `admin/dbinit/` endpoint.

Theere is a default connection created in SQLite. A sqlite file named
**test.db** is created in the **/tmp** folder in the system and the a `default`
connection is stored in DOGA to stay connected to it. This database file is
used by DOGA internally to store information about the content created and
admin users. DOGA however, does allow you to store content on the `default`
connection.


## Admin APIs

The following APIs are available to register and login as admin users:

 1. Register Admin Users
	- **Endpoint**
		`/admin/admin_profile`-
	- **Method-** POST(Create)
	- **Request JSON**:
		```json
		data = {
    			"email":"email@webpage.com",
    			"password": "password",
    			"name": "admin_name"
			}
	- **Response**:
		Code 200 : Success
		```json
			{
				"result": "Admin created successfully.",
    			"id": 1,
    			"email": "email@webpage.com"
			}
		```

 2. Login Admin User
	- **Endpoint**
		`/admin/login`
	- **Method-** POST (Login)
		```json
		data = {
    			"email":"email@webpage.com",
   		 		"password": "password"
				}
		```
	- **Response**
		Code 200 : Success
		```json
		{
			    "result": "Successfully logged in.",
    			"email": "email@someemail.com",
    			"name": "admin",
    			"id": 1 ,
    			"access_token": "jwt_token",
    			"refresh_token": "refresh_token"
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
					"default": "value or "" ",
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

	- **Endpoint-** /admin/dbinit/
 	- **Method-** POST
	- **Request JSON**:

	 ```json
		{
				"database_type": "mysql/postgresql",
				"connection_name": "custom_connection_name",
				"username": "",
				"password": "",
				"host": null,
				"port":null,
				"database_name": ""
		}
	```
	for null values of port default connection values are used, these
	can be found in the config file.


**To deploy the APPs created through DOGA**

	- **Endpoint-** /admin/export/<platform>
	- **Method-** POST
	- **Request JSON**

	```json
	{
    "app_name":"string",
    "user_credentials":{
        "aws_username": "string",
        "aws_secret_key":"string",
        "aws_access_key":"string"
    	},
    "config":{
			"region_name": "string" #optional,
			"signature_version":"string"#optional
			 "retries": {
				 "max_attempts":"string",
				 "mode": "string"
				 } #optional
            },
    "rds_config":{
        "Engine":"MySQL/SQLite/Postgres",
        "AllocatedStorage": "integer",
        "DBInstanceIdentifier":"string",
        "DBInstanceClass":"ex.db.t2.micro or instance classes in string",
        "MasterUsername":"string",
        "MasterUserPassword":"string",
        "MaxAllocatedStorage":"integer"
    	},
    "ec2_config":{
        "BlockDeviceMappings":"",
        "InstanceType":"",
        "ImageId":""
    	}
	}
	```
## User APIs

The CRUD APIs for the content types added by the user are automatically created
with the following endpoints:

 1. GET - db_name/table_name/, db_name/table_name/id
 2. POST - db_name/table_name
 3. PUT -db_name/table_name/id
 4. DELETE - db_name/table_name/id
