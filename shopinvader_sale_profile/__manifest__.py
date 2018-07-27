# -*- coding: utf-8 -*-
# Copyright 2018 Akretion (http://www.akretion.com).
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'ShopInvader - Sale profile',
    'description': """
        This ShopInvader submodule give the possibility to specify some
        sale profiles (with pricelist per profile) per backend to apply on
        your customers""",
    'version': '10.0.1.0.0',
    'depends': [
        'base',
        'shopinvader_locomotive',
        'shopinvader',
    ],
    'author': 'Akretion,ACSONE SA/NV',
    'website': 'http://www.akretion.com',
    'license': 'AGPL-3',
    'category': 'e-commerce',
    'data': [
        'views/shopinvader_backend.xml',
        'views/res_partner.xml',
        'views/shopinvader_partner.xml',
        'security/shopinvader_sale_profile.xml',
    ],
    'demo': [
        'demo/shopinvader_sale_profile.xml',
        'demo/account_fiscal_position.xml',
    ],
    'installable': True,
}
