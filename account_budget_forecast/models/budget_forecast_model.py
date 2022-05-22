# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class BudgetForecastModel(models.Model):
    _name = "budget.forecast.model"
    _description = _name

    name = fields.Char("Name", copy=False)


class BudgetForecastModelLine(models.Model):
    _name = "budget.forecast.model.line"
    _description = _name

    budget_model = fields.Many2one("budget.forecast.model", copy=True)

    name = fields.Char("Name", copy=True)

    display_type = fields.Selection(
        [
            ("line_section", "Section"),
            ("line_subsection", "Sub-Section"),
        ],
        copy=True,
        store=True,
    )
    product_id = fields.Many2one(
        "product.product", copy=True, domain="[('budget_level', '=', display_type)]"
    )
    parent_id = fields.Many2one(
        "budget.forecast.model.line",
        store=True,
        copy=False,
    )
    child_ids = fields.One2many("budget.forecast.model.line", "parent_id", copy=False)
