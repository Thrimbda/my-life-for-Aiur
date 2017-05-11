# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-10 13:41:28
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 11:33:58
from flask import Flask
from flask_script import Manager
from flask.ext.restful import Api
from .resource.crystal import Crystal
from .resource.pylon import Pylon
from .resource.spear_of_Adun import SpearOfAdun
from .resource.zealot import Zealot


app = Flask(__name__)
app.secret_key = b'\xfd\xf0\xd3\x9e\xa0\xa5\xfb\x8e\xf9.!\xd8,(j`M\x9d\xc5%\xbf\x1b\xd0L'
manager = Manager(app)
api = Api(app)


api.add_resource(Crystal, '/crystal')
api.add_resource(Pylon, '/pylon')
api.add_resource(SpearOfAdun, '/', '/SpearOfAdun')
api.add_resource(Zealot, '/zealot')


if __name__ == '__main__':
    manager.run()
