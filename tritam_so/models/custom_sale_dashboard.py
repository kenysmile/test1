# -*- coding: utf-8 -*-
from json import dumps
from odoo import api, fields, models
import datetime
from datetime import timedelta
from .embed_question_metabase import embed_question_metabase

class CustomSalesDashboard(models.Model):
    _name = "custom.sale.dashboard"

    name = fields.Char("Tên báo cáo")
    title = fields.Char("Tên hiển thị")
    color = fields.Integer("Color Index")
    sequence = fields.Integer('Thứ tự')
    kanban_type = fields.Selection([('graph', 'Đồ thị'), ('figure', 'Số liệu'),], "Loại kanban")

    metabase_iframe = fields.Char('METABASE_IFRAME_URL', compute='_compute_metabase_iframe')
    iframe_height = fields.Integer('IFRAME_HEIGHT (pixel)')
    metabase_question_id = fields.Integer('Metabase Question ID')

    # kanban_type: FIGURE
    figure_type = fields.Selection([
        ('mission', 'Nhiệm vụ'),
        ('kpi_summation', 'Tổng kết KPI'),
    ], "Loại số liệu")
    # kanban_type: FIGURE | figure_type: mission
    today_contact_count = fields.Integer('Tổng số liên hệ cần gọi trong ngày', compute='_compute_today_contact_count')
    today_contact_done_count = fields.Integer('Tổng số liên hệ đã gọi trong ngày',
                                              compute="_compute_today_contact_done_count")
    # kanban_type: FIGURE | figure_type: kpi_summation
    kpi_target_count = fields.Integer('KPI cần đạt')
    kpi_rate_count = fields.Float('Phần trăm (%) KPI đạt được')

    @api.one
    def _compute_metabase_iframe(self):
        teamids = []
        crm_team_record = self.env['crm.team'].search([])
        for record in crm_team_record:
            if record.name:
                teamids.append(record.name.encode("utf-8"))
        param = {
            'Teamids': teamids,
        }
        metabase_secret_key =  self.env['ir.values'].get_default('sales.config.settings','metabase_secret_key')
        metabase_site_url = self.env['ir.values'].get_default('sales.config.settings','metabase_site_url')
        if metabase_secret_key and metabase_site_url and self.metabase_question_id:
            self.metabase_iframe = embed_question_metabase(ID=self.metabase_question_id,METABASE_SITE_URL=metabase_site_url,
                                                           METABASE_SECRET_KEY=metabase_secret_key, param=param)
        else:
            self.metabase_iframe = False
    @api.one
    def _compute_today_contact_count(self):
        today = (datetime.date.today() + timedelta(hours=7)).strftime('%Y-%m-%d')
        contact_opp_negative_1 = self.env['crm.lead'].search([('stage_id.status_opp', '=', '-1')])
        contact_opp_1_noactive = self.env['crm.lead'].search(
            [('stage_id.status_opp', '=', '1'), ('date_action', '=', today)])
        contact_opp_1_active = self.env['crm.lead'].search(
            [('stage_id.status_opp', '=', '1'), ('date_action', '=', False)])
        self.today_contact_count = len(contact_opp_1_active | contact_opp_1_noactive | contact_opp_negative_1)

    @api.one
    def _compute_today_contact_done_count(self):
        today = (datetime.date.today() + timedelta(hours=7)).strftime('%Y-%m-%d')
        contact_opp_negative_1 = self.env['crm.lead'].search(
            [('stage_id.status_opp', '=', '-1'), ('day_log_activity', '=', today)])
        contact_opp_1_noactive = self.env['crm.lead'].search(
            [('stage_id.status_opp', '=', '1'), ('date_action', '=', today), ('day_log_activity', '=', today)])
        contact_opp_1_active = self.env['crm.lead'].search(
            [('stage_id.status_opp', '=', '1'), ('date_action', '=', False), ('day_log_activity', '=', today)])
        self.today_contact_done_count = len(contact_opp_1_active | contact_opp_1_noactive | contact_opp_negative_1)

    @api.multi
    def open_pipeline(self):
        return self.env['crm.team'].action_your_pipeline();
