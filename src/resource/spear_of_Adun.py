# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 10:53:57
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 10:58:37
from flask.ext.restful import Resource, reqparse
from flask import session
from src.common.util import abortIfSubjectUnauthenticated, checkRole, checkPermission
from src.common.subject_role import subject_role
from src.common.role_permission import role_permission
from src.API import nexus


class SpearOfAdun(Resource):

    def __init__(self):
        self.putparser = reqparse.RequestParser()
        self.putparser.add_argument('for_aiur',
                                    type=bool,
                                    default=False,
                                    location='json')
        self.putparser.add_argument('subject',
                                    type=str,
                                    location='json')
        self.putparser.add_argument('role',
                                    type=str,
                                    location='json')
        super(SpearOfAdun, self).__init__()

    def get(self):
        pass

    def post(self):
        pass
