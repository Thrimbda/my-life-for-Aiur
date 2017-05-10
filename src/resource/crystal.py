# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 01:04:44
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 01:15:11
from flask.ext.restful import Resource, reqparse
from flask import session
from src.common.util import abortIfSubjectUnauthenticated, checkRole
from src.common.subject_role import subject_role
from src.API import nexus


class Crystal(Resource):

    def __init__(self):
        self.putparser = reqparse.RequestParser()
        self.putparser.add_argument
        super(Crystal, self).__init__()

    def put(self):
        abortIfSubjectUnauthenticated(session)
        checkRole(session.subject, session.role, subject_role)
        nexus.collect()
