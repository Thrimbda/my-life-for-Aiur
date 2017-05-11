# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 01:04:44
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 11:55:03
from flask.ext.restful import Resource, reqparse
from flask import session
from src.common.util import abortIfSubjectUnauthenticated, checkRole, checkPermission
from src.common.subject_role import subject_role
from src.common.role_permission import role_permission
from src.common.nexus import nexus


class Crystal(Resource):

    def __init__(self):
        self.putparser = reqparse.RequestParser()
        self.putparser.add_argument('amount',
                                    type=int,
                                    default=1000,
                                    location='json')
        super(Crystal, self).__init__()

    def get(self):
        permission = 'crystal_status'
        abortIfSubjectUnauthenticated(session)
        checkRole(session['subject'], session['role'], subject_role)
        checkPermission(session['role'], permission, role_permission)
        return {'message': 'remain %d units crystal.'} % (nexus.crestalRemain), 200

    def put(self):
        permission = 'get_crystal'
        abortIfSubjectUnauthenticated(session)
        checkRole(session['subject'], session['role'], subject_role)
        checkPermission(session['role'], permission, role_permission)
        args = self.putparser.parse_args()
        amount = nexus.collect(args['amount'])
        return {'message': 'collected %d units crystal.'} % (amount), 200
