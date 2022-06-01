# -*- coding: utf-8 -*-
import logging

from bdb import set_trace
from odoo import models, fields, _

_logger = logging.getLogger(__name__)


class BudgetForecastModelChoice(models.Model):
    _name = "budget.forecast.model.choice"
    _description = _name

    budget_forecast_model = fields.Many2one("budget.forecast.model")

    def create_budget_forecast_lines(self):
        analytic_account = self.env["account.analytic.account"].browse(
            self._context.get("active_ids")
        )
        # Budget line deletion must be done in a precise order to avoid trying to unlink already deleted lines.
        # 1. Delete summary lines to remove all the linked section and subsection lines
        for line in analytic_account.budget_forecast_ids.filtered(
            lambda r: r.is_summary
        ):
            _logger.debug("SUMMARY BUDGET LINE = %s", line.name)
            line.unlink()

        # 2. Delete article and note lines
        for line in analytic_account.budget_forecast_ids.filtered(
            lambda r: r.display_type in ["line_article", "line_note"]
        ):
            _logger.debug("OTHER BUDGET LINE = %s", line.name)
            line.unlink()

        if self.budget_forecast_model:
            # Create new summary lines
            section_model_lines = self.env["budget.forecast.model.line"].search(
                [
                    ("budget_model", "=", self.budget_forecast_model.id),
                    ("display_type", "=", "line_section"),
                ]
            )
            sequence = 0
            for section in section_model_lines:
                vals = {
                    "analytic_id": self.env["account.analytic.account"]
                    .browse(self._context.get("active_ids"))
                    .id,
                    "display_type": "line_section",
                    "product_id": section.product_id.id,
                    "description": section.name,
                    "is_summary": True,
                    "sequence": sequence,
                }
                section_line = self.env["budget.forecast"].create(vals)
                sequence += 1
                if section.child_ids:
                    for sub_section in section.child_ids:
                        vals = {
                            "analytic_id": self.env["account.analytic.account"]
                            .browse(self._context.get("active_ids"))
                            .id,
                            "display_type": "line_subsection",
                            "product_id": sub_section.product_id.id,
                            "description": sub_section.name,
                            "is_summary": True,
                            "parent_id": section_line.id,
                            "sequence": sequence,
                        }
                        self.env["budget.forecast"].create(vals)
                        sequence += 1
