from odoo import models, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.ondelete(at_uninstall=False)
    def _check_posted(self):
        """ Prevent deletion of a account move if it has been posted
        """

        if (self.posted_before):
            raise UserError(_(""
                "You cannot delete this account move because it has been posted."
            ))
