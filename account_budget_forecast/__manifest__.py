# Copyright 2021 Elabore ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "account_budget_forecast",
    "version": "13.0.1.0.0",
    "author": "Elabore",
    "maintainer": "False",
    "website": "False",
    "license": "AGPL-3",
    "category": "False",
    "summary": "Project Forcast Budget to plan the costings and expenses of your projects",
    "description": """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3
=======================
Account Budget Forecast
=======================
This module provides budget forecast functionnalities.

Installation
============
Just install account_budget_forecast, all dependencies will be installed by default.

Known issues / Roadmap
======================

Bug Tracker
===========
Bugs are tracked on `GitHub Issues
<https://github.com/elabore-coop/elabore-odoo-addons/issues>`_. In case of trouble, please
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
* Amaco (https://amaco.org)

Maintainer
----------
This module is maintained by ELABORE.

""",
    # any module necessary for this one to work correctly
    "depends": [
        "account",
        "analytic",
        "base",
        "crm",
        "hr_timesheet",
        "product",
        "project",
        "sale",
        "stock",
    ],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/account_analytic_account.xml",
        "views/account_analytic_account_categories.xml",
        "views/account_invoice.xml",
        "views/sale_order.xml",
        "views/budget_forecast.xml",
        "views/budget_coefficient.xml",
        "views/budget_coefficient_model.xml",
        "views/product_template_form.xml",
        "views/hr_employee.xml",
        "views/actions.xml",
        "views/assets.xml",
        "views/menu.xml",
        "views/crm_lead.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
    "js": [],
    "css": [],
    "qweb": [],
    "installable": True,
    # Install this module automatically if all dependency have been previously
    # and independently installed.  Used for synergetic or glue modules.
    "auto_install": False,
    "application": False,
}
