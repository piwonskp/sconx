# Sconx
An extension to [connexion](https://github.com/zalando/connexion) that reduces size of requests. Size reduction is achieved by sending objects as lists of the values of their attributes. Under the hood lists are translated to objects similarly to vanilla connexion. 
## Quickstart
Prepare app just like you would do in connexion.
```python
# app.py
from sconx import App

sconx_app = App(__name__,
                options={'serve_spec': True})
app = sconx_app.app

sconx_app.add_api("people.yaml")
```
Prepare OpenAPI specification.
```yaml
# people.yaml
openapi: "3.0.2"
info:
  version: "0.0.1"
  title: Swagger REST Article
components:
  schemas:
    Poeple:
      type: "array"
      items:
        $ref: "#/components/schemas/Person"
    Person:
      type: object
      properties:
          last_name:
            type: "string"
          first_name:
            type: "string"
          email:
            type: "string"
servers:
  - url: "/api/people"
paths:
  /read/jsan:
    get:
      operationId: "people.read_jsan"
      tags:
        - "People"
      responses:
        200:
          description: "Read people list operation"
          content:
            application/jsan:
              schema:
                $ref: "#/components/schemas/Poeple"
```
Handle the request however you like.
```python
# people.py
def read_jsan():
    return [{"last_name": "Blair", "first_name": "Martin", "email": "elliottshelby@sanders.org"}]
```
## Example
Example usage is available at [sconx-example](https://github.com/piwonskp/sconx-example).
