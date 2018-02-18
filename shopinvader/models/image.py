# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class Image(models.Model):
    _inherit = 'base_multi_image.image'

    locomotive_bind_ids = fields.One2many(
        'locomotive.image',
        'record_id',
        string='Locomotive Binding')

    # Automatically create the locomotive binding for the image created
    @api.model
    def create(self, vals):
        image = super(Image, self).create(vals)
        if image.owner_model in ('product.template', 'product.category'):
            record = self.env[image.owner_model].browse(image.owner_id)
            binding_obj = self.env['locomotive.image']
            for binding in record.locomotive_bind_ids:
                for size in binding_obj._image_size:
                    binding_obj.create({
                        'size': size,
                        'record_id': image.id,
                        'backend_id': binding.backend_id.id,
                        })
        return image


class LocomotiveImage(models.Model):
    _name = 'locomotive.image'
    _inherit = 'locomotive.binding'
    _inherits = {'base_multi_image.image': 'record_id'}
    _image_size = {
        'extra_large': {'label': 'Extra Large', 'resize': None},
        'large': {'label': 'Large', 'resize': (500, 500)},
        'medium': {'label': 'Medium', 'resize': (300, 300)},
        'small': {'label': 'Small', 'resize': (60, 60)},
    }

    record_id = fields.Many2one(
        'base_multi_image.image',
        required=True,
        ondelete='cascade')
    url = fields.Char()
    size = fields.Selection('_select_size')

    _sql_constraints = [
        ('record_uniq', 'unique(backend_id, size, record_id)',
         'A product can only have one binding by backend.'),
    ]

    def _select_size(self):
        return [(key, vals['label']) for key, vals in self._image_size.items()]
