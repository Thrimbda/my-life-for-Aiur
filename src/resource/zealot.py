# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 01:46:30
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 01:46:47
from flask.ext.restful import Resource, reqparse


class Zealot(Resource):

    def __init__(self):
        self.putparser = reqparse.RequestParser()
        self.putparser.add_argument('amount',
                                    type=int,
                                    default=1,
                                    location='json')
        super(Zealot, self).__init__()

    def get(self):
        pass

    def put(self):
        pass
