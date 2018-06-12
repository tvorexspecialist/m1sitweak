# -*- coding: utf-8 -*-
# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.component.core import AbstractComponent


class AbstractSaleService(AbstractComponent):
    _inherit = 'base.shopinvader.service'
    _name = 'shopinvader.abstract.sale.service'

    def _parser_product(self):
        return [
            'full_name:name',
            'short_name',
            ('shopinvader_product_id:model', ('name',)),
            'object_id:id',
            'url_key',
            'default_code:sku',
            ]

    def _convert_one_sale(self, sale):
        sale.ensure_one()
        return {
            'id': sale.id,
            'state': sale.shopinvader_state,
            'name': sale.name,
            'date': sale.date_order,
            'step': self._convert_step(sale),
            'lines': self._convert_lines(sale),
            'amount': self._convert_amount(sale),
            'shipping': self._convert_shipping(sale),
            'invoicing': self._convert_invoicing(sale),
            }

    def _convert_step(self, sale):
        return {
            'current': sale.current_step_id.code,
            'done': sale.done_step_ids.mapped('code'),
            }

    def _is_item(self, line):
        return True

    def _convert_one_line(self, line):
        if line.shopinvader_variant_id:
            # TODO we should reuse the parser of the index
            product = line.shopinvader_variant_id.jsonify(
                self._parser_product())[0]
        else:
            product = {}
        return {
            'id': line.id,
            'product': product,
            'amount': {
                'price': line.price_unit,
                'untaxed': line.price_subtotal,
                'tax': line.price_tax,
                'total': line.price_total,
                },
            'qty': line.product_uom_qty,
            'discount': {
                'rate': line.discount,
                }
            }

    def _convert_lines(self, sale):
        items = []
        for line in sale.order_line:
            if self._is_item(line):
                items.append(self._convert_one_line(line))
        return {
            'items': items,
            'count': sum([item['qty'] for item in items]),
            'amount': {
                'tax': sum([item['amount']['tax'] for item in items]),
                'untaxed': sum([item['amount']['untaxed'] for item in items]),
                'total': sum([item['amount']['total'] for item in items]),
                }
            }

    def _convert_shipping(self, sale):
        if sale.partner_shipping_id ==\
                self.shopinvader_backend.anonymous_partner_id:
            return {'address': {}}
        else:
            address_service = self.component(usage='addresses')
            return {
                'address':
                    address_service._to_json(sale.partner_shipping_id)[0]
            }

    def _convert_invoicing(self, sale):
        if sale.partner_invoice_id ==\
                self.shopinvader_backend.anonymous_partner_id:
            return {'address': {}}
        else:
            address_service = self.component(usage='addresses')
            return {
                'address':
                    address_service._to_json(sale.partner_invoice_id)[0],
                }

    def _convert_amount(self, sale):
        return {
            'tax': sale.amount_tax,
            'untaxed': sale.amount_untaxed,
            'total': sale.amount_total,
            }

    def _to_json(self, sales):
        res = []
        for sale in sales:
            res.append(self._convert_one_sale(sale))
        return res
