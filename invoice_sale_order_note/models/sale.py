# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.addons.sale.models.sale_order import LOCKED_FIELD_STATES


class SaleOrder(models.Model):
    _inherit = "sale.order"

    report_note = fields.Html("Note", states=LOCKED_FIELD_STATES,)

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res["report_note"] = self.report_note
        return res
