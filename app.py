from flask import Flask, render_template
from influxdb import InfluxDBClient
import my_influxdb  # Importez le fichier où se trouve la fonction obtenir_deveui_non_communs_ris

app = Flask(__name__)


# Route pour afficher la page HTML pour le mois
@app.route('/mois')
def index_mois():
    # Appel à la fonction obtenir_deveui_non_communs_ris pour obtenir les données du mois
    ris_deveui_non_communs_mois, nombre_deveui_non_communs_mois = my_influxdb.obtenir_deveui_non_communs_ris_Mois()
    
    # Rendu du template index1.html avec les données
    return render_template('index3.html', ris_deveui_non_communs_mois=ris_deveui_non_communs_mois, nombre_deveui_non_communs_mois=nombre_deveui_non_communs_mois)

# Route pour afficher la page HTML pour la semaine
@app.route('/semaine')
def index_semaine():
    # Appel à la fonction obtenir_deveui_non_communs_ris pour obtenir les données de la semaine
    ris_deveui_non_communs_Semaine, nombre_deveui_non_communs_Semaine = my_influxdb.obtenir_deveui_non_communs_ris_Semaine()
    
    # Rendu du template index1.html avec les données
    return render_template('index.html', ris_deveui_non_communs_Semaine=ris_deveui_non_communs_Semaine, nombre_deveui_non_communs_Semaine=nombre_deveui_non_communs_Semaine)
@app.route('/all')
def index_all():
    # Appel à la fonction obtenir_deveui_non_communs_ris pour obtenir les données du mois
    ris_deveui_non_communs, nombre_deveui_non_communs = my_influxdb.obtenir_deveui_non_communs_ris()
    
    # Rendu du template index1.html avec les données
    return render_template('index1.html', ris_deveui_non_communs=ris_deveui_non_communs, nombre_deveui_non_communs=nombre_deveui_non_communs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
