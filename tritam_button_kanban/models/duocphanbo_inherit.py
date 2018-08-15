# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import logging


class Duocphanbo_inherit(models.Model):
    _inherit = 'res.automatic'

    @api.model
    def action_in(self):
        return super(Duocphanbo_inherit, self).action_in()

    @api.model
    def action_renew_rp(self):
        return super(Duocphanbo_inherit, self).action_renew_rp()

    @api.model
    def action_to_sign(self):
        return super(Duocphanbo_inherit, self).action_to_sign()

    @api.model
    def action_to_sp(self):
        return super(Duocphanbo_inherit, self).action_to_sp()