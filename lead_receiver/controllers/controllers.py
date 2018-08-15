# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Submit(http.Controller):
	@http.route('/submit', type='http', method=['POST'], auth="none", csrf=False)
	def submit_lead(self, **kw):
		print(kw)
		# check token

		# create lead
		page_id = kw['page_id'] if 'page_id' in kw else ''
		page_name = kw['page_name'] if 'page_name' in kw else ''
		page_url = kw['page_url'] if 'page_url' in kw else ''
		landing_page = "pageid: %s, page_name: %s, page_url: %s)" % (page_id, page_name, page_url)

		product_id = False
		Product = request.env['product.template'].sudo()
		default_code = kw['product'] if 'product' in kw else ''
		if default_code:
			product = Product.search([('default_code', '=', default_code)])
			if not product:
				product = Product.create({'name': default_code, 'default_code' : default_code})
			product_id = Product.product_variant_id.id
			
		value = {
			'name': kw['name'] if 'name' in kw else False,
			'email_from': kw['email'] if 'email' in kw else False,
			'phone': kw['phone'] if 'phone' in kw else False,
			'landing_page_device': kw['desktopmobile'] if 'desktopmobile' in kw else False,
			'landing_page_ip_address': kw['ipaddress'] if 'ipaddress' in kw else False,
			'landing_page_referral_source': kw['referralsource'] if 'referralsource' in kw else False,
			'landing_page': landing_page,
			'product_id' : product_id
		}

		request.env['crm.lead'].sudo().create(value)