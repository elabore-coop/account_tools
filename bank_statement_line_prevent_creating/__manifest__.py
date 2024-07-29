# Copyright  Elabore ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "bank statement lines : prevent creating",
    "version": "16.0.1.0.0",
    "author": "Elabore",
    "website": "https://elabore.coop",
    "maintainer": "Elabore",
    "license": "AGPL-3",
    "category": "Accounting",
    "summary": "Hide Create button in Bank Statement Line view without changing rights",
    # any module necessary for this one to work correctly
    "depends": [
        "base","account","account_statement_base","account_reconcile_oca",
    ],
    "qweb": [],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "views/bank_statement_line_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
    "js": [],
    "css": [],
    "installable": True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    "auto_install": False,
    "application": False,
}