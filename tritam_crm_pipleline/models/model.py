# -*- coding: utf-8 -*-
from odoo import models, fields, api,tools,_
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class Duoc_Crm_Lead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def get_date(self):
        import datetime
        return datetime.date.today()

    date_create = fields.Date(default=get_date)
    product_id = fields.Many2one('product.product', string="Sản phẩm")

    @api.constrains('phone', 'a')
    def check(self):
        # list_a = []
        check_ids = self.search([('phone' ,'=', self.phone)])
        # print(self.phone_hidden)
        print(check_ids)
        for i in check_ids:
            print(i)
        # for check_id in check_ids:
        #     # list_a.append(check_id.phone)
        #     # print(list_a)
        #     # print(self.phone)
        #     # print(check_id)
        #     print(check_id)
            if self.phone == '123':
                raise UserError(_("Trùng SÐT à sản phẩm"))

    @api.multi
    def schedule_reject_ticket(self):
        today = datetime.strptime(fields.Datetime.now(),tools.DEFAULT_SERVER_DATETIME_FORMAT)
        obj_crm_stage = self.env['crm.stage'].search([('probability','=',100)])
        obj_crm_lead = self.search([('active','=',True),('stage_id.id','not in',obj_crm_stage.ids),('type_contact','not in',['sp'])])
        reason = self.env['crm.lost.reason'].search([('type_state', '=', 1)], limit=1)
        day_new_contact = self.env['res.automatic.share.settings'].sudo().search([])[0].conf_new_contact
        day_re_use = self.env['res.automatic.share.settings'].sudo().search([])[0].conf_re_use
        number_re_sign = self.env['res.automatic.share.settings'].sudo().search([])[0].conf_re_sign
        list_ticket_apply = []
        list_res_partner = []
        if reason:
            id_reason = reason.id
        else:
            raise UserError(_("Chưa cài đặt loại cho một lý do là Quá Hạn"))
        for rec in obj_crm_lead :
            number_day = day_re_use if rec.type_contact == "reuse" else number_re_sign if rec.type_contact == "contract" else day_new_contact
            create_date = datetime.strptime(rec.create_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
            real_date = create_date + timedelta(days=number_day)
            if (real_date - today ).days < 0 :
                list_ticket_apply.append(rec.id)
                rec.action_set_lost()
                if len(rec.partner_id.ids)>0:
                    list_res_partner.append(rec.partner_id.id)
        if(list_ticket_apply):
            self.env.cr.execute("""UPDATE crm_lead SET lost_reason = %s WHERE id in %s""" % (id_reason, tuple(list_ticket_apply)))
        if(list_res_partner):
            self.env.cr.execute("""UPDATE res_partner SET reuse = '%s' WHERE id in %s""" % ('yes',tuple(list_res_partner)))


class CrmLeadLostInherit(models.TransientModel):
    _inherit = 'crm.lead.lost'

    @api.multi
    def action_lost_reason_apply(self):
        res = super(CrmLeadLostInherit, self).action_lost_reason_apply()
        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
        reason_name = self.lost_reason_id.name or ""
        body_html_partner = "<div><ul>" \
                            "<li>Thất Bại</li>" \
                            "<li>{sale_man} : {time}</li>" \
                            "<li>Lý Do: {activity}</li>" \
                            "</ul></div>".format(sale_man=self.env.user.name.encode('utf-8'), time=fields.Date.today(),
                                                 activity=reason_name.encode('utf-8'))
        leads.partner_id.message_post(body_html_partner)
        if self.lost_reason_id and self.lost_reason_id.type_state == 2 and len(leads.partner_id.ids) > 0:
                leads.partner_id.write({'active': False})
        return res

class CrmStageInherit(models.Model):
    _inherit = "crm.stage"
    _sql_constraints = [
        ('type_stage', 'unique (type_state)', 'Loại trạng thái đã tồn tại'),
    ]
    type_state = fields.Selection([
        (1, 'Đơn đã bị huỷ'),
        (2, 'Đơn xác nhận'),
        (3, 'Đơn đang đi trên đường'),
        (4, 'Đơn hàng hoàn thành'),
        (5, 'Đơn hoàn')
    ], string='Loại trạng thái')
        # for rec in obj_crm_lead:
class CrmLeadLostReasonInherit(models.Model):
    _inherit = 'crm.lost.reason'
    _sql_constraints = [
        ('type_stage', 'Check(1=1)', 'Loại lý do đã tồn tại'),
    ]
    type_state = fields.Selection([
        (1, 'Quá Hạn'),
        (2, 'Không tái phân bổ'),
    ], string='Loại')

    @api.constrains('type_state')
    def _check_type_state(self):
        if self.type_state == 1 :
            obj_lost = self.search([('type_state','=',1)])
            if obj_lost :
                raise UserError(_("Loại lý do Quá Hạn đã tồn tại"))
