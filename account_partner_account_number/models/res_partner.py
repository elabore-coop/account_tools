from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    account_code = fields.Char('Account code')

    _sql_constraints = [
        ('account_coder_unique', 
        'unique(account_code)',
        'Choose another value of account code - it has to be unique!')
    ]
