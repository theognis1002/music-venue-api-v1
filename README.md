# flask_venue_api
Custom Restful API built using Flask/Python - powered by a SQL database consisting of over 1300+ music and sports venues. The api can be quered to retrieve the venue name, capacity, city, state, etc. or to add new venues.

![Alt text](/static/APIDocumentation.JPG?raw=true "API documentation")
## Endpoints:

### Route: "/"

* Content-Type: application/json

* Description: index

* Method(s): ['GET']

### Route: "/venue/v1"

* Content-Type: application/json

* Description: get venue

* Method(s): ['GET']

### Route: "/venue/v1/add"

* Content-Type: application/json

* Description: add venue

* Method(s): ['POST']
