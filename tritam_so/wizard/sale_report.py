# -*- coding: utf-8 -*-
from odoo import models, fields, api,_,exceptions
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning
import calendar
from datetime import datetime, timedelta, date
import odoo.addons.decimal_precision as dp


# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport_Inherit(models.Model):
    _inherit = "sale.report"

    x_status_do = fields.Selection([
        (1, 'Chưa xác nhận'),
        (2, 'Đơn hàng đang đi đường'),
        (3, 'Đơn hàng hoàn thành'),
        (7, 'Đơn hoàn'),
        ], string='Trạng thái vận chuyển',default=1,readonly=True)
    type_contact = fields.Selection([
        ('new', 'Contact mới'),
        ('reuse', 'Contact tái sử dụng'),
        ('contract', 'Contact tái ký'),
        ('sp', 'Contact CSKH')
    ],default=1,readonly=True)
    team_marketing = fields.Char('Team Marketing', readonly=True)
    source_customer = fields.Char('Nguồn', readonly=True)
    ratio_type_contact = fields.Float('Tỷ lệ doanh số hoàn đơn', readonly=True)


    def _select(self):
        return super(SaleReport_Inherit, self)._select() + ",s.x_status_do x_status_do,cl.type_contact type_contact"\
                                                           ",(case when s.x_status_do = 7 then ((l.price_subtotal /(select sum(l.price_subtotal) From sale_order_line l)*100)) else null end )  as ratio_type_contact " \
                                                           ",hrd.name team_marketing " \
                                                           ",cs.name as source_customer"

    def  _from(self):
        return super(SaleReport_Inherit, self)._from() + "left join  crm_lead cl on cl.id = s.opportunity_id " \
                                                         "left join customer_source  cs on partner.source_customer = cs.id " \
                                                         "left join hr_department hrd on cs.team_marketing = hrd.id " \


    def _group_by(self):
        return super(SaleReport_Inherit, self)._group_by() + ",x_status_do,type_contact,l.price_subtotal,hrd.name,cs.name"
