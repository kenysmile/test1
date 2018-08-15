# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReportLeadMaketing(models.Model):
    _name = "sale.report.lead.marketing"
    _description = "Sales Orders Statistics"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    date = fields.Datetime('Date Create', readonly=True)
    team_marketing = fields.Char('Team Marketing', readonly=True)
    total_amount = fields.Float('Chi phí', readonly=True)
    cost_contact = fields.Float('Chi phí / Contact', readonly=True)
    partner_name = fields.Char('Khách hàng', readonly=True)
    nbr = fields.Integer('Số Khách Hàng', readonly=True)
    def _select(self):
        select_str = """
        With total as (
             WITH tmp as (SELECT hrs.id id,max(partner.id) partner_id
            From res_partner partner
            inner join customer_source  cs on partner.source_customer = cs.id 
            inner join hr_department hrd on cs.team_marketing = hrd.id 
            inner join hr_expense_sheet hrs on hrs.department_id = hrd.id 
            and partner.create_date::date = hrs.accounting_date
            where partner.active = true and partner.customer = true and partner.parent_id is null
            GROUP BY hrs.id
            )
            SELECT  partner.id id,partner.name partner_name,partner.create_date::date date,hrd.name team_marketing
            ,sum(hrs.total_amount) total_amount
            --,(sum(hrs.total_amount)/count(partner.id)) cost_contact,count(partner.id)
            From 
            
            res_partner partner
            left join customer_source  cs on partner.source_customer = cs.id 
            left join hr_department hrd on cs.team_marketing = hrd.id 
            left join tmp tp on partner.id = tp.partner_id
            left join hr_expense_sheet hrs on hrs.id = tp.id 
            and partner.create_date::date = hrs.accounting_date
            where partner.active = true and partner.customer = true and partner.parent_id is null
        GROUP BY partner.id,partner.create_date::date,partner.name,hrd.name)
        Select min(id) id, date,team_marketing,sum(total_amount) total_amount ,(sum(total_amount)/count(team_marketing)) cost_contact,count(team_marketing) nbr
        """
        return select_str

    def _from(self):
        from_str = """
                total
        """
        return from_str

    def _where(self):
            where_str = """
              where team_marketing is not null
            """
            return where_str

    def _group_by(self):
        group_by_str = """
	        GROUP BY date,team_marketing
        """
        return group_by_str

    @api.model_cr
    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            )""" % (self._table, self._select(), self._from(),self._where(),self._group_by()))
