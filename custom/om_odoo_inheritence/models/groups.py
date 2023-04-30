# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResGroups(models.Model):
    _inherit = 'res.groups'

    def get_application_groups(self, domain):
        print("Domain", domain)
        group_id = self.env.ref('stock.group_reception_report').id
        wave_group_id = self.env.ref('stock.group_stock_picking_wave').id
        return super(ResGroups, self).get_application_groups(domain + [('id', '!=', (group_id, wave_group_id))])
