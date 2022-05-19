# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    budget_forecast_id = fields.Many2one("budget.forecast")

    # def _timesheet_preprocess(self, vals):
    #     vals = super(AccountAnalyticLine, self)._timesheet_preprocess(vals)
    #     if vals.get("so_line") and not vals.get("product_id"):
    #         so_line = self.env["sale.order.line"].browse(vals["so_line"])
    #         vals["product_id"] = so_line.product_id.id
    #     if vals.get("employee_id") and not vals.get("product_id"):
    #         employee = self.env["hr.employee"].browse(vals["employee_id"])
    #         vals["product_id"] = employee.timesheet_product_id.id
    #     return vals
