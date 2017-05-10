# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-10 13:41:28
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 01:15:30
from flask import Flask
from flask_script import Manager
from flask.ext.restful import Api
from common.nexus import Nexus


app = Flask(__name__)
app.secret_key = b'\xfd\xf0\xd3\x9e\xa0\xa5\xfb\x8e\xf9.!\xd8,(j`M\x9d\xc5%\xbf\x1b\xd0L'
manager = Manager(app)
api = Api(app)
nexus = Nexus()
