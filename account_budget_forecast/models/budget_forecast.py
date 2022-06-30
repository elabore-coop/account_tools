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
        index=True,
        copy=True,
    )
    analytic_tag = fields.Many2one(
        "account.analytic.tag",
        "Analytic tag",
        index=True,
        copy=False,
        ondelete="cascade",
    )

    budget_category = fields.Selection(
        [
            ("manpower", "Manpower"),
            ("material", "Material"),
            ("equipment", "Equipment"),
            ("subcontractors", "Subcontractors"),
            ("delivery", "Delivery"),
            ("miscellaneous", "Miscellaneous"),
            ("unplanned", "Unplanned"),
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
        record.analytic_tag = self.env["account.analytic.tag"].create(
            {"name": record._calculate_name()}
        )
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
                if record.display_type in [
                    "line_section",
                    "line_subsection",
                ]:
                    if record.is_summary:
                        domain = [("summary_id", "=", record.id)]
                    else:
                        domain = [
                            ("id", "!=", record.id),
                            "|",
                            ("summary_id", "=", record.summary_id.id),
                            ("id", "=", record.summary_id.id),
                        ]
                    # find similar section/sub_section lines
                    lines = record.env["budget.forecast"].search(domain)
                    for line in lines:
                        line.unlink(True)
        res = super(BudgetForecast, self).unlink()
        return res

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            self.description = self.product_id.name
            self._calc_plan_price(True)
        else:
            self.description = ""
            self.plan_price = 0

    def _get_budget_category_label(self):
        categories = dict(self._fields["budget_category"].selection)
        for key, val in categories.items():
            if key == self.budget_category:
                return val
        return ""

    def _calculate_name(self):
        for record in self:
            name = (
                record.description
                + " - "
                + record.product_id.name
                + " - "
                + record._get_budget_category_label()
                + " - "
                + record.analytic_id.name
            )
            return name

    @api.onchange("description", "product_id")
    def _compute_name(self):
        for record in self:
            if record.product_id:
                values = {"name": record._calculate_name()}
                record.write(values, False)

    @api.onchange("name")
    def _compute_analytic_tag_name(self):
        for record in self:
            if record.analytic_tag:
                record.analytic_tag.name = record.name

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
            modulo = record.plan_amount_with_coeff % 100
            if (modulo > 0) and (modulo < 25):
                record.plan_amount_with_coeff = record.plan_amount_with_coeff - modulo
            elif (modulo >= 25) and (modulo < 50):
                record.plan_amount_with_coeff = record.plan_amount_with_coeff + (
                    50 - modulo
                )
            elif (modulo > 50) and (modulo < 75):
                record.plan_amount_with_coeff = record.plan_amount_with_coeff - (
                    modulo - 50
                )
            elif (modulo >= 75) and (modulo < 100):
                record.plan_amount_with_coeff = record.plan_amount_with_coeff + (
                    100 - modulo
                )

    @api.depends("child_ids")
    def _calc_plan_qty(self):
        for record in self:
            if record.child_ids:
                record.plan_qty = sum(record.mapped("child_ids.plan_qty"))

    @api.depends("child_ids")
    def _calc_plan_price(self, product_change=False):
        for record in self:
            if record.display_type in ["line_section", "line_subsection"]:
                if record.child_ids:
                    lst = record.mapped("child_ids.plan_price")
                    if lst and (sum(lst) > 0):
                        record.plan_price = lst and sum(lst)
                elif product_change:
                    record.plan_price = record.product_id.standard_price
            elif product_change and (record.display_type == "line_article"):
                record.plan_price = self.product_id.standard_price
            elif record.display_type == "line_note":
                record.plan_price = 0.00

    def _find_analytic_lines(self, move_type, with_timesheets=False):
        self.ensure_one()
        if with_timesheets:
            domain = [
                "|",
                (
                    "move_id.move_id.move_type",
                    "in",
                    move_type,
                ),
                ("timesheet_entry", "=", True),
            ]
        else:
            domain = [
                (
                    "move_id.move_id.move_type",
                    "in",
                    move_type,
                )
            ]
        analytic_lines = (
            self.env["account.analytic.line"]
            .search(domain)
            .filtered(lambda x: self.analytic_tag in x.tag_ids)
        )
        return analytic_lines

    def _find_draft_invoice_lines(self, move_type):
        self.ensure_one()
        domain = [
            ("analytic_account_id", "=", self.analytic_id.id),
            ("parent_state", "in", ["draft"]),
            ("move_id.move_type", "in", move_type),
        ]
        invoice_lines = (
            self.env["account.move.line"]
            .search(domain)
            .filtered(lambda x: self.analytic_tag in x.analytic_tag_ids)
        )
        return invoice_lines

    @api.depends("analytic_id.line_ids.amount")
    def _calc_actual(self):
        for record in self:
            # Section or Sub-section
            if record.display_type in ["line_section", "line_subsection"]:
                if record.child_ids:
                    # Actual expenses are calculated with the child lines
                    record.actual_amount = sum(record.mapped("child_ids.actual_amount"))

                    # Incomes are calculated with the analytic lines
                    line_ids = record._find_analytic_lines(
                        ["out_invoice", "out_refund", "out_receipt"]
                    )
                    record.incomes = sum(line_ids.mapped("amount"))
                    # Add Draft Invoice lines ids to incomes
                    invoice_lines = record._find_draft_invoice_lines(
                        ["out_invoice", "out_refund"]
                    )
                    for invoice_line in invoice_lines:
                        if invoice_line.move_id.move_type == "out_invoice":
                            record.incomes = (
                                record.incomes + invoice_line.price_subtotal
                            )
                        elif invoice_line.move_id.move_type == "out_refund":
                            record.incomes = (
                                record.incomes - invoice_line.price_subtotal
                            )
                    record.balance = record.incomes - record.actual_amount

            # Note
            elif record.display_type == "line_note":
                record.actual_amount = 0.00

            # Product
            else:
                line_ids = record._find_analytic_lines(
                    ["in_invoice", "in_refund", "in_receipt"], True
                )
                record.actual_amount = -sum(line_ids.mapped("amount"))

                # Add Draft Invoice lines ids
                invoice_lines = record._find_draft_invoice_lines(
                    ["in_invoice", "in_refund"]
                )
                for invoice_line in invoice_lines:
                    if invoice_line.move_id.move_type == "in_invoice":
                        record.actual_amount = (
                            record.actual_amount + invoice_line.price_subtotal
                        )
                    elif invoice_line.move_id.move_type == "in_refund":
                        record.actual_amount = (
                            record.actual_amount - invoice_line.price_subtotal
                        )

                record.incomes = None
                record.balance = None

            record.diff_expenses = record.plan_amount_with_coeff - record.actual_amount

    def action_view_analytic_lines(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "analytic.account_analytic_line_action_entries"
        )
        action["domain"] = [("tag_ids", "ilike", self.analytic_tag.id)]
        return action
