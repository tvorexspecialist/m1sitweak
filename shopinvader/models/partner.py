# -*- coding: utf-8 -*-
# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class LocomotivePartner(models.Model):
    _name = 'locomotive.partner'
    _inherit = 'locomotive.binding'
    _inherits = {'res.partner': 'record_id'}

    record_id = fields.Many2one(
        'res.partner',
        required=True,
        ondelete='cascade')
    partner_email = fields.Char(
        related='record_id.email',
        readonly=True,
        required=True,
        store=True)

    _sql_constraints = [
        ('record_uniq', 'unique(backend_id, record_id, partner_email)',
         'A partner can only have one binding by backend.'),
        ('email_uniq', 'unique(backend_id, partner_email)',
         'An email must be uniq per backend.'),
    ]

    @api.model
    def create(self, vals):
        # As we want to have a SQL contraint on customer email
        # we have to set it manually to avoid to raise the constraint
        # at the creation of the element
        vals['partner_email'] = self.env['res.partner'].browse(
            vals['record_id']).email
        return super(LocomotivePartner, self).create(vals)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    locomotive_bind_ids = fields.One2many(
        'locomotive.partner',
        'record_id',
        string='Locomotive Binding')

    # TODO it will be great to have a generic module that
    # - filter correctly the address on sale order, invoice, po
    # - define a default address per type
    is_default_delivery = fields.Boolean(readonly=True)
    is_default_invoice = fields.Boolean(readonly=True)

    def set_as_main_delivery_address(self):
        self._set_as_main_address('delivery')

    def set_as_main_invoice_address(self):
        self._set_as_main_address('invoice')

    def _set_as_main_address(self, address_type):
        for record in self:
            address_to_remove = self.search([
                '|',
                ('parent_id', '=', record.parent_id),
                ('id', '=', record.parent_id),
                ('is_default_%s' % address_type, '=', True),
                ])
            address_to_remove.write({'is_default_%s' % address_type: False})
            record.write({'is_default_%s' % address_type: True})

    def _get_main_address(self, address_type):
        self.ensure_one()
        delivery = self.search([
            ('parent_id', '=', self.id),
            ('is_default_%s' % address_type, '=', True),
            ])
        if not delivery:
            return self
        else:
            return delivery
