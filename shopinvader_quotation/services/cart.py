# -*- coding: utf-8 -*-
# Copyright 2016 Akretion (http://www.akretion.com)
# Benoît GUILLOT <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.addons.component.core import Component


class CartService(Component):
    _inherit = 'shopinvader.cart.service'

    def request_quotation(self, **params):
        cart = self._get()
        cart.action_request_quotation()
        res = self._to_json(cart)
        res.update({
            'store_cache': {'last_sale': res['data'], 'cart': {}},
            'set_session': {'cart_id': 0},
        })
        return res

    # Validator
    def _validator_request_quotation(self):
        return {}

    def _convert_one_sale(self, sale):
        res = super(CartService, self)._convert_one_sale(sale)
        res.update({'available_for_quotation': True})
        return res
