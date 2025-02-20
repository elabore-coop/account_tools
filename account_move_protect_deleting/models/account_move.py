from odoo import models, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.ondelete(at_uninstall=False)
    def _check_posted(self):
        """ Prevent deletion of a account move if it has been posted
            exeptions : Check deposit or Cash deposit. In V16 in odoo the account move is deleted
                        when the check deposit is reset to draft.
                        This work the same with Cash deposit
        """
        for rec in self:

            is_cash_deposit = False
            is_check_deposit = False

            # search in account.cash.deposit if account move is this one
            if rec.env.get('account.cash.deposit'):
                for cash_deposit in rec.env['account.cash.deposit'].search([]):
                    if cash_deposit.move_id == rec:
                        print (cash_deposit.move_id, rec)
                        is_cash_deposit = True

            # # search in account.check.deposit if account move is this one
            if rec.env.get('account.check.deposit'):
                for check_deposit in rec.env['account.check.deposit'].search([]):
                    if check_deposit.move_id == rec:
                        is_check_deposit = True

            if (
                rec.posted_before and
                    (
                    not is_cash_deposit
                    and not is_check_deposit
                    )
                ):
                raise UserError(_(""
                    "You cannot delete this account move because it has been posted."
                ))
