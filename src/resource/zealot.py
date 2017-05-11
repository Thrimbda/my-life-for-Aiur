# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 01:46:30
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 11:58:29
from flask.ext.restful import Resource, reqparse
from flask import session
from src.common.util import abortIfSubjectUnauthenticated, checkRole, checkPermission
from src.common.subject_role import subject_role
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
        checkRole(session['subject'], session['role'], subject_role)
        checkPermission(session['role'], permission, role_permission)
        return {'message': 'you have %d zealot warriors' % nexus.zealot}, 200

    def put(self):
        permission = 'transport_zealot'
        abortIfSubjectUnauthenticated(session)
        checkRole(session['subject'], session['role'], subject_role)
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

    def post(self):
        permission = 'for_aiur'
        abortIfSubjectUnauthenticated(session)
        checkRole(session['subject'], session['role'], subject_role)
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
