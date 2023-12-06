# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ChorusFlow(models.Model):
    _inherit = "chorus.flow"

    def update_flow_status(self):
        res = super(ChorusFlow, self).update_flow_status()
        for flow in self:
            if flow.status == 'IN_REJETE':
                for invoice in flow.invoice_ids:
                    invoice.message_post(_("Chorus flow n°%s rejected.")%(flow.name,))
        return res