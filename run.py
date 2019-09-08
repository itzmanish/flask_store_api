from core import db
from server import app

db.init_app(app)

# Another solution can be importing whole db file instead of db module from db file.
# But this one is also good way to achieve functionality.


@app.before_first_request
def create_table():
    db.create_all()
