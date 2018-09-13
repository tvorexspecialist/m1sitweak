# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader.tests.test_notification import (
    CommonNotificationCase
)


class NotificationQuotationCase(CommonNotificationCase):

    def test_quotation_notification(self):
        self._init_job_counter()
        self.cart.action_request_quotation()
        self._check_nbr_job_created(1)
        self._perform_created_job()
        self._check_notification('quotation_request', self.cart)
