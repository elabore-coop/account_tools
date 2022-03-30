from odoo import models


class NewgenPaymentCardTransaction(models.Model):
    _inherit = "newgen.payment.card.transaction"

    def process_line(self):
        res = super(NewgenPaymentCardTransaction, self).process_line()
        if res:
            for line in self:
                if line.invoice_id:
                    line.invoice_id.receipt_lost = line.receipt_lost
                    line.invoice_id.mooncard_record = True
                    move_lines = line.invoice_id.line_ids
                    for move_line in move_lines:
                        move_line.receipt_lost = line.receipt_lost
                        move_line.mooncard_record = True

        return res

    def generate_bank_journal_move(self):
        bank_move = super(
            NewgenPaymentCardTransaction, self
        ).generate_bank_journal_move()
        if bank_move:
            for line in bank_move.line_ids:
                line.receipt_lost = self.receipt_lost
                line.mooncard_record = True
        return bank_move
