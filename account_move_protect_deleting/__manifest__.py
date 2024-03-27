# Copyright 2024 Boris Gallet ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "account_move_protect_deleting",
    "version": "16.0.1.0.0",
    "author": "Elabore",
    "website": "https://elabore.coop",
    "maintainer": "Boris Gallet",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Forbid to delete an account move that has already been validated",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "account"
    ],
    "qweb": [],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": [
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