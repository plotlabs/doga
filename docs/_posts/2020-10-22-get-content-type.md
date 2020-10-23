---
category: Admin Endpoints
url_path: '/admin/content/types'
title: 'Get content types'
type: 'GET'

layout: null
---

This method allows the user to get information about the content available, i.e 
all the content that has been posted or created using doga is sent listed before
the user.

### Request

* The headers can include a **valid authentication token**.
* **The body is omitted**.

### Response

Sends back a collection of things.

```Status: 200 :```
```{
    code: 200,
    message: '[     "type": "array",
    "items": [
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
              },]'
}```

For errors responses, see the [response status codes documentation](#response-status-codes).
