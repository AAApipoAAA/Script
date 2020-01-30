#!/usr/bin/python
# -*-coding:Utf-8 -*-
#####################################
#Ce script permet de Sauvegarder/Restaurer Wordpress,Mysql,Apache
#Creer en Décembre 2019 sur une machine débian
#DATE 12/12/2019
#Created  by Alexis LERICHE
#Python version: 2.7.13
####################################

###   Module   ###

import os
from os.path import expanduser
import time


###   FONCTION   ###


def clear_screen():

        os.system('cls' if os.name == 'nt' else 'clear')

def backup():

        try:
                os.stat(PATHBACKUPTMP)
                print('The folder ' + PATHBACKUPTMP +' exist')    #######   test si le dossier  contenu dans la variable PATHBACKUPTMP existe   #######
        except:
                os.mkdir(PATHBACKUPTMP)
                print('Create folder ' + PATHBACKUPTMP)           #######   sinon il le creer   #######
        try:
                os.stat(PATHBACKUP)
                print('The folder ' + PATHBACKUP +' exist')       #######   test si le dossier contenu dans PATHBACKUP existe   #######
        except:
                os.mkdir(PATHBACKUP)
                print('Create folder ' + PATHBACKUP)              #######   sinon il le creer   #######

        print('Start Backup of databases ' + DB_NAME+ '...')
        dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_PASSWORD + " " + DB_NAME + " > " + PATHBACKUPTMP + "/" + DB_NAME + ".sql"   #######   Création de la sauvegarde de la bases de donnée    #######
        os.system(dumpcmd)

        print('copy the folder ' + WP_PATH + '...')
        os.system('cp -r' + WP_PATH + ' '+ PATHBACKUPTMP)       #######   Copie du repertoire Wordpress   #######

        print('copy the folder ' + APACHE_PATH +'...')
        os.system('cp -r' + APACHE_PATH + ' '+ PATHBACKUPTMP)   #######   Copie du repertoire Apache   #######

        print('ZIP the folder ' + PATHBACKUPTMP + 'to ' + PATHBACKUP )
        os.system('tar -czvf ' + PATHBACKUP +'FullBackup-'+DATETIME+'.tar.gz ' + PATHBACKUPTMP)         #######   Création de l'archive   #######

        print(' Create the link')
        os.system('rm -rf '+ PATHBACKUP + 'LastBackup.tar.gz' )         #######   Supression de l'ancien lien symbolique    #######
        os.system('ln -s ' + PATHBACKUP +'FullBackup-'+DATETIME+'.tar.gz ' + PATHBACKUP +'/LastBackup.tar.gz' )         #######   création du lien symbolique    #######

        os.system('rm -rf '+ PATHBACKUPTMP)     #######   Supression du repertoire temporaire    #######

        print('Backup databases + Wordpress + Apache is done')


def restore():

        try:
                os.stat(PATHRESTORETMP)                                 #######   test si le dossier  contenu dans la variable PATHRESTORETMP existe   #######
                print('The folder ' + PATHRESTORETMP +' exist')          
        except:
                os.mkdir(PATHRESTORETMP)                                #######   sinon il le creer   #######
                print('Create folder ' + PATHRESTORETMP)

        print('UNZip the folder ' + LASTBACKUP + ' to ' + PATHRESTORETMP )
        os.system('tar -xzvf '+ LASTBACKUP + ' -C ' + PATHRESTORETMP )          #######   extraction del'archive   #######

        print('copy the folder to ' + WP_PATH)
        os.system('cp -r' + PATHRESTORE + 'www /var/')                  #######   Copie du dossier www vers /var/   #######

        print('copy the folder to ' + APACHE_PATH)
        os.system('cp -r' + PATHRESTORE + 'apache2 /etc/')              #######   Copie du dossier Apache2 vers /etc/   #######

        print('Start Restore of databases ' + DB_NAME+ '...')
        os.system("mysql -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_PASSWORD + " " + DB_NAME + " < " + PATHRESTORE + "/" + DB_NAME + ".sql")        #######   Restauration de la bases de donnée    #######
        
        print('Remove /tmp')
        os.system('rm -rf '+ PATHRESTORETMP)    #######   Supression du repertoire temporaire    #######
        os.system('rm -rf '+ PATHRESTORE)       #######   Supression du repertoire extraction temporaire    #######

        print('Restore databases + Wordpress + Apache is done')


###   Choix Utilisateur   ###

 
def process_user_choice(user_choice):
        """
        Lance l'action que l'utilisateur a demandé
        """
        clear_screen()

        # Sauvegarde de la base
        if user_choice == 1:

                print("Backup BDD + Wordpress + Apache")        #######   Choix utilisateur 1 = Sauvegarde    #######
                backup()

        # Restauration de la base
        elif user_choice == 2:
                print("Restore BDD + Wordpress + Apache")       #######   Choix utilisateur 2 = Restauration    #######
                restore()

        elif user_choice == 99:                                 #######   Choix utilisateur 99 = Quitte le programme    #######
                exit(0)

        else:
                sys.stderr.write("Error : Choice the number \n")        #######   Si aucun des chiffres du dessus message d'erreur    #######
                sys.exit(1)


def main():

        print("Enter your choice :\n")


        print("[1] => Backup BDD + Wordpress + Apache")
        print("[2] => Restore BDD + Wordpress + Apache")


        while True:
                try:
                        user_choice = int(input("Enter your choice : > ")) #######   Attente choix utilisateur     #######
                        break
                except ValueError:
                        sys.stderr.write("Error : Undefined choice")    #######   si erreur print "Error : Undefined choice"     #######
                # sys.exit(1)
        process_user_choice(user_choice)


###   VARIABLE   ###

DATETIME = time.strftime('%Y%m%d-%H%M%S')

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

try:
        main()                          #######   Démarage du programme     #######
except KeyboardInterrupt:               #######    sinon interuption  #######
        print('Process Interrupted')
        try:
                sys.exit(0)
        except SystemExit:
                sys.exit(0)