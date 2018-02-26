# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ShopinvaderCartStep(models.Model):
    _name = 'shopinvader.cart.step'
    _description = 'Shopinvader Cart Step'

    name = fields.Char(required=True)
    code = fields.Char(required=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    typology = fields.Selection([
        ('sale', 'Sale'),
        ('cart', 'Cart'),
        ], default='sale')
    shopinvader_backend_id = fields.Many2one(
        'locomotive.backend',
        'Backend')
    current_step_id = fields.Many2one(
        'shopinvader.cart.step',
        'Current Cart Step',
        readonly=True)
    done_step_ids = fields.Many2many(
        comodel_name='shopinvader.cart.step',
        string='Done Cart Step',
        readonly=True)
    # TODO move this in an extra OCA module
    shopinvader_state = fields.Selection([
        ('cancel', 'Cancel'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ], compute='_compute_shopinvader_state',
        store=True)

    def _get_shopinvader_state(self):
        self.ensure_one()
        if self.state == 'cancel':
            return 'cancel'
        elif self.state == 'done':
            return 'shipped'
        elif self.state == 'draft':
            return 'pending'
        else:
            return 'processing'

    @api.depends('state')
    def _compute_shopinvader_state(self):
        # simple way to have more human friendly name for
        # the sale order on the website
        for record in self:
            record.shopinvader_state = record._get_shopinvader_state()

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res['shopinvader_backend_id'] = self.shopinvader_backend_id.id
        return res

    @api.multi
    def action_confirm_cart(self):
        for record in self:
            record.write({'typology': 'sale'})
            if record.shopinvader_backend_id:
                record.shopinvader_backend_id._send_notification(
                    'cart_confirmation', record)
        return True

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for record in self:
            if record.state != 'draft' and record.shopinvader_backend_id:
                record.shopinvader_backend_id._send_notification(
                    'sale_confirmation', record)
        return res

    def reset_price_tax(self):
        for record in self:
            record.order_line.reset_price_tax()

    def _need_price_update(self, vals):
        for field in ['fiscal_position_id', 'pricelist_id']:
            if field in vals and self[field].id != vals[field]:
                return True
        return False

    @api.multi
    def write_with_onchange(self, vals):
        self.ensure_one()
        # Playing onchange on one2many is not really really clean
        # all value are returned even if their are not modify
        # Moreover "convert_to_onchange" in field.py add (5,) that
        # will drop the order_line
        # so it's better to drop the key order_line and run the onchange
        # on line manually
        reset_price = False
        new_vals = self.play_onchanges(vals, vals.keys())
        new_vals.pop('order_line', None)
        vals.update(new_vals)
        reset_price = self._need_price_update(vals)
        self.write(vals)
        if reset_price:
            self.reset_price_tax()
        return True


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    shopinvader_variant_id = fields.Many2one(
        'shopinvader.variant',
        compute='_compute_shopinvader_variant',
        string='Shopinvader Variant',
        store=True)

    def reset_price_tax(self):
        for line in self:
            line.product_id_change()

    @api.depends('order_id.shopinvader_backend_id', 'product_id')
    def _compute_shopinvader_variant(self):
        for record in self:
            record.shopinvader_variant_id = self.env['shopinvader.variant']\
                .search([
                    ('record_id', '=', record.product_id.id),
                    ('shopinvader_product_id.backend_id', '=',
                        record.order_id.shopinvader_backend_id.id),
                    ])
