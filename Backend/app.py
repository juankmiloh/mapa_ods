#!/usr/bin/env python
import os
from src import create_app
from flask_script import Manager

app = create_app()
manager = Manager(app)

@manager.command
def test():
    from subprocess import call

    os.environ['FLASK_CONFIG'] = 'testing'
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=app', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])

if __name__ == '__main__':
    if app.config.get("ENV") == 'development':
        app.run()
    else:
        manager.run()