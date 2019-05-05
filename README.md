# Flask API

### Simple store with items and CRUD operation on it.

### Also there is JWT Extented Authentication with token refresh

[Live Demo](https://rudra-store-flask-rest-api.herokuapp.com/)

```
Endpoint            Methods                 Rule
------------        ----------------------  -----------------------
confirmationbyuser  GET, POST               /confirmation/user/<int:user_id>
emailconfirmation   GET                     /confirmation/<string:confirmation_id>
items               DELETE, GET, POST, PUT  /item/<string:name>
itemslist           GET                     /items
phoneconfirmation   POST                    /verify-phone/<string:otp>
phoneotp            POST                    /send-otp
static              GET                     /static/<path:filename>
storelist           GET                     /stores
stores              DELETE, GET, POST       /store/<string:name>
tokenrefresh        POST                    /refresh
user                DELETE, GET, POST       /users/<int:user_id>
userlogin           POST                    /login
userlogout          POST                    /logout
userregister        POST                    /register
```

---

Find documentation [here](https://documenter.getpostman.com/view/6774879/S11KRJsR#3da35eb7-6d05-4159-aa20-109584b84375)
