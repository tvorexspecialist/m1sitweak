# -*- coding: utf-8 -*-
# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Shopinvader Product Media",
    "summary": "Shopinvader Product Media",
    "version": "8.0.1.0.0",
    "category": "e-commerce",
    "website": "https://akretion.com",
    "author": "Akretion",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "shopinvader",
        "product_media",
    ],
    "data": [
        "data/ir_product_export.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
