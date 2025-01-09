{
    'name': 'Account Usability Misc',
    'version': '16.0.1.3.0',
    'description': 'account usability misc : improve account usability in v16',
    'summary': 'Various chantes to improve the usability of Account application',
    'author': 'Elabore',
    'website': 'https://elabore.coop/',
    'license': 'AGPL-3',
    'category': 'Accounting',
    'depends': [
        'account','base','account_reconcile_oca',
        'account_check_deposit','account_cash_deposit',
        'account_statement_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_search.xml',
        'views/account_menu.xml',
        'views/account_tree_view.xml',
        "views/bank_statement_line_views.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'assets': {
    }
}
