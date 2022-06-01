# -*- coding: utf-8 -*-

from odoo import models, fields, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    budget_level = fields.Selection(
        [
            ("line_section", "Section"),
            ("line_subsection", "Sub-Section"),
            ("line_article", "Article"),
        ],
        string="Budget level",
        default="line_article",
    )
