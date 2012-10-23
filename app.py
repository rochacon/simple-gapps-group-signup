# coding: utf-8
import os

from flask import Flask, jsonify, render_template, request
from gdata.apps.groups.client import GroupsProvisioningClient


app = Flask(__name__)
app.config.from_object('settings')

GAPPS_DOMAIN = app.config['GAPPS_DOMAIN']
GAPPS_USER =  app.config['GAPPS_USER']
GAPPS_PASS =  app.config['GAPPS_PASS']
GAPPS_GROUP = app.config['GAPPS_GROUP']

if not GAPPS_USER or not GAPPS_PASS or not GAPPS_GROUP:
    raise RuntimeError(u'You need to set the GAPPS_USER, GAPPS_PASS and GAPPS_GROUP environment variables')


@app.route('/')
def index():
    return render_template('index.html', GAPPS_DOMAIN=GAPPS_DOMAIN, GAPPS_GROUP=GAPPS_GROUP)


@app.route('/register', methods=('POST',))
def register():
    username = request.form.get('username')
    if username is None or len(request.form['username']) < 1:
        return jsonify(status=1, message='Please, type in your username')

    api = GroupsProvisioningClient(domain=GAPPS_DOMAIN)
    api.ClientLogin(email='%s@%s' % (GAPPS_USER, GAPPS_DOMAIN), password=GAPPS_PASS, source='apps')
    api.AddMemberToGroup(GAPPS_GROUP, username)
    return jsonify(status=0, message='Done!')


if __name__ == '__main__':
    app.run()
