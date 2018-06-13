# -*- coding: utf-8 -*-
# © 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Shopinvader Locomotive CMS Connector',
    'version': '10.0.1.0.0',
    'category': 'Connector',
    'summary': 'Manage communications between Shopinvader and Locomotive CMS',
    'author': 'Akretion',
    'website': 'http://www.akretion.com',
    'license': 'AGPL-3',
    'images': [],
    'depends': [
        'connector',
        'queue_job',
        'keychain',
        'shopinvader'
    ],
    'data': [
        'views/shopinvader_backend_view.xml',
    ],
    'demo': [
        'demo/backend_demo.xml',
    ],
    'test': [
    ],
    'external_dependencies': {
        'python': ['locomotivecms', 'openupgradelib'],
        },
    'pre_init_hook': 'rename_module',
    'installable': True,
    'auto_install': False,
    'application': False,
}
