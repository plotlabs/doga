---
category: Content Endpoints
url_path: '/"db_name"/"content"'
title: 'Get content'
type: 'GET'

layout: null
---

This method allows the user to get information about the a particular content 
object created by the user.

### Request

* The headers can include a **valid authentication token**.
* **The body is omitted**.

### Response

Sends back a collection of things.

```Status: 200 Content Found```
```{
    code: 200,
    message: '[     "type": "array",
    "items":
      {
        "type": "object",
        "properties": {
          "columns": {
            "type": "array",
            "items": [
              {
                "type": "object",
                "properties": {
                  "default": {
                    "type": "string"
                  },
                  "foreign_key": {
                    "type": "string"
                  },
                  "name": {
                    "type": "string"
                  },
                  "nullable": {
                    "type": "string"
                  },
                  "type": {
                    "type": "string"
                  },
                  "unique": {
                    "type": "string"
                  }
                },
                "required": [
                  "default",
                  "foreign_key",
                  "name",
                  "nullable",
                  "type",
                  "unique"
                ]
              }'
}```

For errors responses, see the [response status codes documentation](#response-status-codes).
