# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    report_note = fields.Html("Note")
