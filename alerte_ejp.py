#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Programme d'alerte pour le tarif EJP.

    Le programme envoie une alerte si le lendemain est une journée EJP.
    Le programme envoie une prévision sur la base du tarif TEMPO, ce dernier
    étant connu avant (vers 8h pour le lendemain).

"""

from email.header import Header
from email.mime.text import MIMEText
import datetime
import email.utils
import logging
import smtplib
import time

import requests

try:
    import my_config as config
except ImportError:
    import config

logging.basicConfig(filename='alerte_ejp.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)-8s %(message)s')
EJP_API = r"https://particulier.edf.fr/bin/edf_rc/servlets/ejptemponew?Date_a_remonter=%s&TypeAlerte=EJP"
TEMPO_API = r"https://particulier.edf.fr/bin/edf_rc/servlets/ejptemponew?Date_a_remonter=%s&TypeAlerte=TEMPO"


def send_mail(message):
    """ Envoie un mail """
    #pylint: disable=redefined-outer-name
    if config.TO_ADDRS:
        msg = MIMEText(message.encode('latin_1'), 'plain', 'latin_1')
        msg['From'] = email.utils.formataddr(('Alerte EJP', config.FROM_ADDR))
        msg['To'] = email.utils.formataddr(('Alerte EJP',
                                            ', '.join(config.TO_ADDRS)))
        msg['Subject'] = Header("Alerte EJP", 'utf-8')

        server = smtplib.SMTP(host='smtp.gmail.com')
        server.starttls()
        server.ehlo()
        server.login(config.FROM_ADDR, config.PASSWORD)
        # server.set_debuglevel(True) # show communication with the server
        try:
            server.sendmail(config.FROM_ADDR, config.TO_ADDRS, msg.as_string())
            logging.info('Email envoyé')
        finally:
            server.quit()


def send_sms_freemobile(message):
    """ Envoi de sms via l'API de FREEMOBILE """
    for url in config.TO_FREEMOBILE_API:
        try:
            response = requests.get(url, params={'msg': message})
            if response.status_code == 200:
                logging.info('SMS envoyé à %s', url)
            else:
                logging.error('SMS non envoyé à %s', url)
                logging.debug(response)

        except BaseException as err:
            logging.error(err)


def alert_ejp(previous_status):
    """ Procédure qui s'occupe d'envoyer les alertes lorsque le lendemain est une journée EJP """
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    logging.info('Date: %s', tomorrow_str)

    try:
        req = requests.get(EJP_API % tomorrow_str)
        response_dict = req.json()
        logging.debug(response_dict)
        status = response_dict['JourJ'][config.ZONE]

        if status != previous_status and status != 'ND':
            if 'EST' in status:
                msg = 'On est en EJP demain :-('
            elif 'NON' in status:
                msg = 'On n\'est pas en EJP demain :-)'
            msg = msg + ' (le %s)' % tomorrow.strftime('%d-%m-%Y')
            logging.info(msg)
            send_mail(msg)
            send_sms_freemobile(msg)

        return status

    except BaseException as err:
        logging.error(err)


def prevision_ejp(previous_color):
    """ Procédure qui s'occupe d'envoyer une prevision de l'EJP sur la base du tarif TEMPO """
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    logging.info('Date: %s', tomorrow_str)

    try:
        req = requests.get(TEMPO_API % tomorrow_str)
        response_dict = req.json()
        logging.debug(response_dict)
        color = response_dict['JourJ']['Tempo']

        if color != previous_color and color != 'ND':
            msg = 'Le probabilité d\'être en EJP demain est '
            if color == "BLEU":
                msg += 'faible'
            elif color == "BLANC":
                msg += 'moyenne'
            elif color == "ROUGE":
                msg += 'élevée'

            msg = msg + ' (le %s)' % tomorrow.strftime('%d-%m-%Y')
            logging.info(msg)
            send_mail(msg)
            send_sms_freemobile(msg)

        return color

    except BaseException as err:
        logging.error(err)


if __name__ == '__main__':

    ejp_previous_status = 'ND'
    tempo_previous_color = 'ND'
    while True:

        if not 4 <= datetime.date.today().weekday() <= 5:
            logging.info('-' * 50)
            ejp_status = alert_ejp(ejp_previous_status)
            if ejp_status:
                ejp_previous_status = ejp_status
            tempo_color = prevision_ejp(tempo_previous_color)
            if tempo_color:
                tempo_previous_color = tempo_color

        time.sleep(60)
