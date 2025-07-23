import streamlit as st
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from io import BytesIO
import io

st.set_page_config(
    page_title="Ingénieur NDAO", layout="wide", page_icon="ndao abdoulaye.png"
)
profil = Image.open("Logo Afrika Leyri.png")
st.logo(profil)

st.markdown("<h1 style='text-align: center;'>Gestion des Stocks de Produits</h1>", unsafe_allow_html=True)
# Upload du fichier Excel
Chargement = pd.read_excel("Donnees_Promoteurs.xlsx", engine='openpyxl')

# Définir les chemins des fichiers source et destination
Chargement["Date"] = Chargement["Date"].dt.date

# donnee["Mois"] = donnee["Date"].dt.month
# Définir les bornes du slider
min_date = Chargement["Date"].unique()
#Slider Streamlit pour filtrer une plage de dates

colone= st.columns(5)
colone[2].write(" ")
colone[1].write(" ")
dat = colone[0].selectbox("", min_date)
# Choix de l’onglet
menu = st.sidebar.radio("Navigation", ["OMAR","SAMBOU"])
#-----------------------------------------------------------------#
if menu == "OMAR":
    #omar = st.sidebar.radio("Navigation", ["Versement","Stock", "Promoteur"])
    donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Date"] == dat)]
    donnee_agre = (
        donne_vente.groupby(["tata"])
        .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
        .reset_index()
    )

    st.markdown("<h4 style='text-align: center;'>!---------- Versement des promoteurs ----------!</h4><br>", unsafe_allow_html=True)
    #st.subheader("!-------------------- Versement des promoteurs --------------------!")
    donnee_agre = donnee_agre.rename(
        columns={
            "Quantites_Cartons": "Quantités",
            "Montant": "Montant A verser",
        }
    )
    donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)
    #donnee_agre["Date"] = donnee_agre["Date"].dt.strftime("%d/%m/%Y")
    #st.dataframe(donnee_ordre)

    colone= st.columns(3)
    colone[0].metric("💴 CA TATA 1", f"{donnee_ordre[donnee_ordre["tata"] =="TATA 1"]["Montant A verser"].sum():,.2f}".replace(",", " ")+" XOF")
    colone[1].metric("💴 CA TATA 2", f"{donnee_ordre[donnee_ordre["tata"] =="TATA 2"]["Montant A verser"].sum():,.2f}".replace(",", " ")+" XOF")
    colone[2].metric("💴 CA TATA 3", f"{donnee_ordre[donnee_ordre["tata"] =="TATA 3"]["Montant A verser"].sum():,.2f}".replace(",", " ")+" XOF")


    # Étape 2 : Génération du PDF avec matplotlib
    # -----------------------
   # fig, ax = plt.subplots(figsize=(10, len(df_final)*0.6 + 1))
   # ax.axis('off')
    #table = ax.table(cellText=donnee_ordre.values,
     #               colLabels=donnee_ordre.columns,
      #              cellLoc='center',
       #             loc='center')
    #table.scale(1, 1.5)
    #plt.title("Rapport de Stock par TATA - Comparaison avec Stock Descente (25-07-22)", fontsize=14, weight='bold')

    # Sauvegarde en PDF
    #plt.savefig("rapport_stock.pdf", bbox_inches='tight')
    #plt.close()

    #print("✅ Rapport PDF généré : rapport_stock.pdf")
