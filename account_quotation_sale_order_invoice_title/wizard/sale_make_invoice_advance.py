# -*- coding: utf-8 -*-

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, so_line):
        res = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, so_line
        )
        res["move_title"] = order.so_title
        return res
