# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17L3aTg3dvErzECHhlrDiWRtgpYBGjJLf
"""

from flask import Flask, render_template
from influxdb import InfluxDBClient

app = Flask(__name__)

#####################################################   pour tous la base de données    ######################################

def obtenir_deveui_non_communs_ris():
    # Informations d'authentification
    username = "username"
    password = "password"

    # Connexion au serveur InfluxDB
    host = "192.168.201.21"
    port = 8086
    database = "mydatabase"
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

    # Exécuter la requête pour obtenir les valeurs distinctes de RIS
    query_ris = 'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1"'
    result_ris = client.query(query_ris)

    ris_deveui_non_communs = {}
    ris_IG_non_communs = {}





        # Requêtes pour période 1 et période 2
    query_period1 = f'SELECT DISTINCT("deveui") AS "deveuiall" FROM "autogen"."Consommation_ModBus1"'
    query_period2 = f'SELECT DISTINCT("deveui") AS "deveui" FROM "autogen"."Consommation_ModBus1" WHERE  time >= now() - 2d'

    # Exécution des requêtes
    result_period1 = client.query(query_period1)
    result_period2 = client.query(query_period2)

    # Extraire les deveui pour chaque période
    deveui_periode1 = [point['deveuiall'] for point in result_period1.get_points()]
    deveui_periode2 = [point['deveui'] for point in result_period2.get_points()]

    deveui_non_communs = list(set(deveui_periode1) - set(deveui_periode2))

    # Exécuter la requête pour obtenir les valeurs distinctes de RIS
    query_ris = 'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1"'
    result_ris = client.query(query_ris)

    ris_values = [point['RIS'] for point in result_ris.get_points()]

    # Exécution des requêtes pour ig et ris pour chaque deveui
    ig_deveui_mapping = {}
    ris_deveui_mapping = {}
    for deveui in deveui_non_communs:
        query_ig_for_deveui = f'SELECT DISTINCT("ig") as ig FROM "autogen"."Consommation_ModBus1" WHERE  "deveui" = \'{deveui}\''
        result_ig_for_deveui = client.query(query_ig_for_deveui)
        ig_for_deveui = [point['ig'] for point in result_ig_for_deveui.get_points()]
        ig_deveui_mapping[deveui] = ig_for_deveui

        query_ris_for_deveui = f'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1" WHERE  "deveui" = \'{deveui}\''
        result_ris_for_deveui = client.query(query_ris_for_deveui)
        ris_for_deveui = [point['RIS'] for point in result_ris_for_deveui.get_points()]

        ris_deveui_mapping[deveui] = ris_for_deveui  # Utilisation de la liste ici, au lieu d'affecter directement
    taille = len(deveui_non_communs)
    ris_deveui_non_communs = {
        "nombre_deveui_non_communs": len(deveui_non_communs),
        "deveui_non_communs": deveui_non_communs,
        "ig_deveui_mapping": ig_deveui_mapping,
        "ris_deveui_mapping": ris_deveui_mapping,
        "ris_values": ris_values  # Ajout des valeurs de RIS distinctes
    }

    ris_deveui_mapping = list(set (ris_deveui_mapping))
    ig_deveui_mapping = list(set (ig_deveui_mapping))
    ris_values = list (set (ris_values))
    deveui_non_communs= list (set (deveui_non_communs))

    ris_grouped_data = {}

    for deveui, ris_values in ris_deveui_non_communs["ris_deveui_mapping"].items():
        for ris_value in ris_values:  # Parcourir les ris_values associés au deveui
            key = ris_value  # Utiliser le ris_value comme clé

            if key not in ris_grouped_data:
                ris_grouped_data[key] = {"count": 0, "data": []}

            ig_mapping = ris_deveui_non_communs["ig_deveui_mapping"].get(deveui, "")
            ris_grouped_data[key]["data"].append({
                "deveui": deveui,
                "ig_mapping": ig_mapping,

            })
            ris_grouped_data[key]["count"] += 1


    return ris_grouped_data,taille

#####################################################   pour une semaine    ######################################

def obtenir_deveui_non_communs_ris_Semaine():
    # Informations d'authentification
    username = "username"
    password = "password"

    # Connexion au serveur InfluxDB
    host = "192.168.201.21"
    port = 8086
    database = "mydatabase"
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

    # Exécuter la requête pour obtenir les valeurs distinctes de RIS
    query_ris = 'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1"'
    result_ris = client.query(query_ris)

    ris_deveui_non_communs = {}
    ris_IG_non_communs = {}

    # Requêtes pour période 1 et période 2
    query_period1 = f'SELECT DISTINCT("deveui") AS "deveuiall" FROM "autogen"."Consommation_ModBus1" WHERE  time >= now() - 7d'
    query_period2 = f'SELECT DISTINCT("deveui") AS "deveui" FROM "autogen"."Consommation_ModBus1" WHERE  time >= now() - 2d'

    # Exécution des requêtes
    result_period1 = client.query(query_period1)
    result_period2 = client.query(query_period2)

    # Extraire les deveui pour chaque période
    deveui_periode1 = [point['deveuiall'] for point in result_period1.get_points()]
    deveui_periode2 = [point['deveui'] for point in result_period2.get_points()]

    deveui_non_communs = list(set(deveui_periode1) - set(deveui_periode2))

    # Exécuter la requête pour obtenir les valeurs distinctes de RIS
    query_ris = 'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1"'
    result_ris = client.query(query_ris)

    ris_values = [point['RIS'] for point in result_ris.get_points()]

    # Exécution des requêtes pour ig et ris pour chaque deveui
    ig_deveui_mapping = {}
    ris_deveui_mapping = {}
    for deveui in deveui_non_communs:
        query_ig_for_deveui = f'SELECT DISTINCT("ig") as ig FROM "autogen"."Consommation_ModBus1" WHERE  "deveui" = \'{deveui}\''
        result_ig_for_deveui = client.query(query_ig_for_deveui)
        ig_for_deveui = [point['ig'] for point in result_ig_for_deveui.get_points()]
        ig_deveui_mapping[deveui] = ig_for_deveui

        query_ris_for_deveui = f'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1" WHERE  "deveui" = \'{deveui}\''
        result_ris_for_deveui = client.query(query_ris_for_deveui)
        ris_for_deveui = [point['RIS'] for point in result_ris_for_deveui.get_points()]

        ris_deveui_mapping[deveui] = ris_for_deveui  # Utilisation de la liste ici, au lieu d'affecter directement
    taille = len(deveui_non_communs)
    ris_deveui_non_communs = {
        "nombre_deveui_non_communs": len(deveui_non_communs),
        "deveui_non_communs": deveui_non_communs,
        "ig_deveui_mapping": ig_deveui_mapping,
        "ris_deveui_mapping": ris_deveui_mapping,
        "ris_values": ris_values  # Ajout des valeurs de RIS distinctes
    }

    ris_deveui_mapping = list(set (ris_deveui_mapping))
    ig_deveui_mapping = list(set (ig_deveui_mapping))
    ris_values = list (set (ris_values))
    deveui_non_communs= list (set (deveui_non_communs))

    ris_grouped_data = {}

    for deveui, ris_values in ris_deveui_non_communs["ris_deveui_mapping"].items():
        for ris_value in ris_values:  # Parcourir les ris_values associés au deveui
            key = ris_value  # Utiliser le ris_value comme clé

            if key not in ris_grouped_data:
                ris_grouped_data[key] = {"count": 0, "data": []}

            ig_mapping = ris_deveui_non_communs["ig_deveui_mapping"].get(deveui, "")
            ris_grouped_data[key]["data"].append({
                "deveui": deveui,
                "ig_mapping": ig_mapping,

            })
            ris_grouped_data[key]["count"] += 1




    return ris_grouped_data,taille



#####################################################   pour un mois    ######################################

def obtenir_deveui_non_communs_ris_Mois():
    # Informations d'authentification
    username = "username"
    password = "password"

    # Connexion au serveur InfluxDB
    host = "192.168.201.21"
    port = 8086
    database = "mydatabase"
    client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

    # Exécuter la requête pour obtenir les valeurs distinctes de RIS
    query_ris = 'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1"'
    result_ris = client.query(query_ris)

    ris_deveui_non_communs = {}
    ris_IG_non_communs = {}

        # Requêtes pour période 1 et période 2
    query_period1 = f'SELECT DISTINCT("deveui") AS "deveuiall" FROM "autogen"."Consommation_ModBus1" WHERE  time >= now() - 30d'
    query_period2 = f'SELECT DISTINCT("deveui") AS "deveui" FROM "autogen"."Consommation_ModBus1" WHERE  time >= now() - 2d'

    # Exécution des requêtes
    result_period1 = client.query(query_period1)
    result_period2 = client.query(query_period2)

    # Extraire les deveui pour chaque période
    deveui_periode1 = [point['deveuiall'] for point in result_period1.get_points()]
    deveui_periode2 = [point['deveui'] for point in result_period2.get_points()]

    deveui_non_communs = list(set(deveui_periode1) - set(deveui_periode2))

    # Exécuter la requête pour obtenir les valeurs distinctes de RIS
    query_ris = 'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1"'
    result_ris = client.query(query_ris)

    ris_values = [point['RIS'] for point in result_ris.get_points()]

    # Exécution des requêtes pour ig et ris pour chaque deveui
    ig_deveui_mapping = {}
    ris_deveui_mapping = {}
    for deveui in deveui_non_communs:
        query_ig_for_deveui = f'SELECT DISTINCT("ig") as ig FROM "autogen"."Consommation_ModBus1" WHERE  "deveui" = \'{deveui}\''
        result_ig_for_deveui = client.query(query_ig_for_deveui)
        ig_for_deveui = [point['ig'] for point in result_ig_for_deveui.get_points()]
        ig_deveui_mapping[deveui] = ig_for_deveui

        query_ris_for_deveui = f'SELECT DISTINCT "RIS" AS "RIS" FROM "autogen"."Consommation_ModBus1" WHERE  "deveui" = \'{deveui}\''
        result_ris_for_deveui = client.query(query_ris_for_deveui)
        ris_for_deveui = [point['RIS'] for point in result_ris_for_deveui.get_points()]

        ris_deveui_mapping[deveui] = ris_for_deveui  # Utilisation de la liste ici, au lieu d'affecter directement
    taille = len(deveui_non_communs)
    ris_deveui_non_communs = {
        "nombre_deveui_non_communs": len(deveui_non_communs),
        "deveui_non_communs": deveui_non_communs,
        "ig_deveui_mapping": ig_deveui_mapping,
        "ris_deveui_mapping": ris_deveui_mapping,
        "ris_values": ris_values  # Ajout des valeurs de RIS distinctes
    }

    ris_deveui_mapping = list(set (ris_deveui_mapping))
    ig_deveui_mapping = list(set (ig_deveui_mapping))
    ris_values = list (set (ris_values))
    deveui_non_communs= list (set (deveui_non_communs))

    ris_grouped_data = {}

    for deveui, ris_values in ris_deveui_non_communs["ris_deveui_mapping"].items():
        for ris_value in ris_values:  # Parcourir les ris_values associés au deveui
            key = ris_value  # Utiliser le ris_value comme clé

            if key not in ris_grouped_data:
                ris_grouped_data[key] = {"count": 0, "data": []}

            ig_mapping = ris_deveui_non_communs["ig_deveui_mapping"].get(deveui, "")
            ris_grouped_data[key]["data"].append({
                "deveui": deveui,
                "ig_mapping": ig_mapping,

            })
            ris_grouped_data[key]["count"] += 1




    return ris_grouped_data,taille