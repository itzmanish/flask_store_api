# Flask API

### Simple store with items and CRUD operation on it.

### Also there is JWT Extented Authentication with token refresh

[Live Demo](https://rudra-store-flask-rest-api.herokuapp.com/)

```
Endpoint      Methods                 Rule
------------  ----------------------  -----------------------
items         DELETE, GET, POST, PUT  /item/<string:name>
itemslist     GET                     /items
storelist     GET                     /stores
stores        DELETE, GET, POST       /store/<string:name>
token refresh POST                    /refresh
user          DELETE, GET, POST       /users/<int:user_id>
user login    POST                    /login
user logout   POST                    /logout
user register POST                    /register
```

---

Find documentation [here](https://documenter.getpostman.com/view/6774879/S11KRJsR#3da35eb7-6d05-4159-aa20-109584b84375)
