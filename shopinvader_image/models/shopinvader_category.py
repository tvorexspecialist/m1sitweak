# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models


class ShopinvaderCategory(models.Model):
    _name = 'shopinvader.category'
    _inherit = ['shopinvader.category', 'shopinvader.image.mixin']
    _image_field = 'image_ids'
