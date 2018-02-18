# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.addons.connector_locomotivecms.unit.binder import LocomotiveBinder
from ..backend import shopinvader


@shopinvader
class ShopinvaderBinder(LocomotiveBinder):
    _model_name = [
        'shopinvader.partner',
    ]
