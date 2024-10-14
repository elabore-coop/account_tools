# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountInvoiceSend(models.TransientModel):
    _inherit = 'account.invoice.send'

    def send_and_print_action(self):
        if self.model == "account.move":
            move = self.env[self.model].browse(self.res_id)
            move.sent_by_email = True

        return super(AccountInvoiceSend, self).send_and_print_action()