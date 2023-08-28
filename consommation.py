from influxdb import InfluxDBClient

def obtenir_clients_par_deveui():
    # Informations d'authentification
    username = "username"
    password = "password"

    # Connexion au serveur InfluxDB
    host = "192.168.201.21"
    port = 8086
    database = "mydatabase"
    influx_client = InfluxDBClient(host=host, port=port, username=username, password=password, database=database)

    # Exécuter la requête pour obtenir les 10 premiers "deveui" distincts
    query = 'SELECT DISTINCT("deveui") as alldeveui FROM "autogen"."Consommation_ModBus1" '
    result = influx_client.query(query)
    # Initialisation des totaux
    consommation_Bouygues = 0.0
    consommation_Orange = 0.0
    consommation_Free = 0.0
    consommation_SFR = 0.0
    consommation_Environnement_TDF = 0.0
    consommation_Ombriere = 0.0
    # Parcourir les résultats pour chaque "deveui" et afficher les clients et la consommation correspondants
    for point in result.get_points():
        deveui = point['alldeveui']

        # Obtenir les noms des clients
        query_clients = f'SELECT DISTINCT("client") as Clients FROM "autogen"."Consommation_ModBus1" WHERE "deveui" = \'{deveui}\''
        result_clients = influx_client.query(query_clients)
        clients = [client_point['Clients'] for client_point in result_clients.get_points()]

        # Initialisation des totaux de consommation par client
        total_consommation = {client: 0 for client in clients}

        # Boucle pour obtenir la consommation correspondante pour chaque client
        for client_name in clients:
            query_consommation = f'SELECT LAST("consommation") - FIRST("consommation") AS consommation FROM "autogen"."Consommation_ModBus1" WHERE time >= now() - 30d AND "deveui" = \'{deveui}\' AND "client" = \'{client_name}\''
            result_consommation = influx_client.query(query_consommation)
            for consommation_point in result_consommation.get_points():
                consommation = consommation_point.get('consommation', 0)
                total_consommation[client_name] += consommation

        #print(f"Consommation totale par client pour le deveui {deveui}:")
       
        for client_name, consommation in total_consommation.items():

            if client_name == "Bouygues_A" or client_name == "Bouygues_B":
                consommation_Bouygues += consommation
            elif client_name == "Orange_A" or client_name == "Orange_B":
                consommation_Orange += consommation
            elif client_name == "Free_A" or client_name == "Free_B":
                consommation_Free += consommation
            elif client_name == "SFR_A" or client_name == "SFR_B":
                consommation_SFR += consommation
            elif client_name == "Environnement_TDF":
                consommation_Environnement_TDF += consommation
            elif client_name == "Ombriere":
                consommation_Ombriere += consommation
            else:
                print(f"{client_name}: {consommation}")

    print()




    # Création de la liste des points pour l'écriture dans la base de données
    points = []
    
    consommationTotale= consommation_Bouygues + consommation_Orange + consommation_Free + consommation_SFR + consommation_Environnement_TDF + consommation_Ombriere 
    
    # Création de la liste des points pour l'écriture dans la base de données
    points = [
        {
            "measurement": "ConsommationTotale",
            "tags": {
                
                "client": "ConsommationTotale"
            },
            "fields": {
                "consommation_Bouygues": consommation_Bouygues
            }
        },
        {
            "measurement": "ConsommationTotale",
            
            "fields": {
                "consommation_Totale": consommationTotale
            }
        },
        {
            "measurement": "ConsommationTotale",
            "tags": {
                
                "client": "Orange"
            },
            "fields": {
                "consommation_Orange": consommation_Orange
            }
        },
        {
            "measurement": "ConsommationTotale",
            "tags": {
                
                "client": "Free"
            },
            "fields": {
                "consommation_Free": consommation_Free
            }
        },
        {
            "measurement": "ConsommationTotale",
            "tags": {
                
                "client": "SFR"
            },
            "fields": {
                "consommation_SFR": consommation_SFR
            }
        },
         {
            "measurement": "ConsommationTotale",
            "tags": {
                
                "client": "Environnement_TDF"
            },
            "fields": {
                "consommation_Environnement_TDF": consommation_Environnement_TDF
            }
        },
        {
            "measurement": "ConsommationTotale",
            "tags": {
                
                "client": "Ombriere"
            },
            "fields": {
                "consommation_Ombriere": consommation_Ombriere
            }
        },
       
    ]

    # Écrire les points dans la base de données
    influx_client.write_points(points)
    # # Afficher les totaux de consommation pour chaque client
    # print(f"Consommation totale pour le client Bouygues: {consommation_Bouygues}")
    # print(f"Consommation totale pour le client Orange: {consommation_Orange}")
    # print(f"Consommation totale pour le client Free: {consommation_Free}")
    # print(f"Consommation totale pour le client SFR  : {consommation_SFR}")
    # print(f"Consommation totale pour le client Environnement_TDF: {consommation_Environnement_TDF}")
    # print(f"Consommation totale pour le client Ombriere : {consommation_Ombriere}")
    # print(f"Consommation totale : {consommationTotale}")
    # print()
# Appeler la fonction pour obtenir et afficher les clients et la consommation par les 10 premiers "deveui"
obtenir_clients_par_deveui()


       

        

                
            
            
        

