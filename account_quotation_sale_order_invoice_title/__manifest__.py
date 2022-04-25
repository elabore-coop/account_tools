# -*- coding: utf-8 -*-
{
    "name": "Account Quotation Sale Order Invoice Title",
    "category": "Account",
    "version": "13.0.1.0",
    "summary": "Transfer the Receipt Lost value in invoices and account move lines",
    "author": "Elabore",
    "website": "https://elabore.coop/",
    "installable": True,
    "application": False,
    "auto_install": False,
    "description": """
==========================================
Account Quotation Sale Order Invoice Title
==========================================
This module allows to add a title in Quotations, Sale Orders and Invoices.
When an invoice is created from a Sale Order, the title is transfered.

Installation
============
Just install account_quotation_sale_order_invoice_title, all dependencies will be installed by default.

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
* Stéphan Sainléger <https://github.com/stephansainleger>

Funders
-------
The development of this module has been financially supported by:
* Elabore (https://elabore.coop)
* Datactivist (https://datactivist.coop)

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
    ],
    "qweb": [],
}
