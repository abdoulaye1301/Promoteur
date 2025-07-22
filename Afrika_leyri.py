import streamlit as st
import pandas as pd
from PIL import Image
from openpyxl import load_workbook
import io

st.set_page_config(
    page_title="Ingénieur NDAO", layout="wide", page_icon="ndao abdoulaye.png"
)
profil = Image.open("Logo Afrika Leyri.png")
st.logo(profil)

st.title("Gestion des Stocks de Produits")
# Upload du fichier Excel
Chargement = pd.read_excel("Donnees_Promoteurs.xlsx", engine='openpyxl')

# Définir les chemins des fichiers source et destination
Chargement["Date"] = Chargement["Date"].dt.date
# donnee["Mois"] = donnee["Date"].dt.month

# Choix de l’onglet
menu = st.sidebar.radio("Navigation", ["OMAR","SAMBOU"])
if menu == "OMAR":
    #st.subheader("Contenu de la feuille sélectionnée :")
    #st.dataframe(Chargement)
    
    #operation="Kamlac"
#elif menu == "Opération":
 #   operation = st.sidebar.selectbox(
 #       "Type d'opération", ("Commande", "Livraison", "Aucune")
  #  )
   # donnee = Chargement[Chargement["Operation"] == operation]
    #if operation == "Aucune":
     #   nomcol = donnee.columns.tolist()
      #  nomcol.remove("Prix_Unitaire")
       # nomcol.remove("Quantites")
        #nomcol.remove("Produit")
        #nomcol.remove("Prix Total")
        #st.dataframe(donnee[nomcol])
    #else:
     #   st.dataframe(donnee)
#else:
   
    donne_vente = Chargement[Chargement["Operation"] == "Vente"]
    donnee_agre = (
        donne_vente.groupby(["tata"])
        .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
        .reset_index()
    )

    st.subheader("Ventes des promoteurs")
    donnee_agre = donnee_agre.rename(
        columns={
            "Quantites_Cartons": "Quantités",
            "Montant": "Montant A verser",
        }
    )
    donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)
    #donnee_agre["Date"] = donnee_agre["Date"].dt.strftime("%d/%m/%Y")
    st.dataframe(donnee_ordre)

#-----------------------------------------------------------------#
    st.subheader("Stock restant après les ventes")
    # Séparer les opérations
    stock_lundi = Chargement[Chargement['Operation'] == 'Stock Lundi']
    ventes = Chargement[Chargement['Operation'] == 'Vente']
    descente = Chargement[Chargement['Operation'] == 'Stock Descente']

    # Regrouper par tata et produit
    stock_init = stock_lundi.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()
    ventes_total = ventes.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()
    stock_descente = descente.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()

    # Calcul du stock restant
    stock_Theorique = stock_init.subtract(ventes_total, fill_value=0)

    # Fusionner les résultats dans un seul DataFrame
    df_final = stock_Theorique.reset_index().rename(columns={'Quantites_Cartons': 'Stock Théorique'})
    df_final['Stock Restant'] = df_final.apply(
        lambda row: stock_descente.get((row['tata'], row['Produit']), 0), axis=1
    )
    
    # Arrondir à 2 chiffres après la virgule
    df_final['Stock Théorique'] = df_final['Stock Théorique'].astype(float).round(2)
    df_final['Stock Restant'] = df_final['Stock Restant'].astype(float).round(2)

    # Ajouter la colonne Statut
    df_final['Statut'] = df_final.apply(
        lambda row: 'OK' if row['Stock Théorique'] == row['Stock Restant'] else 'Différence',
        axis=1
    )

    st.dataframe(df_final)
#-----------------------------------------------------------------#
elif menu == "SAMBOU":
    # Définir les bornes du slider
    min_date = min(Chargement["Date"])
    max_date = max(Chargement["Date"])

    # Slider Streamlit pour filtrer une plage de dates
    #start_date, end_date = st.slider(
    #   "Sélectionnez une plage de dates",
    #  min_value=min_date,
    # max_value=max_date,
        #value=(min_date, max_date),  # valeur par défaut (tout)
        #format="YYYY/MM/DD"
    #)

    # Filtrer les données selon la plage sélectionnée
    #donnee = Chargement[(Chargement["Date"] >= start_date) & (Chargement["Date"] <= end_date)]

    # Afficher les résultats
    #st.write(f"Résultats entre {start_date} et {end_date} :")

    menu_sambou = st.sidebar.selectbox("Navigation", ["TATA 1", "TATA 2","TATA 3"])
    donnee = Chargement[Chargement["tata"] == menu_sambou]
    donne_vente = Chargement[Chargement["Operation"] == "Vente"]
    donnee_agre = (
        donne_vente.groupby(["tata","Prenom_Nom_Promoteur","Produit"])
        .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
        .reset_index()
    )

    st.subheader("Ventes de promoteurs")
    donnee_agre = donnee_agre.rename(
        columns={
            "tata": "TATA",
            "Prenom_Nom_Promoteur": "Promoteur",
            "Quantites_Cartons": "Quantités",
            "Montant": "Montant A verser",
        }
    )
    donnee_ordre = donnee_agre.sort_values(by=["TATA","Promoteur"], ascending=False)
    #donnee_agre["Date"] = donnee_agre["Date"].dt.strftime("%d/%m/%Y")
    st.dataframe(donnee_ordre)
    
    colone= st.columns(3)
    colone[0].metric("💴 CA TATA 1", f"{donnee_ordre[donnee_ordre["TATA"] =="TATA 1"]["Montant A verser"].sum():,.0f}".replace(",", " ")+" XOF")
    colone[1].metric("💴 CA TATA 2", f"{donnee_ordre[donnee_ordre["TATA"] =="TATA 2"]["Montant A verser"].sum():,.0f}".replace(",", " ")+" XOF")
    colone[2].metric("💴 CA TATA 3", f"{donnee_ordre[donnee_ordre["TATA"] =="TATA 3"]["Montant A verser"].sum():,.0f}".replace(",", " ")+" XOF")
