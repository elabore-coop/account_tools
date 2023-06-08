from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    account_number = fields.Char('Account number')
