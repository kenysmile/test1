# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Duoc Tri Tam Sale',
    'version': '1.0',
    'category': 'Sale',
    'summary': 'Sale',
    'description': """
""",
    'website': 'https://www.odoo.com',
    'depends': [
    	'base','sale', 'tritam_customer','tritam_users','sale_order_dates','delivery','hr_expense','tritam_cpn_api','multiple_invoice','crm','stock_picking_wave'
    ],
    'data': [
        'views/so_view.xml',
        'views/custom_sale_dashboard.xml',
        'wizard/sale_report_views_revenue.xml',
        'wizard/sale_report_views_lead_marketing.xml',
        'views/search_view.xml',
        'views/sale_config_setting_inherit_view.xml',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
