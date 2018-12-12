# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from odoo.addons.component.tests.common import SavepointComponentCase
from odoo.exceptions import ValidationError


class TestResPartner(SavepointComponentCase):

    @classmethod
    def setUpClass(cls):
        super(TestResPartner, cls).setUpClass()
        cls.shopinvader_config = cls.env['shopinvader.config.settings']
        cls.unique_email = datetime.now().isoformat() + '@test.com'

    def test_unique_email_partner(self):
        self.assertTrue(
            self.shopinvader_config.is_partner_duplication_allowed())
        self.env['res.partner'].create({
            'email': self.unique_email,
            'name': 'test partner',
        })
        # by default we can create partner with same email
        self.env['res.partner'].create({
            'email': self.unique_email,
            'name': 'test partner 2',
        })
        self.shopinvader_config.create({
            "no_partner_duplicate": True,
        }).execute()
        self.assertFalse(
            self.shopinvader_config.is_partner_duplication_allowed())
        # once you've changed the config to dispable duplicate partner
        # it's no more possible to create a partner with the same email
        with self.assertRaises(ValidationError), self.cr.savepoint():
            self.env['res.partner'].create({
                'email': self.unique_email,
                'name': 'test partner 3',
            })
