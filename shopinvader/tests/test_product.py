# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Benoît GUILLOT <benoit.guillot@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from .common import ProductCommonCase


class ProductCase(ProductCommonCase):

    def test_create_shopinvader_variant(self):
        self.assertEqual(
            len(self.template.product_variant_ids),
            len(self.shopinvader_variant))

    def test_categories(self):
        self.assertEqual(len(self.shopinvader_variant[0].categories), 0)
        self.backend.bind_all_category()
        self.assertEqual(len(self.shopinvader_variant[0].categories), 1)
        self.assertEqual(
            self.shopinvader_variant[0].categories.record_id,
            self.template.categ_id)
