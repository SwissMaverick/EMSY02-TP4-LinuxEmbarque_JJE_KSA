Ce git contient le script principal faisant les actions suivantes :
- Lecture de la température et de l'humidité captées par le capteur.
- Calcul du point de rosée en se servant de ces deux informations.
- Ecrit dans un fichier.csv la date, l'heure, la température, l'humidité et le point de rosée à chaque fois que le script est lancé.
- Nous avertit en envoyant un mail que la température extérieure dépasse les 28°C.

Ce git contient aussi les instructions pour réaliser un "crontab" qui nous permettra de lancer le script toutes les 15min.
