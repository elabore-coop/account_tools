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

        # search in account.cash.deposit if account move is this one
        for cash_deposit in self.env['account.cash.deposit'].search([]):
            if cash_deposit.move_id == self:
                print (cash_deposit.move_id, self)
                is_cash_deposit = True

        # search in account.check.deposit if account move is this one
        for check_deposit in self.env['account.check.deposit'].search([]):
            if check_deposit.move_id == self:
                is_check_deposit = True

        if (
            self.posted_before and
                (
                not is_cash_deposit
                and not is_check_deposit
                )
            ):
            raise UserError(_(""
                "You cannot delete this account move because it has been posted."
            ))
