# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_forecast_id = fields.Many2one("budget.forecast", store=True)
