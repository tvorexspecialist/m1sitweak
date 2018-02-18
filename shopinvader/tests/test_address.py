# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from ..services.address import AddressService
from .common import CommonCase
from werkzeug.exceptions import Forbidden


class AddressCase(CommonCase):

    def setUp(self, *args, **kwargs):
        super(AddressCase, self).setUp(*args, **kwargs)
        self.partner = self.env.ref('shopinvader.partner_1')
        self.service = self._get_service(AddressService, self.partner)
        self.address = self.env.ref('shopinvader.partner_1_address_1')
        self.address_params = {
            'name': 'Purple',
            'street': 'Rue du jardin',
            'zip': '43110',
            'city': 'Aurec sur Loire',
            'phone': '0485485454',
            'country_id': self.env.ref('base.fr').id,
            }

    def check_data(self, address, data):
        for key in data:
            if key == 'partner_email':
                continue
            elif key == 'country_id':
                self.assertEqual(address[key].id, data[key])
            else:
                self.assertEqual(address[key], data[key])

    def test_add_address(self):
        address_ids = [
            address['id']
            for address in self.service.get({})['data']]
        address_list = self.service.create(self.address_params)['data']
        for address in address_list:
            if address['id'] not in address_ids:
                created_address = address
        self.assertIsNotNone(created_address)
        address = self.env['res.partner'].browse(created_address['id'])
        self.assertEqual(address.parent_id, self.partner)
        self.check_data(address, self.address_params)

    def test_update_address(self):
        params = self.address_params
        params['id'] = self.address.id
        self.service.update(params)
        self.assertEqual(self.address.parent_id, self.partner)
        self.check_data(self.address, params)

    def test_update_main_address(self):
        params = self.address_params
        params['id'] = self.partner.id
        self.service.update(params)
        self.check_data(self.partner, params)

    def test_read_address_profile(self):
        res = self.service.get({
            'domain': {'address_type': 'profile'},
            })['data']
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['id'], self.partner.id)

    def test_read_address_address(self):
        res = self.service.get({
            'domain': {'address_type': 'address'},
            })['data']
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['id'], self.address.id)

    def test_read_address_all(self):
        res = self.service.get({})['data']
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]['id'], self.partner.id)
        self.assertEqual(res[1]['id'], self.address.id)

    def test_delete_address(self):
        address_id = self.address.id
        self.service.delete({'id': address_id})
        address = self.env['res.partner'].search([('id', '=', address_id)])
        self.assertEqual(len(address), 0)
        partner = self.env['res.partner'].search([
            ('id', '=', self.partner.id)])
        self.assertEqual(len(partner), 1)

    def test_delete_main_address(self):
        with self.assertRaises(Forbidden):
            self.service.delete({
                'id': self.partner.id,
                })
