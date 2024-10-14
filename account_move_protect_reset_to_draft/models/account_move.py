from odoo import models, api, _, fields
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    sent_by_email = fields.Boolean()
    
    def button_draft(self):
        res = super(AccountMove, self).button_draft()
        if self.sent_by_email:
            raise UserError(_(
                "You cannot reset to draft this invoice because it has been sent by email."
            ))
        return res
