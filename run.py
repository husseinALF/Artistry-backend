from app.app import create_app
from app.config.db import db

app = create_app()

with app.app_context():
    db.init_app(app)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True) 