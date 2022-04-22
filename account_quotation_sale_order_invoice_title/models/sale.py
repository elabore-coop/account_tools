# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    so_title = fields.Char(string="Title")

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        res["move_title"] = self.so_title
        return res
