# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.base_rest.components.service import to_int
from odoo.addons.component.core import Component
from odoo.exceptions import AccessError


class AddressService(Component):
    _inherit = 'base.shopinvader.service'
    _name = 'shopinvader.address.service'
    _usage = 'addresses'
    _expose_model = 'res.partner'

    # The following method are 'public' and can be called from the controller.

    def get(self, _id):
        return self._to_json(self._get(_id))

    def search(self, **params):
        if not self.partner:
            return {'data': []}
        else:
            return self._paginate_search(**params)

    def create(self, **params):
        params['parent_id'] = self.partner.id
        if not params.get('type'):
            params['type'] = 'other'
        self.env['res.partner'].create(self._prepare_params(params))
        return self.search()

    def update(self, _id, **params):
        address = self._get(_id)
        address.write(self._prepare_params(params, update=True))
        res = self.search()
        if address.address_type == 'profile':
            res['store_cache'] = {'customer': self._to_json(address)[0]}
        return res

    def delete(self, _id):
        address = self._get(_id)
        if self.partner == address:
            raise AccessError('Can not delete the partner account')
        address.active = False
        return self.search()

    # The following method are 'private' and should be never never NEVER call
    # from the controller.
    # All params are trusted as they have been checked before

    # Validator
    def _validator_search(self):
        return {
            'scope': {
                'type': 'dict',
                'nullable': True,
                },
            }

    def _validator_create(self):
        res = {
            'street': {'type': 'string', 'required': True, 'empty': False},
            'street2': {'type': 'string', 'nullable': True},
            'zip': {'type': 'string', 'required': True, 'empty': False},
            'city': {'type': 'string', 'required': True, 'empty': False},
            'phone': {'type': 'string', 'nullable': True, 'empty': False},
            'state': {
                'type': 'dict',
                'schema': {
                    'id': {
                        'coerce': to_int,
                        'nullable': True},
                    }
                },
            'country': {
                'type': 'dict',
                'schema': {
                    'id': {
                        'coerce': to_int,
                        'required': True,
                        'nullable': False},
                    }
                },
            'is_company': {'coerce': bool},
            'opt_in': {'coerce': bool},
            'opt_out': {'coerce': bool},
            }
        if 'partner_firstname' in self.env.registry._init_modules:
            res.update({
                'firstname': {
                    'type': 'string',
                    'required': True,
                    'excludes': 'name',
                    'empty': False
                    },
                'lastname': {
                    'type': 'string',
                    'required': True,
                    'excludes': 'name',
                    'empty': False
                    },
                'name': {
                    'type': 'string',
                    'required': True,
                    'excludes': ['firstname', 'lastname'],
                    'empty': False,
                    },
                })
        else:
            res.update({
                'name': {'type': 'string', 'required': True},
            })
        if 'company' in self.env['res.partner']._fields:
            res.update({'company': {'type': 'string'}})
        return res

    def _validator_update(self):
        res = self._validator_create()
        for key in res:
            if 'required' in res[key]:
                del res[key]['required']
        return res

    def _validator_delete(self):
        return {
            'id': {'coerce': to_int, 'required': True},
            }

    def _get_base_search_domain(self):
        return [('id', 'child_of', self.partner.id)]

    def _json_parser(self):
        res = [
            'id',
            'display_name',
            'name',
            'ref',
            'street',
            'street2',
            'zip',
            'city',
            'phone',
            'opt_in',
            'opt_out',
            'vat',
            ('state_id', ['id', 'name']),
            ('country_id', ['id', 'name']),
            'address_type',
            'is_company',
        ]
        if 'partner_firstname' in self.env.registry._init_modules:
            res += ['firstname', 'lastname']
        if 'company' in self.env['res.partner']._fields:
            res.append('company')
        return res

    def _to_json(self, address):
        return address.jsonify(self._json_parser())

    def _prepare_params(self, params, update=False):
        for key in ['country', 'state']:
            if key in params:
                val = params.pop(key)
                if val.get('id'):
                    params["%s_id" % key] = val['id']
        return params
