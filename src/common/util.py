# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-11 01:05:33
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-11 01:18:05
from flask.ext.restful import abort
from src.common.subject_role import subjects, roles


def abortIfSubjectUnauthenticated(session):
    if 'subject' not in session:
        abort(404, message="Subject Unspecified.")


def abortInvalideSubject(subject):
    if subject not in subjects:
        abort(403, message="invalid subject.")


def abortInvalideRole(role):
    if role not in roles:
        abort(403, message="invalid role.")


def checkRole(subject, role, subject_role):
    if (subject, role) not in subject_role:
        abort(403, message="subject %s can't be a %s." % (subject, role))


def checkPermission(role, permission, role_permission):
    if (role, permission) not in role_permission:
        abort(403, message="role %s access %s denied." % (role, permission))
