# Copyright 2025 Boris Gallet ()
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "account_move_attachement_zipped_download",
    "version": "16.0.1.0.0",
    "author": "Elabore",
    "website": "https://elabore.coop",
    "maintainer": "Boris Gallet",
    "license": "AGPL-3",
    "category": "Tools",
    "summary": "Extend attachments zipped download for account_move model",
    # any module necessary for this one to work correctly
    "depends": ["base", "account", "attachment_zipped_download"],
    "qweb": [],
    "external_dependencies": {
        "python": [],
    },
    # always loaded
    "data": ["views/download_account_move_attachments.xml"],
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
