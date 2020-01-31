#### Backup And Restore ###

Ce script permet de Sauvegarder les dossier suivant

	/VAR/WWW
	/etc/apache2
	
il permet egalement de sauvegarder la bases de donnée qu'on lui indiquera lors de l'execution

### Prerequis ###

Il faut renseigner les Variable Suivante 

###   Backup   ###
PATHBACKUPTMP = ('***********')         #######   Chemin temporaire de la Sauvegarde     #######
PATHBACKUP = ('*************')          #######   Chemin final de la sauvegarde    #######

LASTBACKUP = ('**************')         #######   chemin de la derniere sauvegarde pour le lien symbolique     #######

###   Restore   ###
PATHRESTORETMP = ('****')               #######   Chemin temporaire de la Restauration     #######
PATHRESTORE = ('****************')      #######   Chemin temporaire de l' extraction de l'archive     #######

###   MySQL   ###               
DB_HOST = '*****************'           #######   Nom du serveur ou ce trouve la BDD     #######
DB_NAME = raw_input('entrer le nom de la base Mysql : ' )       #######   Nom de la BDD avec saisie utilisateur      #######
DB_USER = '****'                                                #######   Utilisateur pour la conexion a MySQL      #######
DB_PASSWORD = raw_input('Mot de passe MySQL : ' )               #######   Mot de passe  pour la conexion a MySQL avec saisie Utilisateur     #######

###   WordPress   ###
WP_PATH = (' ********')                 #######   Chemin /var/www     #######

###   Apache   ###
APACHE_PATH = (' ************')         #######   Chemin /etc/apache2     #######

