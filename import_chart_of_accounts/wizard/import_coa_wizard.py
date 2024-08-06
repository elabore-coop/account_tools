from odoo import models, fields, api, exceptions, _
import csv
import base64
from io import StringIO
from odoo.exceptions import UserError

class ImportCoaWizard(models.TransientModel):
    _name = 'import.coa.wizard'

    coa_file = fields.Binary(string='CSV File', required=True)
    filename = fields.Char(string='Filename')

    def import_plan_comptable(self):
        self.ensure_one()
        if not self.coa_file:
            raise UserError("Please upload a file.")

        if self.filename and not self.filename.lower().endswith('.csv'):
            raise UserError("Import COA Wizard only supports CSV")

        file_content = base64.b64decode(self.coa_file).decode('utf-8')
        csv_file = StringIO(file_content)
        csv_reader = csv.DictReader(csv_file)

        required_columns = ['code', 'name']
        if not all(column in csv_reader.fieldnames for column in required_columns):
            raise UserError(f"The CSV file must contain the following columns: {', '.join(required_columns)}")

        data_to_import = [row for row in csv_reader]

        #get all accounts already existing
        all_existing_accounts = self.rstrip_all_accounts()

        for record_data in data_to_import:
            # Verify if a identical account already exists in the COA
            # Example: 701000 and 70100000 are identical, but 701000 and 70100001 are not.
            identical_account_id = self.find_identical_account(all_existing_accounts, record_data['code'])
            if identical_account_id:
                existing_account = self.env['account.account'].browse(identical_account_id)
                existing_account.write(record_data)
            else:
                # find the closest account already existing in Odoo, it has the same first tree digits
                # Example : 706100 is the closest account of 706600
                closest_account = self.find_account_with_same_firsts_digits(record_data['code'][:3])
                if closest_account :
                    record_data['account_type'] = closest_account.account_type
                    record_data['reconcile'] = closest_account.reconcile
                new_account = self.env['account.account'].create(record_data)

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.account",
            "view_mode": "list"
            }

    def find_account_with_same_firsts_digits(self, code_prefix):
        """
        Find an account with the same initial digits of the code.
        
        :param code_prefix: The initial digits of the code to search for.
        :return: The first account found with the same prefix, or None if none is found.
        """
        return self.env['account.account'].search([('code', '=like', f'{code_prefix}%')],limit=1)

    def find_identical_account(self, all_accounts_without_final_zero, code):
        """
        Compare the account code to import with existing accounts stored in Odoo.

        Because 701000 and 70100000 are considered identical, we need to compare their account codes without final zeros.

        Example: 701000 and 70100000 are identical, but 701000 and 70100001 are not.

        Return: The ID of the identical account if it exists; otherwise, return False.
        """
        code_strip = code.rstrip('0')
        for account_id, stripped_code in all_accounts_without_final_zero.items():
            if stripped_code == code_strip:
                return account_id
        else:
            return False

    def rstrip_all_accounts(self):
        """
        Create a dictionary with IDs and acccount codes without trailing zeros for all existing accounts in Odoo.

        :return: A dictionary with account IDs as keys and codes without trailing zeros as values.
        """
        all_accounts_without_final_zero = {}
        accounts = self.env['account.account'].search([])
        for account in accounts:
            code = account.code
            account_id = account.id
            all_accounts_without_final_zero[account_id] = code.rstrip('0')
        return all_accounts_without_final_zero





