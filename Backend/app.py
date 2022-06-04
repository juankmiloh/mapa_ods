#!/usr/bin/env python
import os
from src import create_app
from flask import render_template, redirect, url_for
from flask_script import Manager

app = create_app()
manager = Manager(app)

@app.errorhandler(404)
def page_not_found(e):
    print("--------- ERROR ---------------------------")
    print(e)
    print("------------------------------------")
    return render_template('404.html'), 404

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