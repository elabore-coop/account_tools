# -*- coding: utf-8 -*-
{
    "name": "Account Mooncard Receipt Lost Transfer",
    "category": "Account",
    "version": "14.0.1.0",
    "summary": "Transfer the Receipt Lost value in invoices and account move lines",
    "author": "Elabore",
    "website": "https://elabore.coop/",
    "installable": True,
    "application": False,
    "auto_install": False,
    "description": """
======================================
Account Mooncard Receipt Lost Transfer
======================================
This module allows the transfer of the Receipt Lost field value from model newgen.payment.card.transaction in invoices and account.move.line

Installation
============
Before the installation, please ensure that the addons of the repository `Odoo Mooncard Connector <https://github.com/akretion/odoo-mooncard-connector>` are available in your Odoo
Just install account_mooncard_receipt_lost_transfer, all dependencies will be installed by default.

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

Maintainer
----------
This module is maintained by ELABORE.

""",
    "depends": [
        "base",
        "account",
        "base_newgen_payment_card",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    "qweb": [],
}
