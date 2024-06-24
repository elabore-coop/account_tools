{
    'name': 'Import chart of accounts',
    'version': '16.0.1.1.0',
    'summary': 'while importing the accounts chart, only update account name  of existing accounts and automatise settings for new accounts',
    'description': '',
    'author': '',
    'website': '',
    'license': 'AGPL-3',
    'category': '',
    'depends': [
        'account'
    ],
    'data': [
        'wizard/import_coa_wizard_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
    'assets': {
    }
}


