# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 10:53:57
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 11:55:47
from flask.ext.restful import Resource, reqparse
from flask import session
from src.common.util import abortIfSubjectUnauthenticated
from src.common.util import abortInvalideSubject
from src.common.util import abortInvalideRole
from src.common.util import checkRole
from src.common.util import checkPermission
from src.common.subject_role import subject_role
from src.common.role_permission import role_permission
from src.common.nexus import nexus


class SpearOfAdun(Resource):

    def __init__(self):
        self.putparser = reqparse.RequestParser()
        self.putparser.add_argument('subject',
                                    type=str,
                                    location='json')
        self.putparser.add_argument('role',
                                    type=str,
                                    location='json')
        super(SpearOfAdun, self).__init__()

    def get(self):
        permission = 'get_status'
        abortIfSubjectUnauthenticated(session)
        checkRole(session['subject'], session['role'], subject_role)
        checkPermission(session['role'], permission, role_permission)
        return nexus.getStatus(session['role']), 200

    def post(self):
        args = self.putparser.parse_args()
        if args['subject'] is not None:
            abortInvalideSubject(args['subject'])
        if args['role'] is not None:
            abortInvalideRole(args['role'])
        session['subject'] = args['subject']
        session['role'] = args['role']
        return {'message': 'login as %s using %s' % (session['subject'], session['role'])}, 201

    def put(self):
        args = self.putparser.parse_args()
        if args['role'] is not None:
            abortInvalideRole(args['role'])
        session['role'] = args['role']
        return {'message': 'you-%s change role to %s' % (session.subject, session.role)}, 200

    def delete(self):
        abortIfSubjectUnauthenticated(session)
        session.pop('subject')
        session.pop('role')
        return '', 204
