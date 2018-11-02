# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.osv import expression


class ShopinvaderBackend(models.Model):

    _inherit = 'shopinvader.backend'

    product_manual_binding = fields.Boolean(default=True)
    product_assortment_id = fields.Many2one(
        string="Product Assortment",
        comodel_name="ir.filters",
        help="Bind only products matching with the assortment domain",
        domain=[('is_assortment', '=', True)],
        context={
            'product_assortment': True},
    )

    @api.multi
    def _autobind_product_from_assortment(self):
        self.ensure_one()
        product_obj = self.env['product.product']
        shopinvader_variant_obj = self.env['shopinvader.variant']
        binding_wizard_obj = self.env['shopinvader.variant.binding.wizard']
        unbinding_wizard_obj = self.env['shopinvader.variant.unbinding.wizard']
        assortment_domain = self.product_assortment_id._get_eval_domain()
        assortment_products = product_obj.search(assortment_domain)
        variants_binded = shopinvader_variant_obj.search(
            [('backend_id', '=', self.id)])
        products_binded = variants_binded.mapped('record_id')
        products_to_bind = assortment_products - products_binded
        products_to_unbind = products_binded - assortment_products
        variants_to_unbind = variants_binded.filtered(
            lambda x: x.record_id.id in products_to_unbind.ids)

        if products_to_bind:
            binding_wizard = binding_wizard_obj.create({
                'backend_id': self.id,
                'product_ids': [(6, 0, products_to_bind.ids)]
            })
            binding_wizard.bind_products()

        if variants_to_unbind:
            unbinding_wizard = unbinding_wizard_obj.create({
                'shopinvader_variant_ids': [(6, 0, variants_to_unbind.ids)]
            })
            unbinding_wizard.unbind_products()

    @api.model
    def autobind_product_from_assortment(self, domain=None):
        if domain is None:
            domain = []

        domain = expression.AND([domain,
                                [('product_manual_binding', '!=', True)]])

        for backend in self.search(domain):
            backend._autobind_product_from_assortment()
