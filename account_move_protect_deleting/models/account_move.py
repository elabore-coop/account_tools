from odoo import models, api, _
from odoo.exceptions import UserError
import re

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.ondelete(at_uninstall=False)
    def _check_posted(self):
        """ Prevent deletion of a account move if it has been posted
            exeptions : Check deposit or Cash deposit. In V16 in odoo the account move is deleted
                        when the check deposit is reset to draft. 
                        This work the same with Cash deposit
        """

        pattern_CHQ_DEPOSIT = r"DEP\d{3}"
        pattern_CASH_DEPOSIT = r"CASH-DEP-\d{3}"

        if (
            self.posted_before and 
                ( 
                not re.search(pattern_CHQ_DEPOSIT, self.ref) 
                and not re.search(pattern_CASH_DEPOSIT, self.ref) 
                )
            ):
            raise UserError(_(""
                "You cannot delete this account move because it has been posted."
            ))
