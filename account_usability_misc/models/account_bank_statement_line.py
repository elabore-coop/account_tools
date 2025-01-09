from odoo import fields, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    move_line_journal_type = fields.Char(string="Journal Type", compute="_compute_move_line_journal_type")

    def _compute_move_line_journal_type(self):
        for rec in self:
            if self._context.get('default_journal_id'):
                rec.move_line_journal_type = self.env["account.journal"].browse(self._context.get('default_journal_id')).type
            else:
                rec.move_line_journal_type = None
