{
    'name': 'Import chart of accounts',
    'version': '14.0.1.0.0',
    'summary': 'while importing the accounts chart, only update account name  of existing accounts and automatise settings for new accounts',
    'description': """

Installation
============

Install import_chart_of_accounts, all dependencies will be installed by default.

Description
=============

Pendant l'import, chaque ligne est comparée aux comptes comptables présents dans Odoo
- Si le compte comptable existe déjà dans bdd, seul le nom du compte comptable est mis à jour 
- Si le compte comptable n'existe pas dans bdd, il est créé.
- Un compte similaire est recherché dans la bdd à partir des 3 premier chiffres du code comptable.
- On recherche tous les comptes qui ont les 3 premiers chiffres de son code en commun avec celui du compte nouvellement créé
- Parmi ces comptes, le compte du lequel les paramètres seront copiés sur le nouveau compte est celui au numéro de code le plus bas.
- On enregistre la valeur des variables 'type' et 'reconcilition' du compte "similaire" dans le nouveau compte comptable
- S'il n'existe "compte similaire" pour ce nouveau compte, aucun paramétrage n'est ajouté lors de l'import

Exemple :
                          
J'importe le compte comptable 607730 Epicerie divers 
Ce compte comptable n'existe pas déjà dans Odoo, il est créé. 
Pour le configurer automatiquement, on se fonde sur un compte similaire dans Odoo et avec le code le plus bas parmis les comptes similaires
Ici il s'agit de 607000 Achats de marchandise:
Il a pour Type Charges car c'est une compte de charges et Autoriser le lettrage est à False.
Le compte 607730 Epicerie divers sera donc enregistré dans Odoo avec le même paramétrage.

Usage
=====

Pour importer le plan comptable :

Aller dans l'App Facturation
Menu Configuration > Comptabilité > Importer le plan comptable

Un assistant permettant le téléversement d'un plan comptable apparaît.

Le fichier téléversé doit être au format CSV uniquement.
Il ne doit comporter que deux colonnes :
- La première colonne doit s'appeler 'code' pour le numéro de compte comptable 
- La deuxième colonne doit s'appeler 'name' pour le nom du compte comptable 
""",
    'author': '',
    'website': '',
    'license': 'AGPL-3',
    'category': '',
    'depends': [
        'account'
    ],
    'data': [
        'wizard/import_coa_wizard_views.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': False,
    'assets': {
    }
}


