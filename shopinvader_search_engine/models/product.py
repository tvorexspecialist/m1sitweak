# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class ShopinvaderVariant(models.Model):
    _inherit = ['shopinvader.variant', 'se.binding']
    _name = 'shopinvader.variant'

    index_id = fields.Many2one(
        compute="_compute_index",
        store=True,
        required=False)

    price = fields.Serialized(
        compute='_compute_price',
        string='Shopinvader Image')

    def _compute_price(self):
        for record in self:
            record.price = {}
            for role in record.backend_id.role_ids:
                record.price[role.code] = record._get_price(
                    role.pricelist_id, role.fiscal_position_ids[0])

    @api.depends('lang_id', 'backend_id.se_backend_id')
    def _compute_index(self):
        for record in self:
            se_backend = record.backend_id.se_backend_id
            if se_backend:
                record.index_id = self.env['se.index'].search([
                    ('backend_id', '=', se_backend.id),
                    ('lang_id', '=', record.lang_id.id),
                    ('model_id.model', '=', record._name),
                    ])
