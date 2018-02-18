# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{'name': 'Shopinvader Algolia Connector',
 'version': '8.0.0.0.1',
 'author': 'Akretion',
 'website': 'www.akretion.com',
 'license': 'AGPL-3',
 'category': 'Generic Modules',
 'post_init_hook': 'post_init_hook',
 'depends': [
     'shopinvader_search_engine',
     'connector_algolia',
 ],
 'data': [
 ],
 'demo': [
     'demo/backend_demo.xml',
 ],
 'installable': True,
 'application': True,
 }
