# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 01:39:31
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 10:52:36
from flask.ext.restful import Resource, reqparse
from flask import session
from src.common.util import abortIfSubjectUnauthenticated, checkRole, checkPermission
from src.common.subject_role import subject_role
from src.common.role_permission import role_permission
from src.API import nexus


class Pylon(Resource):

    def __init__(self):
        self.putparser = reqparse.RequestParser()
        self.putparser.add_argument('amount',
                                    type=int,
                                    default=1,
                                    location='json')
        super(Pylon, self).__init__()

    def get(self):
        permission = 'get_status'
        abortIfSubjectUnauthenticated(session)
        checkRole(session.subject, session.role, subject_role)
        checkPermission(session.role, permission, role_permission)
        return 'you have %d pylon(s) provide %d population capacity' % ((nexus.zealot * 2 + nexus.populationCap) / 10,
                                                                        nexus.populationCap), 200

    def put(self):
        permission = 'transport_zealot'
        abortIfSubjectUnauthenticated(session)
        checkRole(session.subject, session.role, subject_role)
        checkPermission(session.role, permission, role_permission)
        args = self.putparser.parse_args()
        amount = nexus.transport(args['amount'])
        return 'built %d pylons provide more %d population capacity' % (amount, amount * 10), 200
