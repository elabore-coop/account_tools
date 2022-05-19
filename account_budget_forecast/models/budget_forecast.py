# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class BudgetForecast(models.Model):
    _name = "budget.forecast"
    _description = _name

    name = fields.Char("Name", store=True)
    description = fields.Char("Description", copy=True)
    sequence = fields.Integer()
    analytic_id = fields.Many2one(
        "account.analytic.account",
        "Analytic Account",
        required=True,
        ondelete="restrict",
        index=True,
        copy=True,
    )

    budget_category = fields.Selection(
        [
            ("manpower", "Manpower"),
            ("material", "Material"),
            ("equipment", "Equipment"),
            ("subcontractors", "Subcontractors"),
            ("miscellaneous", "Miscellaneous"),
        ],
        string=_("Budget Category"),
    )
    is_summary = fields.Boolean(copy=False, default=False, store=True)
    summary_id = fields.Many2one("budget.forecast", store=True)
    display_type = fields.Selection(
        [
            ("line_section", "Section"),
            ("line_subsection", "Sub-Section"),
            ("line_article", "Article"),
            ("line_note", "Note"),
        ],
        copy=True,
        store=True,
    )

    product_id = fields.Many2one(
        "product.product", copy=True, domain="[('budget_level', '=', display_type)]"
    )

    plan_qty = fields.Float("Plan Quantity", copy=False)
    plan_price = fields.Float("Plan Price", default=0.00, copy=False)
    plan_amount_without_coeff = fields.Float(
        "Plan Amount", compute="_calc_plan_amount_without_coeff", store=True, copy=False
    )
    plan_amount_with_coeff = fields.Float(
        "Plan Amount with coeff",
        compute="_calc_plan_amount_with_coeff",
        store=True,
        copy=False,
    )

    analytic_line_ids = fields.One2many(
        "account.analytic.line", "budget_forecast_id", copy=False
    )
    actual_qty = fields.Float(
        "Actual Quantity",
        compute="_calc_actual",
        store=True,
        compute_sudo=True,
        copy=False,
    )
    actual_amount = fields.Float(
        "Expenses",
        compute="_calc_actual",
        store=True,
        compute_sudo=True,
        copy=False,
    )
    diff_expenses = fields.Float(
        "Diff", compute="_calc_actual", store=True, compute_sudo=True, copy=False
    )
    incomes = fields.Float(
        "Incomes",
        compute="_calc_actual",
        store=True,
        compute_sudo=True,
        copy=False,
    )
    balance = fields.Float(
        "Balance", compute="_calc_actual", store=True, compute_sudo=True, copy=False
    )
    parent_id = fields.Many2one(
        "budget.forecast", store=True, compute_sudo=True, compute="_calc_parent_id"
    )
    child_ids = fields.One2many("budget.forecast", "parent_id", copy=False)

    note = fields.Text(string="Note")

    ###################################################################################
    # Budget lines management
    ###################################################################################

    @api.model_create_multi
    @api.returns("self", lambda value: value.id)
    def create(self, vals_list):
        records = super(BudgetForecast, self).create(vals_list)
        for record in records:
            if not record.display_type:
                record.display_type = "line_article"
            elif record.is_summary and record.display_type in [
                "line_section",
                "line_subsection",
            ]:
                record._create_category_sections()
        return records

    def _create_category_sections(self):
        categories = dict(self._fields["budget_category"].selection)
        for category in categories:
            # Create other category lines
            values = {
                "budget_category": category,
                "summary_id": self.id,
                "is_summary": False,
            }
            self.copy(values)

    def write(self, vals, one_more_loop=True):
        res = super(BudgetForecast, self).write(vals)
        if one_more_loop:
            self._sync_sections_data()
        return res

    def unlink(self, child_unlink=False):
        parent_ids = self.mapped("parent_id")
        if not child_unlink:
            for record in self:
                if not record.is_summary and (
                    record.display_type
                    in [
                        "line_section",
                        "line_subsection",
                    ]
                ):
                    # find similar section/sub_section lines
                    lines = record.env["budget.forecast"].search(
                        [
                            "|",
                            ("summary_id", "=", record.summary_id.id),
                            ("id", "=", record.summary_id.id),
                        ]
                    )
                    for line in lines:
                        line.unlink(True)
        res = super(BudgetForecast, self).unlink()
        parent_ids.exists()._calc_plan()
        return res

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            if self.display_type == "line_article":
                self.plan_price = self.product_id.standard_price
            else:
                self._calc_plan_price()
        else:
            self.description = ""
            self.plan_price = 0
            if self.display_type != "line_article":
                self._calc_plan_price()

    def _get_budget_category_label(self):
        categories = dict(self._fields["budget_category"].selection)
        for key, val in categories.items():
            if key == self.budget_category:
                return val
        return ""

    @api.onchange("description", "product_id")
    def _compute_name(self):
        for record in self:
            if record.product_id:
                name = (
                    record.description
                    + " - "
                    + record.product_id.name
                    + " - "
                    + record._get_budget_category_label()
                    + " - "
                    + record.analytic_id.name
                )
                values = {
                    "name": name,
                }
                record.write(values, False)

    def _sync_sections_data(self):
        for record in self:
            if record.display_type in ["line_section", "line_subsection"]:
                if not record.is_summary:
                    # find corresponding line summary
                    summary_line = self.env["budget.forecast"].browse(
                        record.summary_id.id
                    )
                    values = {
                        "product_id": record.product_id.id,
                        "description": record.description,
                    }
                    summary_line.write(values, False)
                    summary_line._compute_name()

                # find similar category section/sub_section lines
                domain = [
                    ("is_summary", "=", False),
                    ("id", "!=", record.id),
                ]
                if not record.is_summary:
                    domain.extend([("summary_id", "=", record.summary_id.id)])
                else:
                    domain.extend([("summary_id", "=", record.id)])
                lines = self.env["budget.forecast"].search(domain)
                for line in lines:
                    values = {
                        "product_id": record.product_id.id,
                        "description": record.description,
                    }
                    line.write(values, False)
                    line._compute_name()

    @api.depends(
        "analytic_id.budget_forecast_ids", "sequence", "parent_id", "child_ids"
    )
    def _calc_parent_id(self):
        for record in self:
            if record.display_type == "line_section":
                # A Section is the top of the line hierarchy => no parent
                record.parent_id = False
                continue
            found = False
            parent_id = False
            for line in record.analytic_id.budget_forecast_ids.search(
                [
                    ("analytic_id", "=", record.analytic_id.id),
                    ("budget_category", "=", record.budget_category),
                ]
            ).sorted(key=lambda r: r.sequence, reverse=True):
                if not found and line != record:
                    continue
                if line == record:
                    found = True
                    continue
                if line.display_type in ["line_article", "line_note"]:
                    continue
                elif line.display_type == "line_subsection":
                    if record.display_type in ["line_article", "line_note"]:
                        parent_id = line
                        break
                    else:
                        continue
                elif line.display_type == "line_section":
                    parent_id = line
                    break
            record.parent_id = parent_id

    def refresh(self):
        self._calc_parent_id()
        self._calc_plan()
        self._calc_actual()

    ###################################################################################
    # Amounts calculation
    ###################################################################################

    def _calc_plan(self):
        self._calc_plan_qty()
        self._calc_plan_price()
        self._calc_plan_amount_without_coeff()
        self._calc_plan_amount_with_coeff()

    @api.depends("plan_qty", "plan_price", "child_ids")
    def _calc_plan_amount_without_coeff(self):
        for record in self:
            if record.child_ids:
                record.plan_amount_without_coeff = sum(
                    record.mapped("child_ids.plan_amount_without_coeff")
                )
            else:
                record.plan_amount_without_coeff = record.plan_qty * record.plan_price

    @api.depends("plan_qty", "plan_price", "child_ids")
    def _calc_plan_amount_with_coeff(self):
        for record in self:
            record.plan_amount_with_coeff = record.plan_amount_without_coeff * (
                1 + record.analytic_id.global_coeff
            )

    @api.depends("child_ids")
    def _calc_plan_qty(self):
        for record in self:
            if record.child_ids:
                record.plan_qty = sum(record.mapped("child_ids.plan_qty"))

    @api.depends("child_ids")
    def _calc_plan_price(self):
        for record in self:
            if record.display_type in ["line_section", "line_subsection"]:
                if record.child_ids:
                    lst = record.mapped("child_ids.plan_price")
                    if lst and (sum(lst) > 0):
                        record.plan_price = lst and sum(lst)
                    else:
                        record.plan_price = record.product_id.standard_price
                else:
                    record.plan_price = record.product_id.standard_price
            elif record.display_type == "line_note":
                record.plan_price = 0.00

    @api.depends("analytic_id.line_ids.amount")
    def _calc_actual(self):
        for record in self:
            if record.display_type in ["line_section", "line_subsection"]:
                if record.child_ids:
                    # Actual expenses are calculated with the child lines
                    record.actual_qty = sum(record.mapped("child_ids.actual_qty"))
                    record.actual_amount = sum(record.mapped("child_ids.actual_amount"))
                    # Incomes are calculated with the analytic lines
                    line_ids = record.analytic_line_ids.filtered(
                        lambda x: x.move_id.move_id.type
                        in ["out_invoice", "out_refund"]
                    )
                    record.incomes = sum(line_ids.mapped("amount"))

                    # Add Invoice lines ids
                    domain = [
                        ("analytic_account_id", "=", record.analytic_id.id),
                        ("parent_state", "in", ["draft", "posted"]),
                        ("budget_forecast_id", "=", record.id),
                        ("move_id.type", "in", ["out_invoice", "out_refund"]),
                    ]
                    invoice_lines = self.env["account.move.line"].search(domain)
                    for invoice_line in invoice_lines:
                        if invoice_line.move_id.type == "out_invoice":
                            record.incomes = (
                                record.incomes + invoice_line.price_subtotal
                            )
                        elif invoice_line.move_id.type == "out_refund":
                            record.incomes = (
                                record.incomes - invoice_line.price_subtotal
                            )
                    record.balance = record.incomes - record.actual_amount

            elif record.display_type == "line_note":
                record.actual_qty = 0
                record.actual_amount = 0.00
            else:
                line_ids = record.analytic_line_ids.filtered(
                    lambda x: x.move_id.move_id.type
                    not in ["out_invoice", "out_refund"]
                )
                record.actual_qty = abs(sum(line_ids.mapped("unit_amount")))
                record.actual_amount = -sum(line_ids.mapped("amount"))

                # Add Invoice lines ids
                domain = [
                    ("analytic_account_id", "=", record.analytic_id.id),
                    ("parent_state", "in", ["draft", "posted"]),
                    ("budget_forecast_id", "=", record.id),
                    ("move_id.type", "in", ["in_invoice", "in_refund"]),
                ]
                invoice_lines = self.env["account.move.line"].search(domain)
                for invoice_line in invoice_lines:
                    if invoice_line.move_id.type == "in_invoice":
                        record.actual_qty = record.actual_qty + invoice_line.quantity
                        record.actual_amount = (
                            record.actual_amount + invoice_line.price_subtotal
                        )
                    elif invoice_line.move_id.type == "in_refund":
                        record.actual_qty = record.actual_qty - invoice_line.quantity
                        record.actual_amount = (
                            record.actual_amount - invoice_line.price_subtotal
                        )

                record.incomes = None
                record.balance = None

            record.diff_expenses = record.plan_amount_with_coeff - record.actual_amount
