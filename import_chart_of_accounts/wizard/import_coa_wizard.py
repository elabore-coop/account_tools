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
        for record_data in data_to_import:
            existing_line = self.env['account.account'].search([('code', '=', record_data['code'])], limit=1)
            if existing_line:
                existing_line.name = record_data['name']
            else:
                closest_account = self.find_closest_account(record_data['code'][:3])
                if closest_account :
                    record_data['account_type'] = closest_account.account_type
                    record_data['reconcile'] = closest_account.reconcile
                new_account = self.env['account.account'].create(record_data)

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.account",
            "view_mode": "list"
            }
            
    def find_closest_account(self, code_prefix):
        # return first code with first tree caracters identical 
        return self.env['account.account'].search([('code', '=like', f'{code_prefix}%')],limit=1)
