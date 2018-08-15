# -*- coding: utf-8 -*-
from odoo import models,api
from odoo.addons.base_phone import fields
from odoo.exceptions import AccessDenied, UserError
from odoo.exceptions import ValidationError

class tritam_sale_order(models.Model):
    _inherit = 'sale.order'

    phone = fields.Phone(string='Phone')
    mobile = fields.Phone(string='Mobile')

    @api.onchange('partner_id')
    def onchange_phone_mobile(self):
        values = {}
        if self.partner_id:
            values['phone'] = self.partner_id.phone
        if self.partner_id:
            values['mobile'] = self.partner_id.mobile
        self.update(values)

    @api.constrains('mobile')
    def _verify_mobile(self):
        for r in self:
            if r.mobile != r.partner_id.mobile:
                raise ValidationError('Không khớp mobile')

    @api.constrains('phone')
    def _verify_phone(self):
        for r in self:
            if r.phone != r.partner_id.phone:
                raise ValidationError('Không khớp phone')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    phone = fields.Phone(string='Phone', related='partner_id.phone')
    mobile = fields.Phone(string='mobile', related='partner_id.mobile')

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    phone = fields.Phone(string='Phone', compute='_get_phone', inverse='_set_phone', search='seach_phone')
    phone_hidden = fields.Phone(string='Phone hidden')

    mobile = fields.Phone(string='mobile', compute='_get_mobile', inverse='_set_mobile')
    mobile_hidden = fields.Phone(string='Mobile hidden')


    @api.depends('partner_id.phone', 'phone_hidden')
    def _get_phone(self):
        for record in self:
            if record.partner_id:
                record.phone = record.partner_id.phone
            else:
                record.phone = record.phone_hidden


    def _search_phone(self, phone, value):
        if self.phone:
            return [(phone, value)]

    # @api.depend('partner_id')
    def _set_phone(self):
        for record in self:
            record.phone_hidden = record.phone
            if record.partner_id:
                record.partner_id.write({'phone': record.phone_hidden})

    @api.depends('partner_id.mobile', 'mobile_hidden')
    def _get_mobile(self):
        for record in self:
            if record.partner_id:
                record.mobile = record.partner_id.mobile
            else:
                record.mobile = record.mobile_hidden

    # @api.depend('partner_id')
    def _set_mobile(self):
        for record in self:
            record.mobile_hidden = record.mobile
            if record.partner_id:
                record.partner_id.write({'mobile': record.mobile_hidden})

    # phone = fields.Phone(string='Phone', related='partner_id.phone')
    # mobile = fields.Phone(string='mobile', related='partner_id.mobile')

