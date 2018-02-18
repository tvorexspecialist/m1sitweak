# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class UrlUrl(models.Model):
    _inherit = "url.url"

    model_id = fields.Reference(
        selection_add=[
            ('locomotive.product', 'Locomotive Product'),
            ('locomotive.category', 'Locomotive Category'),
            ])