#-----------------------------------------------------------------#
    st.subheader("Stock restant après les ventes")
    #prom = st.selectbox("", ["TATA 1", "TATA 2","TATA 3"])
    # Séparer les opérations
    stock_lundi = Chargement[Chargement['Operation'] == 'Stock Lundi']
    ventes = Chargement[Chargement['Operation'] == 'Vente']
    descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Date'] == dat)]

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
#---------------------------- Rapport de Omar ------------------#
    donnee_agr = (
        donne_vente.groupby(["tata","Produit"])
        .agg({"Quantites_Cartons": "sum"})
        .reset_index()
    )
    st.markdown("<br><h4 style='text-align: center;'>!---------- Ventes par produit et Stock Restant ----------!</h4>", unsafe_allow_html=True)
    #st.subheader("Ventes par produit et Stock Restant")
    donnee_agr = donnee_agr.rename(
        columns={
            "tata": "TATA",
            "Quantites_Cartons": "Quantités vendues"
        }
    )
    donn=df_final[["tata","Produit","Stock Restant"]].sort_values(by=["tata"], ascending=False)
    donn= donn.rename(
        columns={"tata": "TATA","Produit":"Produit","Stock Restant":"Stock Restant"})
    donnee_ordr = donnee_agr.sort_values(by=["TATA"], ascending=False)
    
    # 3. Fusionner les deux sur TATA + Produit
    donnee_ordr = pd.merge(donn, donnee_ordr, on=["TATA", "Produit"], how="left")

    
    
    colo = st.columns(5)
    prom = colo[2].selectbox("", ["TATA 1", "TATA 2","TATA 3"])

    #st.dataframe(donnee_ordr[(donnee_ordr["TATA"] == prom)])
      # Étape 2 : Génération du PDF avec matplotlib
    # -----------------------
    # 🔧 Fonction pour créer l'image avec les infos en haut
    def generate_png_report(df, date_str, zone_str, nb_promoteurs):
        fig, ax = plt.subplots(figsize=(12, len(df) * 0.6 + 2))
        ax.axis('off')

        # En-tête
        plt.text(0.5, 1.02, f"Rapport de Stock du {prom}", ha='center', fontsize=14, transform=ax.transAxes, weight='bold')
        plt.text(0.01, 0.97, f"Date : {date_str}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')
        plt.text(0.01, 0.935, f"Zone : {zone_str}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')
        plt.text(0.01, 0.90, f"Nombre de promoteurs : {nb_promoteurs}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')

        # Tableau matplotlib
        table = ax.table(cellText=df.values,
                        colLabels=df.columns,
                        cellLoc='center',
                        loc='center')

        table.scale(1, 1.5)

        # ➕ Mettre en rouge texte + fond si "Stock Restant" < 10
        stock_col_idx = df.columns.get_loc("Stock Restant")
        for i in range(len(df)):
            val = df.iloc[i, stock_col_idx]
            if isinstance(val, (int, float)) and val < 10:
                cell = table[i + 1, stock_col_idx]  # +1 pour l’en-tête
                cell.set_text_props(color='white', weight='bold')  # texte blanc pour lisibilité
                cell.set_facecolor('#FF5C5C')  # rouge clair (hex)
        # ✅ Ligne "TOTAL" en gras et fond orange
        total_row_index = len(df)  # ligne après les données
        for j in range(len(df.columns)):
            cell = table[total_row_index, j]
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#FFA500')  # orange clair
        # Sauvegarde
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=200)
        plt.close()
        buffer.seek(0)
        return buffer
    # Calculer le nombre de promoteurs
    # Génération et bouton
    # Génération de l'image PNG avec en-tête
    zone=Chargement[(Chargement['tata'] == prom) & (Chargement['Date'] == dat)]["zone"].dropna().unique()
    nb_promoteurs=len(Chargement[(Chargement['tata'] == prom) & (Chargement['Date'] == dat)]["Prenom_Nom_Promoteur"].unique())
    # Ajout d'une ligne "Total" avec les sommes des colonnes numériques
    filtre = donnee_ordr[(donnee_ordr["TATA"] == prom)]
    filtre['Quantités vendues'] = filtre['Quantités vendues'].fillna(0)
    # Calcule des totaux
    quantite_total = filtre['Quantités vendues'].sum().round(2)
    stock_restant_total = filtre['Stock Restant'].sum().round(2)
    total_row = {
    "TATA": "", 
    "Produit": "TOTAL", 
    "Stock Restant": stock_restant_total,
    "Quantités vendues": quantite_total
}
    df_final_total = pd.concat([filtre, pd.DataFrame([total_row])], ignore_index=True)
    df_final_total["Stock Restant"] = df_final_total["Stock Restant"].round(2)
    df_final_total["Quantités vendues"] = df_final_total["Quantités vendues"].round(2)
    # Style avec HTML
    def highlight_html(val):
        if isinstance(val, (int, float)) and val < 10:
            return 'background-color: red; color: white'
        return ''

    #df_final_total = df_final_total.style.applymap(highlight_html, subset=["Stock Restant"])
    #styled_df=df_final_total
    #styled_df = styled_df.set_properties(**{'text-align': 'center'})
    # Affichage avec markdown HTML (nécessite unsafe_allow_html=True)
    #st.markdown(styled_df.to_html(escape=False), unsafe_allow_html=True)
    #st.dataframe(df_final_total, use_container_width=True)
    png_bytes = generate_png_report(df_final_total, dat, zone[0], nb_promoteurs)
    # ✅ Afficher l'aperçu de l'image directement dans l'interface
    st.image(png_bytes, caption="Aperçu du rapport stylisé", use_column_width=True)
    #png_bytes = generate_png_report(donnee_ordr[(donnee_ordr["TATA"] == prom)])
    st.download_button(
        label="📥 Télécharger le rapport en PNG",
        data=png_bytes,
        file_name=f"rapport_{prom}_du_{dat}.png",
        mime="image/png"
    )
#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
elif menu == "SAMBOU":
    # Définir les bornes du slider
    min_date = min(Chargement["Date"])
    max_date = max(Chargement["Date"])

    #Slider Streamlit pour filtrer une plage de dates
    start_date, end_date = st.slider(
       "Sélectionnez une plage de dates",
      min_value=min_date,
     max_value=max_date,
        value=(min_date, max_date),  # valeur par défaut (tout)
        format="YYYY/MM/DD"
    )

    # Filtrer les données selon la plage sélectionnée
    donnee = Chargement[(Chargement["Date"] >= start_date) & (Chargement["Date"] <= end_date)]

    # Afficher les résultats
    #st.write(f"Résultats entre {start_date} et {end_date} :")

    menu_sambou = st.sidebar.selectbox("Navigation", ["TATA 1", "TATA 2","TATA 3"])
    donnee1 = donnee[donnee["tata"] == menu_sambou]
    donne_vente = donnee1[donnee1["Operation"] == "Vente"]
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
#-----------------------------------------------------------------#