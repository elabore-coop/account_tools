# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    budget_forecast_id = fields.Many2one("budget.forecast")

    @api.depends("budget_forecast_id")
    def _transfer_budget_forecast_line(self):
        for record in self:
            record.analytic_line_ids.budget_forecast_id = record.budget_forecast_id.id
