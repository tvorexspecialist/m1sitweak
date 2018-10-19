# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com)
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from odoo.addons.component.core import Component
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class CartService(Component):
    _inherit = 'shopinvader.cart.service'

    def _update(self, cart, params):
        coupon_code = params.pop('coupon_code', None)
        if coupon_code is not None:
            if 'payment_params' in params:
                raise UserError(
                    _("Appling discount and paying can "
                      "not be done in the same call"))
        res = super(CartService, self)._update(cart, params)
        if coupon_code:
            cart.add_coupon(coupon_code)
        else:
            if cart.coupon_code:
                # the promotion has been removed:
                # * clear the promotion
                cart.clear_promotions()
        # apply default promotion
        cart.apply_promotions()
        return res

    def _add_item(self, cart, params):
        res = super(CartService, self)._add_item(cart, params)
        cart.apply_promotions()
        return res

    def _update_item(self, cart, params):
        res = super(CartService, self)._update_item(cart, params)
        cart.apply_promotions()
        return res

    def _delete_item(self, cart, params):
        res = super(CartService, self)._delete_item(cart, params)
        cart.apply_promotions()
        return res

    # Validator
    def _validator_update(self):
        res = super(CartService, self)._validator_update()
        res['coupon_code'] = {'type': 'string'}
        return res

    # converter
    def _convert_one_sale(self, sale):
        res = super(CartService, self)._convert_one_sale(sale)
        res.update(self._get_promotions_info(sale))
        return res

    def _convert_one_line(self, line):
        res = super(CartService, self)._convert_one_line(line)
        res.update(self._get_promotions_info(line))
        return res

    def _get_promotions_info(self, o):
        return {
            'promotion_rule_coupon':
                self._convert_promotion_rule(
                    o.coupon_promotion_rule_id),
            'promotion_rules_auto': [
                self._convert_promotion_rule(r) for r in o.promotion_rule_ids]
        }

    def _convert_promotion_rule(self, sale_promotion_rule):
        if not sale_promotion_rule:
            return {}
        return {
            'name': sale_promotion_rule.name or None,
            'code': sale_promotion_rule.code or None,
            'discount_amount': sale_promotion_rule.discount_amount or None,
            'discount_type': sale_promotion_rule.discount_type or None,
            'rule_type': sale_promotion_rule.rule_type
        }
