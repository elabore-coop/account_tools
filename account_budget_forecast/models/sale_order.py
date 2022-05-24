# -*- coding: utf-8 -*-

from odoo import models, fields, _, api
from odoo.exceptions import Warning


class SaleOrder(models.Model):
    _inherit = "sale.order"

    plan_amount_with_coeff = fields.Float(
        related="analytic_account_id.plan_amount_with_coeff"
    )

    def action_budget_forecast(self):
        if not self.analytic_account_id:
            raise Warning(_("Please set the analytic account"))
        return self.analytic_account_id.action_budget_forecast()

    def sync_missing_budget_lines(self):
        for record in self:
            for line in self.order_line:
                if not line.budget_forecast_id:
                    values = {
                        "analytic_id": record.analytic_account_id.id,
                        "product_id": line.product_id.id,
                        "description": line.name,
                        "is_summary": True,
                        "display_type": "line_section",
                        "sequence": 999,
                    }
                    budget_line = self.env["budget.forecast"].create(values)
                    misc_budget_line = self.env["budget.forecast"].search(
                        [
                            ("summary_id", "=", budget_line.id),
                            ("budget_category", "=", "miscellaneous"),
                        ]
                    )
                    misc_budget_line.plan_qty = 1
                    misc_budget_line.plan_price = line.price_unit / (
                        1 + record.analytic_account_id.global_coeff
                    )
                    line.budget_forecast_id = budget_line.id

    @api.returns("self", lambda value: value.id)
    def copy(self, default=None):
        record = super(SaleOrder, self).copy(default=default)
        if self.analytic_account_id.budget_forecast_ids:
            if self.name in self.analytic_account_id.name:
                name = self.analytic_account_id.name.replace(self.name, record.name)
            else:
                name = "%s: %s" % (self.analytic_account_id.name, record.name)
            record.analytic_account_id = self.analytic_account_id.copy(
                default=dict(name=name)
            )
        return record


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    budget_forecast_id = fields.Many2one("budget.forecast")
