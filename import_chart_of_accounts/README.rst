================
import_chart_of_accounts
================

Provide several profiles for one person.

Installation
============

Use Odoo normal module installation procedure to install
``import_chart_of_accounts``.

Description
=============

Pendant l'import, chaque ligne est comparée aux comptes comptables présents dans Odoo
- Si le compte comptable existe déjà dans bdd, seul le nom du compte comptable est mis à jour 
- Un compte comptable est déjà existant si les 6 premiers chiffres du code comptable sont identique (par ex: le compte 120000 et 12000000 sont les mêmes comptes)
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

Known issues / Roadmap
======================

None yet.

Bug Tracker
===========

Bugs are tracked on `our issues website <https://github.com/elabore-coop/account-tools/issues>`_. In case of
trouble, please check there if your issue has already been
reported. If you spotted it first, help us smashing it by providing a
detailed and welcomed feedback.

Credits
=======

Contributors
------------

* Laetitia Da Costa

Funders
-------

The development of this module has been financially supported by:
* Elabore (https://elabore.coop)


Maintainer
----------

This module is maintained by Elabore.