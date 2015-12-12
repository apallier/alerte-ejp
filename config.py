#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Configuration du programme d'alerte pour le tarif EJP """

try:
    # Si une config particulière existe (évite de commiter sa config)
    import my_config, __builtin__
    __builtin__.config = my_config

except ImportError:

    ZONE = 'EjpSud'  # Valeur possible : "EjpOuest" "EjpPaca" "EjpNord" "EjpSud"

    FROM_ADDR = '<mon-adresse>@gmail.com'
    PASSWORD = '<mon_password_mail>'

    TO_ADDRS = ['<adresse_1>@hotmail.com', '<adresse_2>@laposte.net']

    # Exemples d'adresses de l'API de Freemobile (à adapter)
    TO_FREEMOBILE_API = [
        'https://smsapi.free-mobile.fr/sendmsg?user=12345678&pass=4HcpERTXEd2Igj',
        'https://smsapi.free-mobile.fr/sendmsg?user=87654321&pass=aQsTR5XtQfTnAq'
    ]
