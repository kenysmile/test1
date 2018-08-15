# -*- coding: utf-8 -*-

from odoo import models, fields, api

class crm_lead(models.Model):
	_inherit = 'crm.lead'

	landing_page = fields.Char(string="Landing page (id, name, url)")
	landing_page_device = fields.Char(string="Landing desktop/mobile")
	landing_page_ip_address = fields.Char(string="Landing ip address")
	landing_page_referral_source = fields.Char(string="Landing referral source")
