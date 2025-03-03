{
    'name': 'Account Usability Misc POS',
    'version': '16.0.2.0.0',
    'description': 'Prevent deleting account bank statement et account bank statement line throught POS',
    'summary': 'if Account Usability Misc and POS are installed, autoinstalle Account Usability Misc POS to prevent deleting account bank statement and account bank statement line throught POS manager rights',
    'author': 'Elabore',
    'website': 'https://elabore.coop/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'depends': [
        'account_usability_misc','point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'assets': {
    }
}
