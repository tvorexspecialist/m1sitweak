# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com).
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.addons.component.core import Component


class ShopInvaderCustomerService(Component):
    _inherit = 'shopinvader.customer.service'

    def _prepare_create_response(self, binding):
        """
        Inherit the creation of create responseto add the sale profile
        code of the shopinvader partner
        :param binding: instance of shopinvader.binding
        :return: dict
        """
        response = super(ShopInvaderCustomerService, self)\
            ._prepare_create_response(binding=binding)
        data = response.get('data', {})
        data.update({
            'sale_profile': binding.sale_profile_id.code,
        })
        return response
