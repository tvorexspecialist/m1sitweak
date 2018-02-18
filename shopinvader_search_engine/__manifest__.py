# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{'name': 'Shopinvader Catalog Search Engine Connector',
 'version': '10.0.1.0.0',
 'author': 'Akretion',
 'website': 'www.akretion.com',
 'license': 'AGPL-3',
 'category': 'Generic Modules',
 'depends': [
     'shopinvader',
     'connector_search_engine',
 ],
 'data': [
     'views/backend_view.xml',
     'views/product_view.xml',
     'views/product_category_view.xml',
     'data/ir_export_product.xml',
 ],
 'demo': [
 ],
 'installable': True,
 'application': True,
 }
