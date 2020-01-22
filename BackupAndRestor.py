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
                print('The folder ' + PATHBACKUPTMP +' exist')
        except:
                os.mkdir(PATHBACKUPTMP)
                print('Create folder ' + PATHBACKUPTMP)
        try:
                os.stat(PATHBACKUP)
                print('The folder ' + PATHBACKUP +' exist')
        except:
                os.mkdir(PATHBACKUP)
                print('Create folder ' + PATHBACKUP)

        print('Start Backup of databases ' + DB_NAME+ '...')
        dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_PASSWORD + " " + DB_NAME + " > " + PATHBACKUPTMP + "/" + DB_NAME + ".sql"
        os.system(dumpcmd)

        print('copy the folder ' + WP_PATH + '...')
        os.system('cp -r' + WP_PATH + ' '+ PATHBACKUPTMP)

        print('copy the folder ' + APACHE_PATH +'...')
        os.system('cp -r' + APACHE_PATH + ' '+ PATHBACKUPTMP)

        print('ZIP the folder ' + PATHBACKUPTMP + 'to ' + PATHBACKUP )
        os.system('tar -czvf ' + PATHBACKUP +'FullBackup-'+DATETIME+'.tar.gz ' + PATHBACKUPTMP)

        print(' Create the link')
        os.system('rm -rf '+ PATHBACKUP + 'LastBackup.tar.gz' )
        os.system('ln -s ' + PATHBACKUP +'FullBackup-'+DATETIME+'.tar.gz ' + PATHBACKUP +'/LastBackup.tar.gz' )

        os.system('rm -rf '+ PATHBACKUPTMP)

        print('Backup databases + Wordpress + Apache is done')


def restore():

        try:
                os.stat(PATHRESTORETMP)
                print('The folder ' + PATHRESTORETMP +' exist')
        except:
                os.mkdir(PATHRESTORETMP)
                print('Create folder ' + PATHRESTORETMP)

        print('UNZip the folder ' + LASTBACKUP + ' to ' + PATHRESTORETMP )
        os.system('tar -xzvf '+ LASTBACKUP + ' -C ' + PATHRESTORETMP )

        print('copy the folder to ' + WP_PATH)
        os.system('cp -r' + PATHRESTORE + 'www /var/')

        print('copy the folder to ' + APACHE_PATH)
        os.system('cp -r' + PATHRESTORE + 'apache2 /etc/')

        print('Start Restore of databases ' + DB_NAME+ '...')
        os.system("mysql -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_PASSWORD + " " + DB_NAME + " < " + PATHRESTORE + "/" + DB_NAME + ".sql")
        
        print('Remove /tmp')
        os.system('rm -rf '+ PATHRESTORETMP)
        os.system('rm -rf '+ PATHRESTORE)

        print('Restore databases + Wordpress + Apache is done')


###   Choix Utilisateur   ###

 
def process_user_choice(user_choice):
        """
        Lance l'action que l'utilisateur a demandé
        """
        clear_screen()

        # Sauvegarde de la base
        if user_choice == 1:

                print("Backup BDD + Wordpress + Apache")
                backup()

        # Restauration de la base
        elif user_choice == 2:
                print("Restore BDD + Wordpress + Apache")
                restore()

        elif user_choice == 99:
                exit(0)

        else:
                sys.stderr.write("Error : Choice the number \n")
                sys.exit(1)


def main():

        print("Enter your choice :\n")


        print("[1] => Backup BDD + Wordpress + Apache")
        print("[2] => Restore BDD + Wordpress + Apache")


        while True:
                try:
                        user_choice = int(input("Enter your choice : > "))
                        break
                except ValueError:
                        sys.stderr.write("Error : Undefined choice")
                # sys.exit(1)
        process_user_choice(user_choice)


###   VARIABLE   ###

DATETIME = time.strftime('%Y%m%d-%H%M%S')

###   Backup   ###
PATHBACKUPTMP = ('/tmp/backup')
PATHBACKUP = ('/data/backup/')

LASTBACKUP = ('/data/backup/LastBackup.tar.gz')

###   Restore   ###
PATHRESTORETMP = ('/tmp/Restore')
PATHRESTORE = ('/tmp/Restore/tmp/backup/')

###   MySQL   ###
DB_HOST = 'localhost'
DB_NAME = raw_input('entrer le nom de la base Mysql : ' )
DB_USER = 'root'
DB_PASSWORD = raw_input('Mot de passe MySQL : ' )

###   WordPress   ###
WP_PATH = (' /var/www')

###   Apache   ###
APACHE_PATH = (' /etc/apache2')

try:
        main()
except KeyboardInterrupt:
        print('Process Interrupted')
        try:
                sys.exit(0)
        except SystemExit:
                sys.exit(0)