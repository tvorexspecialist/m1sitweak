# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp.addons.connector_locomotivecms.backend import locomotive
from openerp.addons.connector_locomotivecms.unit.exporter import (
    LocomotiveExporter)


@locomotive
class PartnerExporter(LocomotiveExporter):
    _model_name = 'locomotive.partner'
