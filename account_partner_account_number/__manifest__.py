# -*- coding: utf-8 -*-
{
    "name": "Account partner account number",
    "category": "Account",
    "version": "14.0.1.0",
    "summary": "Add account number in partner",
    "author": "Elabore",
    "website": "https://elabore.coop/",
    "installable": True,
    "application": False,
    "auto_install": False,
    "description": """
======================================
Account partner account number
======================================
This module add a new field in partner, visible in account move lines for payable and receivable accounts

Installation
============
Just install account_partner_account_number, all dependencies will be installed by default.

Known issues / Roadmap
======================

Bug Tracker
===========
Bugs are tracked on `GitHub Issues
<https://github.com/elabore-coop/.../issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------
* Elabore: `Icon <https://elabore.coop/web/image/res.company/1/logo?unique=f3db262>`_.

Contributors
------------
* Clément Thoams

Funders
-------
The development of this module has been financially supported by:
* Elabore (https://elabore.coop)
* Rovalterre

Maintainer
----------
This module is maintained by ELABORE.

""",
    "depends": [
        "base",
        "account",        
    ],
    "data": [
        "views/account_move_views.xml",
        "views/partner_views.xml",
    ],
    "qweb": [],
}
