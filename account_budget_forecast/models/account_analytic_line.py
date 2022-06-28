# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    timesheet_entry = fields.Boolean(
        help="Technical field to identify analytic lines created from timesheet vies",
        store=True,
        default=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(AccountAnalyticLine, self).create(vals_list)
        for line, values in zip(lines, vals_list):
            if line.project_id:  # applied only for timesheet
                line.timesheet_entry = True
        return lines
