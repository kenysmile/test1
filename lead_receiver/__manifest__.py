# -*- coding: utf-8 -*-
{
    'name': "Landing page lead receiver",

    'summary': """
        From webhook of instapage, receive POST request and create lead""",

    'description': """
        From webhook of instapage, receive POST request and create lead
    """,

    'author': "Entrust company",
    'website': "http://entrustlab.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'crm', 'tritam_crm_pipleline'],

    # always loaded
    'data': [
        'views/crm_inherit_view.xml',
    ],
}