# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Tri Tam Customer',
    'version': '1.0',
    'category': 'Customer',
    'summary': 'Customer Tri Tam',
    'description': """
""",
    'website': 'https://www.odoo.com',
    'depends': ['base','sale','utm','base_phone','tritam_users','hr_recruitment','tritam_crm_pipleline', 'crm'],
    'data': [
        'data/crm_stage_data.xml',
        'views/tritam_customer.xml',
        'views/tritam_crmavtivity.xml',
        'views/templates.xml',
        'views/tritam_customer_source.xml',
        'views/tritam_tag.xml',
        'views/tritam_res_country.xml',
        'data/data.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
