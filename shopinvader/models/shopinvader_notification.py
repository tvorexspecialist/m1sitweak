# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.addons.queue_job.job import job


class ShopinvaderNotification(models.Model):
    _name = 'shopinvader.notification'
    _description = 'Shopinvader Notification'

    def _get_all_notification(self):
        return {
            'cart_confirmation': {
                'name': _('Cart Confirmation'),
                'model': 'sale.order',
                },
            'sale_confirmation': {
                'name': _('Sale Confirmation'),
                'model': 'sale.order',
                },
            'invoice_open': {
                'name': _('Invoice Validated'),
                'model': 'account.invoice',
                },
            'new_customer_welcome': {
                'name': _('New customer Welcome'),
                'model': 'res.partner',
                },
            }

    def _get_select_notification(self):
        notifications = self._get_all_notification()
        return [(key, notifications[key]['name']) for key in notifications]

    backend_id = fields.Many2one(
        'shopinvader.backend',
        'Backend',
        required=True)
    notification_type = fields.Selection(
        selection=_get_select_notification,
        string='Notification Type',
        required=True)
    model_id = fields.Many2one(
        'ir.model',
        'Model',
        required=True)
    template_id = fields.Many2one(
        'mail.template',
        'Mail Template',
        required=True)

    @api.onchange('notification_type')
    def on_notification_type_change(self):
        self.ensure_one()
        notifications = self._get_all_notification()
        if self.notification_type:
            model = notifications[self.notification_type].get('model')
            if model:
                self.model_id = self.env['ir.model'].search([
                    ('model', '=', model)])
                return {
                    'domain': {'model_id': [('id', '=', self.model_id.id)]},
                    }
            else:
                return {'domain': {'model_id': []}}

    @job(default_channel='root.shopinvader.notification')
    def send(self, record_id):
        return self.template_id.send_mail(record_id)
