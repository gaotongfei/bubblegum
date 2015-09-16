from flask import g
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from app import create_app, db
from app.models import User, Post
import flask.ext.whooshalchemy as whooshalchemy
from app.main.forms import SearchForm


app = create_app('deploy')
manager = Manager(app)
migrate = Migrate(app, db)
whooshalchemy.whoosh_index(app, Post)


@app.before_request
def before_request():
    g.search_form = SearchForm()


def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def createdb():
    db.create_all()

if __name__ == '__main__':
    manager.run()
