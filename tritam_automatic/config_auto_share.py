# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Caidatphanbo(models.Model):
    _name = 'res.automatic.share.settings'
    _inherit = 'res.config.settings'
    _order = 'id desc'


    conf_new_contact = fields.Integer()
    conf_re_use = fields.Integer()
    conf_re_sign = fields.Integer()

    @api.model
    def get_conf_new_contact(self, fields):
        conf_new_contact = self.env['ir.values'].get_defaults_dict('res.automatic.share.settings').get('number_use')
        conf_re_use = self.env['ir.values'].get_defaults_dict('res.automatic.share.settings').get('conf_re_use')
        conf_re_sign = self.env['ir.values'].get_defaults_dict('res.automatic.share.settings').get('conf_re_sign')
        return {
            'conf_new_contact': conf_new_contact,
            'conf_re_use':conf_re_use,
            'conf_re_sign':conf_re_sign
            }

    @api.model
    def set_conf_new_contact(self):
        set_conf_new_contact = self.env['ir.values'].sudo().set_default(
            'res.automatic.share.settings', 'conf_new_contact', self.conf_new_contact)
        set_conf_re_use = self.env['ir.values'].sudo().set_default(
            'res.automatic.share.settings', 'conf_re_use', self.conf_re_use)
        set_conf_re_sign = self.env['ir.values'].sudo().set_default(
            'res.automatic.share.settings', 'conf_re_sign', self.conf_re_sign)
        return set_conf_new_contact,set_conf_re_use,set_conf_re_sign





