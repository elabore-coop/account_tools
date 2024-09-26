# -*- coding: utf-8 -*-
{
    "name": "Invoice and sale order note",
    "category": "Account",
    "version": "16.0.1.0",
    "summary": "Add note in sale orders and invoices document",
    "author": "Elabore",
    "website": "https://elabore.coop/",
    "installable": True,
    "application": False,
    "auto_install": False,
    "description": """
==========================================
Invoice and sale order note
==========================================
Add note field in invoices and sale order
Display this field in generated documents
Copy note field when invoice created from sale order

Installation
============
Just install invoice_sale_order_note, all dependencies will be installed by default.

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
* Clément Thomas

Funders
-------
The development of this module has been financially supported by:
* Elabore (https://elabore.coop)
* Coopérative Tiers-Lieux

Maintainer
----------
This module is maintained by ELABORE.

""",
    "depends": [
        "base",
        "account",
        "sale",
    ],
    "data": [
        "views/sale_views.xml",
        "views/account_move_views.xml",
        "views/account_invoice_report.xml",
        "views/sale_order_report.xml",
    ],
    "qweb": [],
}
