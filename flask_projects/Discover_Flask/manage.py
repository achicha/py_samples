import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from project import app, db

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


@manager.command
def test():
    """Runs the tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='project/*', omit='*/__init__.py')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'coverage')
    cov.html_report(directory=covdir)
    cov.erase()

if __name__ == '__main__':
    manager.run()
