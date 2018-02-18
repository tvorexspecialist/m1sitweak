# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp.addons.connector.backend import Backend


locomotivecms = Backend('locomotivecms')
""" LocomotiveCMS Backend"""

locomotivecms_v3 = Backend(parent=locomotivecms, version='locomotivecms_v3')
""" LocomotiveCMS Backend"""
