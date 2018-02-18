# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from ..services.cart import CartService
from .common import CommonCase


class AbstractCartCase(object):

    def set_up(self):
        self.contact = self.env.ref('shopinvader.partner_1_contact_1')


class AnonymousCartCase(AbstractCartCase, CommonCase):

    def setUp(self, *args, **kwargs):
        super(AnonymousCartCase, self).setUp(*args, **kwargs)
        self.set_up()
        self.cart = self.env.ref('shopinvader.sale_order_1')
        self.partner = self.env.ref('shopinvader.anonymous')
        self.service = self._get_service(CartService, None)
        self.address_ship = {
            'name': 'Purple',
            'street': 'Rue du jardin',
            'zip': '43110',
            'city': 'Aurec sur Loire',
            'phone': '0485485454',
            'country_id': self.env.ref('base.fr').id,
            'email': 'anonymous@customer.example.com',
            'external_id': 'WW5KaGRtOD0=',
            }
        self.address_invoice = {
            'name': 'Gospel',
            'street': 'Rue du jardin',
            'zip': '43110',
            'city': 'Aurec sur Loire',
            'phone': '0485485454',
            'country_id': self.env.ref('base.fr').id,
            }

    def _check_address(self, partner, data):
        for key in data:
            if key == 'external_id':
                continue
            elif key == 'country_id':
                self.assertEqual(partner[key].id, data[key])
            else:
                self.assertEqual(partner[key], data[key])

    def _add_shipping_address(self):
        self.service.update({
            'id': self.cart.id,
            'partner_shipping_id': self.address_ship,
            })
        self._check_address(self.cart.partner_shipping_id, self.address_ship)

    def _add_shipping_and_invoice_address(self):
        self.service.update({
            'id': self.cart.id,
            'partner_shipping_id': self.address_ship,
            'partner_invoice_id': self.address_invoice,
            'use_different_invoice_address': True
            })
        self._check_address(self.cart.partner_shipping_id, self.address_ship)
        self._check_address(self.cart.partner_invoice_id, self.address_invoice)

    def test_add_new_shipping_contact(self):
        cart = self.cart
        self._add_shipping_address()

        self.assertNotEqual(cart.partner_id, self.partner)
        self.assertEqual(cart.partner_id, cart.partner_shipping_id)
        self.assertEqual(cart.partner_id, cart.partner_invoice_id)

    def test_add_new_shipping_and_billing_contact(self):
        self._add_shipping_and_invoice_address()

        cart = self.cart
        self.assertNotEqual(cart.partner_id, self.partner)
        self.assertEqual(cart.partner_id, cart.partner_shipping_id)
        self.assertNotEqual(cart.partner_id, cart.partner_invoice_id)

    def test_anonymous_cart_then_sign(self):
        cart = self.cart
        partner = self.env.ref('shopinvader.partner_1')
        self.service = self._get_service(CartService, partner)
        self.service.update({
            'id': cart.id,
            'assign_partner': True,
            })
        self.assertEqual(cart.partner_id, partner)
        self.assertEqual(cart.partner_shipping_id, self.partner)
        self.assertEqual(cart.partner_invoice_id, self.partner)


class ConnectedCartCase(AbstractCartCase, CommonCase):

    def setUp(self, *args, **kwargs):
        super(ConnectedCartCase, self).setUp(*args, **kwargs)
        self.set_up()
        self.cart = self.env.ref('shopinvader.sale_order_2')
        self.partner = self.env.ref('shopinvader.partner_1')
        self.contact = self.env.ref('shopinvader.partner_1_contact_1')
        self.service = self._get_service(CartService, self.partner)

    def test_set_shipping_contact(self):
        self.service.update({
            'id': self.cart.id,
            'partner_shipping_id': self.contact.id,
            })
        cart = self.cart
        self.assertEqual(cart.partner_id, self.partner)
        self.assertEqual(cart.partner_shipping_id, self.contact)
        self.assertEqual(cart.partner_invoice_id, self.contact)

    def test_set_invoice_contact(self):
        self.service.update({
            'id': self.cart.id,
            'use_different_invoice_address': True,
            'partner_invoice_id': self.contact.id,
            })

        cart = self.cart
        self.assertEqual(cart.partner_id, self.partner)
        self.assertEqual(cart.partner_shipping_id, self.partner)
        self.assertEqual(cart.partner_invoice_id, self.contact)
