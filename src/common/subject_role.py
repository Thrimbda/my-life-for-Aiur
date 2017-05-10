# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-10 23:01:32
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-10 23:39:55
subject_role = (('thrimbda', 'archon'),
                ('probe', 'crystal_collector'),
                ('probe', 'pylon_transporter'),
                ('gateway', 'portal'))

subjects = list(set([item[0] for item in subject_role]))
roles = list(set([item[1] for item in subject_role]))
