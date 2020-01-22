#!/usr/bin/python
# -*-coding:Utf-8 -*-
 #####################################
#this script allows you to backup a MySQL database and restore it
#This script was created and tested in Décember 2019, on a Debian machine
#DATE 19/12/2019
#Created  by Alexis LERICHE
#Python version: 2.7.13
####################################
# Import required python libraries
 
import os
import time
import datetime
import pipes
 
#Variable 
 
DB_HOST = 'localhost' 
DB_USER = 'root'
DB_USER_PASSWORD = raw_input('Mot de passe MySQL')
DB_NAME = raw_input('entrer le nom de la base de donée a Sauvegardé :' )
BACKUP_PATH = '/etc/backup/dbbackup'
 
# Varaible D'heure et Jour.
DATETIME = time.strftime('%Y%m%d-%H%M%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

class Backup:

# Vérifier si le dossier de sauvegarde existe déjà ou non. S'il n'existe pas, le créer.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)
 
# Code permettant de vérifier si vous souhaitez effectuer une sauvegarde de base de données unique ou associer plusieurs sauvegardes dans DB_NAME.
print ("vérification du fichier de noms de bases de données.")
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print ("Fichier de bases de données trouvé ...")
    print ("Démarrage de la sauvegarde " + DB_NAME)
else:
    print ("Fichier de bases de données introuvable")
    print ("Démarrage de la sauvegarde de la base de données" + DB_NAME)
    multi = 0
 
# Démarage de la sauvegarde.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")
 
   while p <= flength:
       db = dbfile.readline()   # lecture du nom de la base de données à partir d'un fichier
       db = db[:-1]         # supprime la ligne supplémentaire
       dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(dumpcmd)
       gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(gzipcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(dumpcmd)
   gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(gzipcmd)
   os.system('ln -s ' + TODAYBACKUPPATH + "/" + db + ".sql" ' /etc/backup/LastBackup')
 
print ("")
print ("Script de sauvegarde terminé")
print ("Vos sauvegardes ont été créées dans '" + TODAYBACKUPPATH + "' directory")

class Restore:
    
os.system ("cp /etc/backup/LastBackup/" + TODAYBACKUPPATH + "/" + db + ".sql /var/lib/mysql/")

