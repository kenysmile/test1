# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReportRevenue(models.Model):
    _name = "sale.report.revenue"
    _description = "Sales Orders Statistics"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    date = fields.Datetime('Date Order', readonly=True)
    team_marketing = fields.Char('Team Marketing', readonly=True)
    total_amount = fields.Float('Chi phí', readonly=True)
    revenue_cost = fields.Float('Chi phí / Doanh thu hàng chuyển đi', readonly=True)
    revenue_cost_done = fields.Float('Chi phí / Doanh thu thành công', readonly=True)
    def _select(self):
        select_str = """
	with total as ( WITH tmp as (SELECT hrs.id id,max(s.id) so_id
        From sale_order s 
        join res_partner partner on s.partner_id = partner.id
        inner join customer_source  cs on partner.source_customer = cs.id 
        inner join hr_department hrd on cs.team_marketing = hrd.id 
        inner join hr_expense_sheet hrs on hrs.department_id = hrd.id 
        and s.date_order::date = hrs.accounting_date
        
        where hrs.total_amount is not null
        GROUP BY hrs.id
        )
        SELECT  s.date_order::date date ,sum(hrs.total_amount) total_amount,hrd.id marketting_id
        From   
        sale_order s 
        inner join res_partner partner on s.partner_id = partner.id
        inner join customer_source  cs on partner.source_customer = cs.id 
        inner join hr_department hrd on cs.team_marketing = hrd.id 
        inner join tmp tp on s.id = tp.so_id
        inner join hr_expense_sheet hrs on hrs.id = tp.id 
        and s.date_order::date = hrs.accounting_date
        group by hrd.id,s.date_order::date
        )
        SELECT marketting_id id,hr_depart.name team_marketing,date::date ,sum(total_amount) total_amount,((sum(total.total_amount)/sum(pit.price_subtotal))*100) revenue_cost ,
	    ((sum(total.total_amount)/sum(pit_done.price_subtotal))*100) revenue_cost_done
        """
        return select_str

    def _from(self):
        from_str = """
	           total left join
            (select sum(l.price_subtotal) price_subtotal,hrd.id team_makerting_id , s.date_order::date order_date  From sale_order_line l inner join sale_order s on (l.order_id=s.id)
            join res_partner partner on s.partner_id = partner.id
            inner join customer_source  cs on partner.source_customer = cs.id 
            inner join hr_department hrd on cs.team_marketing = hrd.id 
            where s.x_status_do = 2
            GROUP BY hrd.id,s.date_order::date
            ) pit on total.marketting_id = pit.team_makerting_id and total.date = pit.order_date
            left join 
            (select sum(l.price_subtotal) price_subtotal,hrd.id team_makerting_id ,s.date_order::date order_date From sale_order_line l inner join sale_order s on (l.order_id=s.id)
            join res_partner partner on s.partner_id = partner.id
            inner join customer_source  cs on partner.source_customer = cs.id 
            inner join hr_department hrd on cs.team_marketing = hrd.id 
            where s.x_status_do = 3
            GROUP BY hrd.id,s.date_order::date
            ) pit_done on total.marketting_id = pit_done.team_makerting_id and total.date = pit_done.order_date
            inner join hr_department hr_depart on total.marketting_id = hr_depart.id
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY marketting_id,date,hr_depart.name
        """
        return group_by_str

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM ( %s )
            %s
            )""" % (self._table, self._select(), self._from(), self._group_by()))
