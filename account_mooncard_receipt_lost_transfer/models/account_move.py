from odoo import fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    receipt_lost = fields.Boolean(string=_("Receipt lost"), store=True)
    mooncard_record = fields.Boolean(store=True)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    receipt_lost = fields.Boolean(string=_("Receipt lost"), store=True)
    mooncard_record = fields.Boolean(store=True)
