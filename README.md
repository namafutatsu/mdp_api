# mdp_api

An API for the magasins de producteurs.

Needs django-newsletter and a fork of the django-places app.

Get rollin' baby.

# Injection

(mdp_api) [victor@M]<~/perso/mdp-api> ENVIRONMENT=dev python inject.py scripts/data/magasindbhmdprod_table_mv_region.csv scripts/mv_reseau.csv scripts/mv_magasin.csv scripts/data/magasindbhmdprod_table_mv_user.csv  scripts/data/magasindbhmdprod_table_mv_global_departement.csv
/home/victor/.virtualenvs/mdp_api/lib/python3.6/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from release 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycopg/docs/install.html#binary-install-from-pypi>.
  """)
>>>>>>> error: department=Guadeloupe region=23 does not exist
>>>>>>> error: department=Martinique region=35 does not exist
>>>>>>> error: department=Guyane region=36 does not exist
>>>>>>> error: department=La Réunion region=38 does not exist
>>>>>>> error: department=Nouvelle-Calédonie region=37 does not exist
>>>>>>> error: department=Mayotte region=38 does not exist
>>>>>>> error: department=Polynésie FranÃ§aise region=34 does not exist
>>>>>>> error: department=Allemagne region=92 does not exist
>>>>>>> error: department=Belgique region=92 does not exist
>>>>>>> error: department=Espagne region=92 does not exist
>>>>>>> error: department=Italie region=92 does not exist
>>>>>>> error: department=Luxembourg region=92 does not exist
>>>>>>> error: department=Pays-bas region=92 does not exist
>>>>>>> error: department=Royaume-Uni region=92 does not exist
>>>>>>> error: department=Suisse region=92 does not exist
>>>>>>> error: department=Autres pays d'Europe region=92 does not exist
>>>>>>> error: department=Algérie region=90 does not exist
>>>>>>> error: department=Cameroun region=90 does not exist
>>>>>>> error: department=Cote d’Ivoire region=90 does not exist
>>>>>>> error: department=Maroc region=90 does not exist
>>>>>>> error: department=Sénégal region=90 does not exist
>>>>>>> error: department=Tunisie region=90 does not exist
>>>>>>> error: department=Autres pays africains region=90 does not exist
>>>>>>> error: department=Canada region=91 does not exist
>>>>>>> error: department=Etats-Unis region=91 does not exist
>>>>>>> error: department=Proche/Moyen-Orient region=91 does not exist
>>>>>>> error: department=Asie et Océanie region=91 does not exist
>>>>>>> error: department=Amérique du Sud region=91 does not exist
>>>>>>> error: shop=Chèvrefeuille region=0 does not exist
>>>>>>> error: shop=Chez Mon Fermier region=0 does not exist
>>>>>>> error: shop=Au Panier des 7 Vallées region=0 does not exist
>>>>>>> error: shop=Bio d&#146;Ici region=0 does not exist
>>>>>>> error: shop=Bio Terroir region=0 does not exist
>>>>>>> error: shop=La Boutique des Fermiers region=0 does not exist
>>>>>>> error: shop=La Clef des Champs region=0 does not exist
>>>>>>> error: shop=La Corbeille Paysanne region=0 does not exist
>>>>>>> error: user=sarlbioterroir@orange.fr shop=102 does not exist
>>>>>>> error: user=villa.leona@yahoo.com shop=147 does not exist
>>>>>>> error: username=Gagephiko1991 email=mmflgp@gmail.com already exists
>>>>>>> error: user=contact@cooppaysanne.fr shop=335 does not exist
>>>>>>> error: username=Luhei email=heisslerlucette@yahoo.fr already exists

Une fois que ceci est fait cela ne suffit pas du tout. Il faut ensuite créer les départements sur la base des infos des magasins et pas du tout sur la
base du fichier de global_departements.CSV qui a beau contenir les noms corrects et les bons numéros de département, il ne permet pas du tout de lier
aux régions. Il y a peut etre moyen de rendre cela plus simple en partant d'une simple liste déclarative des départements et en associant les régions,
ou en réécrivant un peu le process d'import.

Par ailleurs il faut créer l'utilisateur victor, rendre manue staff, et envoyer les bonnes images sur le serveur.

Enfin certains départements voire magasins ont des données encore encodées HTML qu'il faut corriger  à la main (double encodage...)

## LICENSE

MIT
