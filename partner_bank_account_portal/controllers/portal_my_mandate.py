# Copyright 2024 Lokavaluto ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import http, tools, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class CustomerPortalMandate(CustomerPortal):

    def _mandate_get_page_view_values(self, mandate, access_token, **kwargs):
        values = {
            "page_name": "mandate",
            "mandate": mandate,
        }
        return self._get_page_view_values(
            mandate, access_token, values, "my_mandates_history", False, **kwargs
        )

    def _details_mandate_form_validate(self, data, mandate_id):
        error = dict()
        error_message = []
        # public name uniqueness
        if data.get("public_name") and request.env["res.partner"].sudo().search(
            [
                ("name", "=", data.get("public_name")),
                ("is_public_profile", "=", True),
                ("contact_id", "!=", mandate_id),
            ]
        ):
            error["public_name"] = "error"
            error_message.append(
                _("This public name is already used, please find an other idea.")
            )

        # email validation
        if data.get("email") and not tools.single_email_re.match(data.get("email")):
            error["email"] = "error"
            error_message.append(
                _("Invalid Email! Please enter a valid email address.")
            )
        return error, error_message

    def _get_mandate_fields(self):
        fields = [
            "unique_mandate_reference",
            "signature_date",
            "last_debit_date",
            "state",
        ]
        return fields

    def _transform_in_res_partner_fields(self, kw, mandate_fields, prefix=""):
        '''Transforms kw's values in res_partner fields and values'''
        return {key[len(prefix):]: kw[key] for key in mandate_fields if key in kw}

    def _get_page_saving_mandate_values(self, kw):
        mandate_fields = self._get_mandate_fields()
        values = self._transform_in_res_partner_fields(kw, mandate_fields)
        return values

    def _get_page_opening_values(self):
        # Just retrieve the values to display for Selection fields
        countries = request.env["res.country"].sudo().search([])
        values = {
            "countries": countries,
        }
        return values

    @http.route(
        ["/my/mandate/<int:mandate_id>", "/my/mandate/save"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_mandate(
        self,mandate_id=None, access_token=None, redirect=None, **kw
    ):
        if not isinstance(mandate_id, int):
            mandate_id = int(mandate_id)
        try:
            mandate_sudo = self._document_check_access(
                "account.banking.mandate", mandate_id, access_token
            )
        except (AccessError, MissingError):
            return request.redirect("/my/mandates")

        Mandate = request.env["account.banking.mandate"]
        user = request.env.user
        mandate = Mandate.browse(mandate_id)

        values = self._mandate_get_page_view_values(mandate_sudo, access_token, **kw)
        values.update(
            {
                "error": {},
                "error_message": [],
            }
        )
        if kw and request.httprequest.method == "POST":
            # the user has clicked in the Save button to save new data
            error, error_message = self._details_mandate_form_validate(kw, mandate_id)
            values.update({"error": error, "error_message": error_message})
            values.update(kw)
            if not error:
                new_values = self._get_page_saving_mandate_values(kw)
                mandate.sudo().write(new_values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect("/my/mandates")

        # This is just the form page opening. We send all the data needed for the form fields
        can_edit_mandate = user.partner_id == mandate.partner_id
        values.update(self._get_page_opening_values())
        values.update(
            {
                "mandate_id": mandate_id, # Sent in order to retrieve it at submit time
                "can_edit_mandate": can_edit_mandate,
                "redirect": "/my/mandate/" + str(mandate_id) + "?success=True"
            }
        )
        return request.render("partner_bank_account_portal.portal_my_mandate", values) #TODO créer le template portal_my_bank_account.xml
