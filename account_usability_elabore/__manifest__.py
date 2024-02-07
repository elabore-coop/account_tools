{
    'name': 'Account Usability Elabore',
    'version': '16.0.1.1.0',
    'description': 'account usability Elabore : improve account usability in v16',
    'summary': '',
    'author': '',
    'website': '',
    'license': 'AGPL-3',
    'category': '',
    'depends': [
        'account','base','account_reconcile_oca','account_check_deposit','account_cash_deposit'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_search.xml',
        'views/account_menu.xml',
        'views/account_tree_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'assets': {
        
    }
}
