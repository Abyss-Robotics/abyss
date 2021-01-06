Liste des trucs à voir en priorité:

- Init, chmod 7777 de tout les fichiers/dossiers
- ABYME --> En sale état, il manque le 3/4 des trucs
- ABYNT --> Inexistant
- ABYRA --> Enregistreur de requêtes (marche 1 coup sur 5)


Liste d'autres problèmes:

- ABYRA --> Faire répéter les questions
- ABYRD --> Compléter le dico

Autres trucs à ajouter:

- ...


[!] {1} Premières notes concernant le développement - 11/08/2020

- Commencer par intégrer le ABYNT et le ABYMT sans la ABYVI
- Développer le ABYNT sous forme de lib
- Utiliser le code de l'ancienne version "abyss.py" qui comprends une interface écrite, l'ancêtre du ABYME et l'ancêtre du ABYNT dans le même fichier
- Vérifier la compatibilité du ABYME
- Finir par s'occuper du ABYMT

Cela devrait permettre de mettre en place un système notifiant les évènements insérés directement dans la base de donnée. Cependant, le ABYME n'étant pas compplet, seuls certains types d'events seront gérés. Outre cela, les notifications devraient être 100% effectives.


L'étape suivante sera bien évidemment d'intégrer la ABYVI. On peut déjà lister quelques nécessités:

- Créer un "LOCK" pour l'utilisation de l'interface vocale (hardware).
- Permettre l'interruption de la boucle d'attente de requête, pour activation du LOCK ou pour interruption du programme. 


Enfin, il est important d'ajouter que tous les threads, notamment au niveau des "sleep" et des boucles doivent être pensés afin de permettre l'interruption rapide du programme.

FIN des premières notes - 11/08/2020 {1}



[!] {2} Notes concernant le développement - 18/10/2020

Reprise du projet avec le début des vacances. Mise en route de Git pour faciliter le versionnage et l'accès/la synchronisation à travers les différentes plateformes de développement.

Liste des modifications:
- Lancement du git 'abyss' (woodfox13)
- Suppression d'une version obsolète du abymt (abymt_V1_0.py)
- Modification du abyme ('os.chdir(../../../Abyss)' obsolète, modification du nom et du lieu du dossier)
- Modification du abymt (certaines fonctions du abyme sont utilisées directement, et non pas comme des fonctions dépendantes de la lib ('abyme.XXX')

Liste des problèmes à régler:
- Clarifier le fonctionnement (papier)
- Installer un clone sur les ordis
- Faire une version standardisée des directions, noms, chemins, git, etc... pour éviter de s'embrouiller sur les différentes plateformes et versions (penser à renommer les fichiers comprennant un id de version)
- Aucun des problèmes des notes {1} n'a été résolu.

FIN des notes - 18/10/2020 {2}


[!] {3} Notes concernant le développement - 19/10/2020

Liste des modifications:
- Un clone du git a été installé sur la totalité des ordinateurs du réseau (iMac, MacBook, rasp4 + rasp3)
- Tous les dossiers clones locaux sont répertoriés de la même façon sur les différentes plateformes ("abyssGitCode/")
- Les noms de fichiers et de directions ont été renommés afin d'éviter les confusions
- Les problèmes de la note {2} ont été résolus.

Liste des problèmes à régler:
- Aucun des problèmes des notes {1} n'a été résolu.

FIN des notes - 19/10/2020 {3}


[!] {4} Notes concernant le développement - 24/10/2020

Liste des modifications:
- Conformément à la note {1}, mise en forme de l'ABYNT sous forme de lib (à partir du code de l'ancienne version d'abyss, entièrement vérifié)
- Indication des zones qu'il faudra updater avec l'ABYVI (dans l'ABYNT) et de quelques parties de code pouvant être à l'origine d'erreurs

Liste des problèmes à régler:
- Régler les problèmes des parties de code pouvant être à l'origine d'erreurs dans l'ABYNT
- Procéder à la suite des modifications listées dans la note {1}

FIN des notes - 24/10/2020 {4}


[!] {5} Notes concernant le développement - 26/10/2020

Liste des modifications:
- Résolution de quelques problèmes dans l'ABYNT
- Résolution de quelques problèmes dans l'ABYME
- Premiers tests d'intégration de l'ABYNT dans l'ABYMT

Liste des problèmes à régler:
- Idem aux notes précédentes
- Mettre au propre certaines parties de code

FIN des notes - 26/10/2020 {5}


[!] {6} Notes concernant le développement - 30/10/2020

Liste des modifications:
- Résolution de quelques problèmes sur l'ABYNT. Il est maintenant fonctionnel, même si quelques améliorations sont possibles/nécessaires.
- Reprise en main de l'ABYME (premier check, commentaires)

Liste des problèmes à régler:
- [ABYME]: problème dans le management des events (index/création/suppresion) et des dossiers/fichiers de manière générale --> Autorisations (chmod 777), données non à jour, etc... => METTRE AU PROPRE
- [ABYME]: zones WIP à finir
- [ABYMT]: système 'exit' à mettre au propre

Liste des améliorations à faire ultérieurement:
- [ABYNT]: système de notification pas carré (quand il reçoit le signal, il cherche les notifs qui doivent être notifiées +/- à ce moment là) --> risque d'en oublier/d'en notifier certaines plusieurs fois

FIN des notes - 30/10/2020 {6}


[!] {7} Bilan du développement à ce jour - 01/11/2020

Liste des problèmes à régler:
- [ABYME]: problème dans le management des events (index/création/suppresion) et des dossiers/fichiers de manière générale --> Autorisations (chmod 777), données non à jour, etc... => METTRE AU PROPRE
- [ABYMT]: système 'exit' à mettre au propre

Liste des choses à finir:
- [ABYME]: zones WIP à finir

Liste des prochaines modifications à effectuer:
- [ABYVI]: intégrer le code de l'ABIVY. Prendre en compte note {1}: Créer un "LOCK" pour l'utilisation de l'interface vocale (hardware) & Permettre l'interruption de la boucle d'attente de requête, pour activation du LOCK ou pour interruption du programme. 

Liste des améliorations à faire ultérieurement:
- [ABYRA]: Enregistreur de requêtes (marche 1 coup sur 5)
- [ABYRA]: Faire répéter les questions
- [ABYRD]: Compléter le dico
- [ABYNT]: système de notification pas carré (quand il reçoit le signal, il cherche les notifs qui doivent être notifiées +/- à ce moment là) --> risque d'en oublier/d'en notifier certaines plusieurs fois

Autres idées d'améliorations (?):
- [ABYME]: Events inachevés, barre de progression --> pouvoir passer d'une task à l'autre et y revenir

FIN des notes - 01/11/2020 {7}


[!] {8} Bilan du développement à ce jour - 08/11/2020

Liste des modifications:
- [ABYMT]/[ABYNT]/[ABIVY]: Clarification du système d'interruption

FIN des notes - 08/11/2020 {8}
