# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class Lead2OpportunityMassConvert(models.TransientModel):

    _inherit = 'crm.lead2opportunity.partner.mass'

    @api.onchange('team_id')
    def set_domain_user_ids(self):
        return {'domain': {'user_ids': [('user_ids', 'in', self.team_id.member_ids.ids)]}}

    @api.multi
    def mass_convert(self):
        selected_id = self._context.get('active_ids', [])
        for id in selected_id:
            lead = self.env['crm.lead'].browse(id)
            lead.user_id = self.user_ids[0]
        return super(Lead2OpportunityMassConvert, self).mass_convert()
