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

menu = st.sidebar.selectbox("Navigation", ["Kamlac","TATA 1", "TATA 2","TATA 3"])

if menu == "Kamlac":
    #st.subheader("Contenu de la feuille sélectionnée :")
    #st.dataframe(Chargement)
    operation="Kamlac"
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
    st.write(
        "La colonne Opération ne se trouve pas dans les colonnes selectionnées"
    )
    donne_vente = Chargement[Chargement["Operation"] == "Vente"]
    donnee_agre = (
        donne_vente.groupby(["tata"])
        .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
        .reset_index()
    )

    st.subheader("Ventes de promoteurs")
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
    stock_restant = stock_init.subtract(ventes_total, fill_value=0)

    # Fusionner les résultats dans un seul DataFrame
    df_final = stock_restant.reset_index().rename(columns={'Quantites_Cartons': 'Stock Restant'})
    df_final['Stock Descente'] = df_final.apply(
        lambda row: stock_descente.get((row['tata'], row['Produit']), 0), axis=1
    )

    # Ajouter la colonne Statut
    df_final['Statut'] = df_final.apply(
        lambda row: 'OK' if row['Stock Restant'] == row['Stock Descente'] else 'Différence',
        axis=1
    )

    st.dataframe(df_final)
#-----------------------------------------------------------------#

    nom_nouvelle_feuille = st.sidebar.text_input("Nom de la feuille :",value=operation)
    if st.button("Sauvegarder"):
        # Définir le nom sous lequel la feuille sera enregistrée dans le fichier de destination
        if nom_nouvelle_feuille.strip() == "":
            st.warning(
                "Veuillez renseigner le nom de la feuille dans la barre de naviagation."
            )
        else:
            # Charger le fichier original dans openpyxl
            memorise_nouvelle_feuille = io.BytesIO(Chargement.getvalue())
            wb = load_workbook(memorise_nouvelle_feuille)

            # Supprimer la feuille si elle existe déjà (et n'est pas la seule)
            if nom_nouvelle_feuille in wb.sheetnames:
                if len(wb.sheetnames) > 1:
                    del wb[nom_nouvelle_feuille]
                else:
                    st.error("Impossible de supprimer la seule feuille visible.")
                    st.stop()

            # Copie de toutes les feuilles existantes dans un nouveau Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                # Copier les anciennes feuilles
                for feuille in wb.sheetnames:
                    data = pd.read_excel(memorise_nouvelle_feuille, sheet_name=feuille)
                    data.to_excel(writer, sheet_name=feuille, index=False)

                # Ajouter la feuille modifiée
                Chargement.to_excel(writer, sheet_name=nom_nouvelle_feuille, index=False)
                donnee_ordre.to_excel(writer, sheet_name=f"Récapitulatif des {nom_nouvelle_feuille}", index=False)
            


            st.success("✅ Fichier modifié avec succès.")

            # Bouton de téléchargement
            st.download_button(
                label="📥 Télécharger",
                data=output.getvalue(),
                file_name="KAMLAC_RZ.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
