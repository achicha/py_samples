from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

"""
how to use migrations:
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
"""

app.config.from_object('config.DevConfig')
migrate = Migrate(app, db)  # create migration instance
manager = Manager(app)      # create Manager instance

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
