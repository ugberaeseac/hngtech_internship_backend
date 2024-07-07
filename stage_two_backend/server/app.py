#!/usr/bin/python3
"""
create the app instance
"""


from server import app, db
from server.views import app_views


#with app.app_context():
#    db.create_all()


app.register_blueprint(app_views)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(host='0.0.0.0', port=5000, debug=True)
