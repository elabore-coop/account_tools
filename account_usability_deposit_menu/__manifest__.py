{
    'name': 'Account Usability Deposit Menu',
    'version': '16.0.1.0.0',
    'description': 'Create Deposit menu',
    'summary': 'Brings together the check and the cash deposit submenus under a common Deposit menu ',
    'author': 'Elabore',
    'website': 'https://elabore.coop/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'depends': [
        'account_check_deposit',
        'account_cash_deposit',
    ],
    'data': [
        'views/account_menu.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': False,
    'assets': {
    }
}
