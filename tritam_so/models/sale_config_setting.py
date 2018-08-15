# -*- coding: utf-8 -*-
from json import dumps
from odoo import api, fields, models

class SaleOrderSettings(models.TransientModel):
    _inherit = 'sale.config.settings'

    metabase_site_url = fields.Char('METABASE_SITE_URL')
    metabase_secret_key = fields.Char('METABASE_SECRET_KEY')

    @api.model
    def get_default_metabase_site_url(self, fields):
        return {
            'metabase_site_url': self.env['ir.values'].get_default('sales.config.settings',
                                                                   'metabase_site_url')
        }

    @api.multi
    def set_default_metabase_site_url(self):
        IrValues = self.env['ir.values'].sudo()
        IrValues.set_default('sales.config.settings', 'metabase_site_url', self.metabase_site_url)

    @api.model
    def get_default_metabase_secret_key(self, fields):
        return {
            'metabase_secret_key': self.env['ir.values'].get_default('sales.config.settings',
                                                                   'metabase_secret_key')
        }

    @api.multi
    def set_default_metabase_secret_key(self):
        IrValues = self.env['ir.values'].sudo()
        IrValues.set_default('sales.config.settings', 'metabase_secret_key', self.metabase_secret_key)