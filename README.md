# Programme d'alerte sur le tarif EJP d'EDF

* Le programme envoie une alerte si le lendemain est une journée EJP.
* Le programme envoie une prévision sur la base du tarif TEMPO, ce dernier étant connu avant (vers 8h pour le lendemain).

## Installation

Fonctionne avec Python 3.

Nécessite la librairie `requests` et `tendo`:
```
pip install requests, tendo
```

## Principe

Le programme tourne en continue et va scruter les deux adresses suivantes à interval régulier :

* Pour l'EJP : https://particulier.edf.fr/bin/edf_rc/servlets/ejptemponew?Date_a_remonter=date&TypeAlerte=EJP
  
  Lorsque le tarif EJP de la journée du lendemain est connu, une alerte est envoyée par mail ou par sms via l'API Freemobile.

* Pour le TEMPO : https://particulier.edf.fr/bin/edf_rc/servlets/ejptemponew?Date_a_remonter=date&TypeAlerte=TEMPO
  
  Lorsque la couleur du tarif Tempo de la journée du lendemain est connue, une indication de la probabilité d'être en EJP est envoyée (Bleu=faible, Blanc=moyenne et rouge=élevé)
