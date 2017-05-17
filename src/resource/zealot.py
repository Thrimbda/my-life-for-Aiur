# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 01:46:30
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 15:36:37
from flask.ext.restful import Resource, reqparse
from flask import session
from src.common.util import abortIfSubjectUnauthenticated, checkPermission
from src.common.role_permission import role_permission
from src.common.nexus import nexus


class Zealot(Resource):

    def __init__(self):
        self.putparser = reqparse.RequestParser()
        self.putparser.add_argument('amount',
                                    type=int,
                                    default=1,
                                    location='json')
        super(Zealot, self).__init__()

    def get(self):
        permission = 'get_status'
        abortIfSubjectUnauthenticated(session)
        checkPermission(session['role'], permission, role_permission)
        return {'message': 'you have %d zealot warriors' % nexus.zealot}, 200

    def put(self):
        permission = 'transport_zealot'
        abortIfSubjectUnauthenticated(session)
        checkPermission(session['role'], permission, role_permission)
        args = self.putparser.parse_args()
        amount = nexus.transport(args['amount'])
        return {'message': 'transport %d zealot warriors, En Taro Tassadar!' % amount}, 200


class ForAiur(Resource):

    def __init__(self):
        self.putparser = reqparse.RequestParser()
        self.putparser.add_argument('for_aiur',
                                    type=bool,
                                    default=False,
                                    location='json')
        super(ForAiur, self).__init__()

    def get(self):
        permission = 'scout'
        abortIfSubjectUnauthenticated(session)
        checkPermission(session['role'], permission, role_permission)
        return {'message': "to defeat Amond, you'll need %d zealot!" % (nexus._amond)}, 200

    def post(self):
        permission = 'for_aiur'
        abortIfSubjectUnauthenticated(session)
        checkPermission(session['role'], permission, role_permission)
        args = self.putparser.parse_args()
        message = None
        if args['for_aiur']:
            if nexus.forAiur():
                message = 'Khassar de templari! Congratulations!'
            else:
                message = 'You failed.'

        else:
            message = "you'd better transport more zealot!"
        return {'message': message}, 200
