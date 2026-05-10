import streamlit as st
import pandas as pd
from PIL import Image
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyBboxPatch
import textwrap
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from io import BytesIO

st.set_page_config(
    page_title="Ingénieur NDAO", layout="wide", page_icon="ndao abdoulaye.png"
)
profil = Image.open("Logo Afrika Leyri.png")
st.logo(profil)

#st.markdown("<h1 style='text-align: center;'>Gestion des Stocks de Produits</h1>", unsafe_allow_html=True)
# Upload du fichier Excel
Chargement = pd.read_excel("Donnees_Promoteurs.xlsx", engine='openpyxl')
donnee_RZ = pd.read_excel("Donnees_RZ.xlsx", engine='openpyxl')

# Définir les chemins des fichiers source et destination
Chargement["Date"] = Chargement["Date"].dt.date
donnee_RZ["Date"] = donnee_RZ["Date"].dt.date

# donnee["Mois"] = donnee["Date"].dt.month
# Définir les bornes du slider
num_semaine = Chargement["Numero_semaine"].unique()
#Slider Streamlit pour filtrer une plage de dates

colone= st.columns(5)
# Choix de l’onglet
menu = st.sidebar.radio("Navigation", ["AGREGATION","DETAIL","FICHE"])
periode = colone[0].selectbox("", ["Jour","Semaine"])
if periode == "Jour":
    semaine = colone[2].selectbox("", num_semaine)
    min_date = Chargement[Chargement["Numero_semaine"] == semaine]["Date"].dropna().unique()
    dat = colone[4].selectbox("", min_date)
    datea = dat.strftime("%d-%m-%Y")
    statio = Chargement[(Chargement["Date"] == dat)]
    donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Date"] == dat)]
elif periode == "Semaine":
    semaine = colone[2].selectbox("", num_semaine)
    statio = Chargement[(Chargement["Numero_semaine"] == semaine)]
    datea = semaine
    donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Numero_semaine"] == semaine)]
#-----------------------------------------------------------------#
if menu == "AGREGATION":
    sous_menu = st.sidebar.selectbox("", ["Versement","Stock","Stock Départ","Récapitulatif"])
    if sous_menu == "Versement":
        donnee_agre = (
            donne_vente.groupby(["tata"])
            .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
            .reset_index()
        )
        
        st.markdown(f"<h4 style='text-align: center;'>!---------- Versement des promoteurs du {datea} ----------!</h4><br>", unsafe_allow_html=True)
        #st.subheader("!-------------------- Versement des promoteurs --------------------!")
        donnee_agre = donnee_agre.rename(
            columns={
                "Quantites_Cartons": "Quantités",
                "Montant": "Montant A verser",
            }
        )
        donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)
        #st.dataframe(donnee_ordre)

        colone= st.columns(3)
        colone[0].metric("💴 CA TATA 1", f"{donnee_ordre[donnee_ordre["tata"] =="TATA 1"]["Montant A verser"].sum():,.2f}".replace(",", " ")+" XOF")
        colone[1].metric("💴 CA TATA 2", f"{donnee_ordre[donnee_ordre["tata"] =="TATA 2"]["Montant A verser"].sum():,.2f}".replace(",", " ")+" XOF")
        colone[2].metric("💴 CA TATA 3", f"{donnee_ordre[donnee_ordre["tata"] =="TATA 3"]["Montant A verser"].sum():,.2f}".replace(",", " ")+" XOF")
        colone[0].write(" ")
        #colone[2].write(" ")
        colone[1].write(" ")
        colonne= st.columns(3)
        colonne[0].metric("🚐 Transport TATA 1", f"{statio[statio["tata"] =="TATA 1"]["Transport"].sum():,.0f}".replace(",", " ")+" XOF")
        colonne[1].metric("🚐 Transport TATA 2", f"{statio[statio["tata"] =="TATA 2"]["Transport"].sum():,.0f}".replace(",", " ")+" XOF")
        colonne[2].metric("🚐 Transport TATA 3", f"{statio[statio["tata"] =="TATA 3"]["Transport"].sum():,.0f}".replace(",", " ")+" XOF")
        colonne[0].write(" ")
        #colonne[2].write(" ")
        colonne[1].write(" ")
        colonne[0].metric("🅿️ Stationnement TATA 1", f"{statio[statio["tata"] =="TATA 1"]["Stationnement"].sum():,.0f}".replace(",", " ")+" XOF")
        colonne[1].metric("🅿️ Stationnement TATA 2", f"{statio[statio["tata"] =="TATA 2"]["Stationnement"].sum():,.0f}".replace(",", " ")+" XOF")
        colonne[2].metric("🅿️ Stationnement TATA 3", f"{statio[statio["tata"] =="TATA 3"]["Stationnement"].sum():,.0f}".replace(",", " ")+" XOF")
    

    elif sous_menu == "Stock Départ" and periode == "Semaine":
        st.markdown(f"<h4 style='text-align: center;'>!---------- Stock de départ du {datea} ----------!</h4><br>", unsafe_allow_html=True)
        
        #st.subheader("!-------------------- Stock de départ --------------------!")
        
        prom = colone[4].selectbox("", ["TATA 1","TATA 2","TATA 3"])
        
        statio1= statio[(statio["tata"] == prom) & (statio["Operation"] == "Stock Lundi")]
        donnee_agre = (
            statio1.groupby(["tata", "Produit"])
            .agg({"Quantites_Cartons": "sum",
                  "Montant": "sum"})
            .reset_index()
        )
        donnee_agre = donnee_agre.rename(
            columns={
                "Quantites_Cartons": "Quantités",
            }
        )
        donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)
        #colone= st.columns(3)
        ndao=f"{donnee_ordre[donnee_ordre["tata"] ==prom]["Montant"].sum():,.2f}".replace(",", " ")+" XOF"
        st.markdown(f"<h2 style='text-align: center;'> CA DU  {prom} : {ndao}</h2><br>", unsafe_allow_html=True)
        #colone[1].metric(f"💴 Quantités {prom}", f"{donnee_ordre[donnee_ordre["tata"] =="TATA 2"]["Quantité"].sum():,.2f}".replace(",", " "))
        st.dataframe(donnee_ordre)
    elif sous_menu == "Stock Départ" and periode == "Jour":
        st.warning("Cette option n'est disponible que pour la vue Semaine.")
    elif sous_menu == "Stock":
        if periode == "Jour":
            donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Numero_semaine"] == semaine) & (Chargement["Date"] == dat)]
        elif periode == "Semaine":
            donne_vente = Chargement[(Chargement["Operation"] == "Vente") & (Chargement["Numero_semaine"] == semaine)]
        donnee_agre = (
            donne_vente.groupby(["tata"])
            .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
            .reset_index()
        )
        #st.subheader("!-------------------- Versement des promoteurs --------------------!")
        donnee_agre = donnee_agre.rename(
            columns={
                "Quantites_Cartons": "Quantités",
                "Montant": "Montant A verser",
            }
        )
        donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)

#-----------------------------------------------------------------#


        if st.button("Voire plus de détails ") :
            st.sidebar.markdown("---")
            password = st.sidebar.text_input("Veuillez entrer le code d'accès", type="password")
            # Récupération sécurisée du secret
            OMAR = st.secrets["credentials"]["omar"]
            MANSOUR = st.secrets["credentials"]["mansour"]
            DJIBRIL = st.secrets["credentials"]["djibril"]
            IBRAHIMA = st.secrets["credentials"]["ibrahima"]

            st.markdown(f"<h4 style='text-align: center;'>!---------- Stock restant après les ventes du {datea} ----------!</h4><br>", unsafe_allow_html=True)
            #st.subheader("Stock restant après les ventes")
            #prom = st.selectbox("", ["TATA 1", "TATA 2","TATA 3"])
            # Séparer les opérations
            if (password == OMAR or password == MANSOUR or password == DJIBRIL or password == IBRAHIMA):
            
                if password == OMAR:
                    st.success("Accès autorisé, vous êtes connectés avec les identifiants de OMAR")
                    if sous_menu=="Stock":
                            prom = colone[3].selectbox("", ["TATA 1", "TATA 2", "TATA 3"])
                    else:
                        prom = colone[4].selectbox("", ["TATA 1", "TATA 2", "TATA 3"]) 
                elif password == MANSOUR:
                    st.success("Accès autorisé, vous êtes connectés avec les identifiants de MANSOUR")
                    prom = "TATA 2"
                elif password == DJIBRIL:
                    st.success("Accès autorisé, vous êtes connectés avec les identifiants de DJIBRIL")
                    prom = "TATA 1"
                elif password == IBRAHIMA:
                    st.success("Accès autorisé, vous êtes connectés avec les identifiants de IBRAHIMA")
                    prom = "TATA 3"
            
            

                if periode == "Jour":
                    stock_lundi = Chargement[(Chargement['Operation'] == 'Stock Lundi') & (Chargement['Numero_semaine'] == semaine) & (Chargement['tata'] == prom)]
                    ventes = Chargement[(Chargement['Operation'] == 'Vente') & (Chargement['Numero_semaine'] == semaine) & (Chargement["Date"] <= dat) & (Chargement['tata'] == prom)]
                    descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == dat) & (Chargement['tata'] == prom)]
                elif periode == "Semaine":
                    stock_lundi = Chargement[(Chargement['Operation'] == 'Stock Lundi') & (Chargement['Numero_semaine'] == semaine) & (Chargement['tata'] == prom)]
                    ventes = Chargement[(Chargement['Operation'] == 'Vente') & (Chargement["Numero_semaine"] == semaine) & (Chargement['tata'] == prom)]
                    
                    min_dat = Chargement[Chargement["Numero_semaine"] == semaine]["Date"].dropna().unique()[0]
                    #dat = colone[2].selectbox("", min_date)
                    descente = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat) & (Chargement['tata'] == prom)]

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
                df_final1 = df_final.drop("tata", axis=1).copy()
                st.dataframe(df_final1)
            #-----------------------------------------------------------------#
            #---------------------------- Rapport de Omar ------------------#
                donnee_agr = (
                    donne_vente.groupby(["tata","Produit"])
                    .agg({"Quantites_Cartons": "sum"})
                    .reset_index()
                )
                st.markdown(f"<br><h4 style='text-align: center;'>!---------- Rapport des ventes du {datea} ----------!</h4>", unsafe_allow_html=True)
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

                
                
                #colo = st.columns(5)
                #st.dataframe(donnee_ordr[(donnee_ordr["TATA"] == prom)])
                # Étape 2 : Génération du PDF avec matplotlib
                # -----------------------
                # 🔧 Fonction pour créer l'image avec les infos en haut
                def generate_png_report(df, date_str, zone_str, nb_promoteurs,commentaire):
                    fig, ax = plt.subplots(figsize=(12, len(df) * 0.6+1.5))
                    ax.axis('off')
                    # ✅ Texte commentaire à droite du cadre
                    if commentaire:
                        # ✅ Rectangle gris clair pour encadrer le commentaire
                        comment_box = FancyBboxPatch(
                            (0.63, 0.78),  # position (x, y) en coord. Axes (ajustable)
                            0.35,          # largeur
                            0.18,          # hauteur
                            boxstyle="round,pad=0.01",
                            transform=ax.transAxes,
                            linewidth=1,
                            edgecolor='gray',
                            facecolor='#f0f0f0',  # gris clair
                            zorder=1
                        )
                        ax.add_patch(comment_box)
                    # retour à la ligne pour le commentaire
                    wrapped_comment = textwrap.fill(commentaire, width=45)
                    # au-dessus du rectangle
                    ax.text(0.8, 0.88,wrapped_comment,
                    transform=ax.transAxes,
                    fontsize=11,
                    weight='bold',
                    va='center',
                    ha='center',
                    style='italic',
                    color='red',
                    wrap=True,
                    zorder=2) 
                    # Dimensions du rectangle d’en-tête (valeurs relatives à l’axe)
                    header_x = 0.001    # gauche
                    header_y = 0.76    # position verticale bas du bloc
                    header_width = 0.996
                    header_height = 0.24

                    # ✅ Dessiner le rectangle d'encadrement
                    rect = Rectangle((header_x, header_y), header_width, header_height,
                                    transform=ax.transAxes,
                                    fill=False, color='black', linewidth=1.5)
                    ax.add_patch(rect)
                    # En-tête
                    plt.text(0.45, 0.95, f"Rapport de Stock du {prom}", ha='center', fontsize=14, transform=ax.transAxes, weight='bold')
                    plt.text(0.01, 0.89, f"Date : {date_str}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')
                    plt.text(0.01, 0.84, f"Zone : {zone_str}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')
                    plt.text(0.01, 0.79, f"Nombre de promoteurs : {nb_promoteurs}", ha='left', fontsize=12, transform=ax.transAxes, weight='bold')

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
                if periode == "Jour":
                    zone = Chargement[(Chargement['tata'] == prom) & (Chargement["Numero_semaine"] == semaine) & (Chargement['Date'] == dat)]["zone"].dropna().unique()
                    nb_promoteurs=len(Chargement[(Chargement['tata'] == prom) & (Chargement["Numero_semaine"] == semaine) & (Chargement['Date'] == dat) & (Chargement['Prenom_Nom_Promoteur'] != "Autre")]["Prenom_Nom_Promoteur"].unique())-1
                    commente=Chargement[(Chargement['tata'] == prom) & (Chargement["Numero_semaine"] == semaine) & (Chargement['Date'] == dat)]["Commentaire"].dropna().unique().tolist()
                elif periode == "Semaine":
                    # Pour la semaine, on peut prendre la zone de la première entrée de la semaine
                    zone=Chargement[(Chargement['tata'] == prom) & (Chargement["Numero_semaine"] == semaine)]["zone"].dropna().unique()
                    nb_promoteurs=len(Chargement[(Chargement['tata'] == prom) & (Chargement["Numero_semaine"] == semaine) & (Chargement['Prenom_Nom_Promoteur'] != "Autre")]["Prenom_Nom_Promoteur"].unique())
                    commente=Chargement[(Chargement['tata'] == prom) & (Chargement["Numero_semaine"] == semaine)]["Commentaire"].dropna().unique().tolist()
                # Si le commentaire est vide, on utilise une chaîne vide
                if len(commente) == 0: 
                    commente.append("Aucune observation") 
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
                df_final_total1 = df_final_total.drop("TATA", axis=1).copy()
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
                png_bytes = generate_png_report(df_final_total1, datea, zone[0], nb_promoteurs,commente[0])
                # ✅ Afficher l'aperçu de l'image directement dans l'interface
                st.image(png_bytes, caption="", use_container_width=True)
                #png_bytes = generate_png_report(donnee_ordr[(donnee_ordr["TATA"] == prom)])
                st.download_button(
                    label="📥 Télécharger le rapport en PNG",
                    data=png_bytes,
                    file_name=f"rapport_{prom}_du_{datea}.png",
                    mime="image/png"
                )
            else:
                st.error("Accès refusé, code d'accès incorrect.")
#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
#-----------------------------------------------------------------#
    elif sous_menu == "Récapitulatif" and periode == "Semaine":
        st.markdown(f"<h4 style='text-align: center;'>!---------- Récapitulatif des ventes TATA et RZ du semaine {datea} ----------!</h4><br>", unsafe_allow_html=True)
        #st.subheader("Récapitulatif des ventes")
        donnee_agre = (
            donne_vente.groupby(["tata"])
            .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
            .reset_index()
        )
        donnee_agre = donnee_agre.rename(
            columns={
                "Quantites_Cartons": "Quantités",
                "Montant": "Montant A verser",
            }
        )
        donnee_ordre = donnee_agre.sort_values(by=["tata"], ascending=False)
        #st.dataframe(donnee_ordre)
        # ============================= Variables donnees restantes ============================= #
        donnee_RZ_Livr= donnee_RZ[(donnee_RZ["Operation"] == "Livraison") & (donnee_RZ["Semaine"] == semaine)]
        CA_donnee_RZ=donnee_RZ_Livr["Prix Total"].sum()

        # TATA 1
        min_dat = Chargement[Chargement["Numero_semaine"] == semaine]["Date"].dropna().unique()[0]
        
        #dat = colone[2].selectbox("", min_date)
        descente_T1 = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat) & (Chargement['tata'] == "TATA 1")]
        # Regrouper par tata et produit
        stock_descente_T1 = descente_T1.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()

        # TATA 2
        descente_T2 = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat) & (Chargement['tata'] == "TATA 2")]
        # Regrouper par tata et produit
        stock_descente_T2 = descente_T2.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()

        # TATA 3
        descente_T3 = Chargement[(Chargement['Operation'] == 'Stock Descente') & (Chargement['Numero_semaine'] == semaine) & (Chargement['Date'] == min_dat) & (Chargement['tata'] == "TATA 3")]
        # Regrouper par tata et produit
        stock_descente_T3 = descente_T3.groupby(['tata', 'Produit'])['Quantites_Cartons'].sum()


        colonnne= st.columns(2)
        
        colonnne[0].metric("💴 CA RZ", f"{CA_donnee_RZ:,.2f}".replace(",", " ")+" XOF")
        colonnne[1].metric("💴 CA RZ + TATA", f"{CA_donnee_RZ+donnee_ordre["Montant A verser"].sum():,.2f}".replace(",", " ")+" XOF")
        colonnne[0].metric("💴 CA TATA", f"{donnee_ordre["Montant A verser"].sum():,.2f}".replace(",", " ")+" XOF")
        colonnne[1].metric("🔢 Quantité vendue", f"{donnee_ordre["Quantités"].sum():,.2f}".replace(",", " "))
        ca_restant=descente_T2["Montant"].sum()+descente_T1["Montant"].sum() +descente_T3["Montant"].sum()
        rest=stock_descente_T1.sum()+stock_descente_T2.sum()+stock_descente_T3.sum()


        colonnne[0].metric("🚐 Transport TATA", f"{statio["Transport"].sum():,.0f}".replace(",", " ")+" XOF")
        colonnne[1].metric("🅿️ Stationnement", f"{statio["Stationnement"].sum():,.0f}".replace(",", " ")+" XOF")

        colonnne[0].metric("🏠 **Stock Restant (CA)**", f"{ca_restant:,.2f}".replace(",", " ")+" XOF")
        colonnne[1].metric("🏠 **Quantité Restante (STOCK)**", f"{rest:,.2f}".replace(",", " "))

        
    
    elif sous_menu == "Récapitulatif" and periode == "Jour":
        st.warning("Cette option n'est disponible que pour la vue Semaine.")
    
#-----------------------------------------------------------------#
elif menu == "DETAIL":
    # Filtrer les données selon la plage sélectionnée
    donnee = donne_vente
    # Afficher les résultats
    menu_sambou = st.sidebar.selectbox("TATAS", ["TATA 1","TATA 2", "TATA 3"])
    donnee1 = donnee[(donnee["tata"] == menu_sambou)]
    nom_promo=donnee1["Prenom_Nom_Promoteur"].dropna().unique().tolist()
    produit_list=donnee1[donnee1["Operation"] == "Vente"]["Produit"].dropna().unique().tolist()
    tat_indi= st.sidebar.selectbox("Option", ["TATA","INDIVIDUEL"])
    if tat_indi == "INDIVIDUEL":
        choix= st.sidebar.selectbox("Votre choix", ["Promoteur","Produit"])
        if choix == "Promoteur":
            if periode == "Jour":
                promoteur = st.sidebar.selectbox("Promoteurs", nom_promo)
                donnee2 = donnee1[(donnee["Prenom_Nom_Promoteur"] == promoteur)]
                donne_vente = donnee2[donnee2["Operation"] == "Vente"]
                if promoteur=="Autre":
                    donnee_agre = (
                        donne_vente.groupby(["tata","zone","Precisez","Produit"])
                        .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
                        .reset_index()
                    )

                    st.subheader("Ventes de promoteurs")
                    donnee_agre = donnee_agre.rename(
                        columns={
                            "tata": "TATA",
                            "Precisez": "RZ",
                            "Quantites_Cartons": "Quantités",
                            "Montant": "Montant A verser",
                        }
                    )
                    donnee_ordre = donnee_agre.sort_values(by=["TATA","RZ"], ascending=False)
                else:
                    donnee_agre = (
                        donne_vente.groupby(["tata","zone","Prenom_Nom_Promoteur","Produit"])
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
            elif periode == "Semaine":
                donne_vente = donnee1[donnee1["Operation"] == "Vente"]
                donnee_agre = (
                    donne_vente.groupby(["tata","Prenom_Nom_Promoteur"])
                    .agg({"Montant": "sum"})
                    .reset_index()
                )

                st.subheader("Ventes de promoteurs")
                donnee_agre = donnee_agre.rename(
                    columns={
                        "tata": "TATA",
                        "Prenom_Nom_Promoteur": "Promoteur",
                        "Montant": "CA SEMAINE",
                    }
                )

                donnee_ordre = donnee_agre.sort_values(by=["Promoteur"], ascending=False)
        elif choix == "Produit":
            menu_prin=st.sidebar.selectbox("PRODUITS", produit_list)
            donnee2 = donnee1[(donnee["Produit"] == menu_prin)]
            donne_vente = donnee2[donnee2["Operation"] == "Vente"]
            donnee_agre = (
                donne_vente.groupby(["tata","zone","Prenom_Nom_Promoteur","Produit"])
                .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
                .reset_index()
            )

            st.subheader("Ventes de promoteurs")
            if periode == "Semaine":
                donnee_agre = donnee_agre.rename(
                    columns={
                        "tata": "TATA",
                        "Prenom_Nom_Promoteur": "Promoteur",
                        "Quantites_Cartons": "Quantités",
                        "Montant": "CA SEMAINE",
                    }
                )
            elif periode == "Jour":
                donnee_agre = donnee_agre.rename(
                    columns={
                        "tata": "TATA",
                        "Prenom_Nom_Promoteur": "Promoteur",
                        "Quantites_Cartons": "Quantités",
                        "Montant": "Montant A verser",
                    }
                )
            donnee_ordre = donnee_agre.sort_values(by=["TATA","Promoteur"], ascending=False)

    elif tat_indi == "TATA":
        donnee2 = donnee1[(donnee["tata"] == menu_sambou)]
        donne_vente = donnee2[donnee2["Operation"] == "Vente"]
        donnee_agre = (
            donne_vente.groupby(["tata","zone","Produit"])
            .agg({"Quantites_Cartons": "sum", "Montant": "sum"})
            .reset_index()
        )

        st.subheader("Ventes de promoteurs")
        if periode == "Semaine":
            donnee_agre = donnee_agre.rename(
                columns={
                    "tata": "TATA",
                    "Quantites_Cartons": "Quantités",
                    "Montant": "CA SEMAINE",
                }
            )
        elif periode == "Jour":
            donnee_agre = donnee_agre.rename(
                columns={
                    "tata": "TATA",
                    "Quantites_Cartons": "Quantités",
                    "Montant": "Montant A verser",
                }
            )
        donnee_ordre = donnee_agre.sort_values(by=["TATA"], ascending=False)
    #donnee_agre["Date"] = donnee_agre["Date"].dt.strftime("%d/%m/%Y")
    st.dataframe(donnee_ordre.drop("TATA", axis=1))
    
    colone= st.columns(3)
    if periode== "Semaine":
        colone[1].metric("💴 CA TATA", f"{donnee_ordre[donnee_ordre["TATA"] ==menu_sambou]["CA SEMAINE"].sum():,.0f}".replace(",", " ")+" XOF")
    elif periode == "Jour":
        colone[1].metric("💴 CA TATA", f"{donnee_ordre[donnee_ordre["TATA"] ==menu_sambou]["Montant A verser"].sum():,.0f}".replace(",", " ")+" XOF")
#-----------------------------------------------------------------#
# Dans votre onglet VALERIE
elif menu == "FICHE":
    Donnees_Mens = pd.read_excel("Donnees_Mensuelle.xlsx", engine='openpyxl')
    periode = "Semaine"
    if periode == "Semaine":
        st.sidebar.markdown("---")
        password = st.sidebar.text_input("Code d'accès requis", type="password")
        # Récupération sécurisée du secret
        VALERIE = st.secrets["credentials"]["valerie"]
        OMAR = st.secrets["credentials"]["omar"]
        MANSOUR = st.secrets["credentials"]["mansour"]
        DJIBRIL = st.secrets["credentials"]["djibril"]
        IBRAHIMA = st.secrets["credentials"]["ibrahima"]

        if password == DJIBRIL:
            prom ="TATA 1"
            st.success("ACCES AUTORISE POUR DJIBRIL")
            
            data_semaine = Donnees_Mens[
                (Donnees_Mens["Numero_semaine"] == semaine) &
                (Donnees_Mens["Prenom_Nom_Promoteur"] != "Autre") &
                (Donnees_Mens["Prenom_Nom_Promoteur"].notna()) &
                (Donnees_Mens['tata'] == prom)
            ]
        elif password == MANSOUR:
            prom = "TATA 2"
            st.success("ACCES AUTORISE POUR MANSOUR")
            data_semaine = Donnees_Mens[
                (Donnees_Mens["Numero_semaine"] == semaine) &
                (Donnees_Mens["Prenom_Nom_Promoteur"] != "Autre") &
                (Donnees_Mens["Prenom_Nom_Promoteur"].notna()) &
                (Donnees_Mens['tata'] == prom)
            ]
        elif password == IBRAHIMA:
            prom = "TATA 3"
            st.success("ACCES AUTORISE POUR IBRAHIMA")
            data_semaine = Donnees_Mens[
                (Donnees_Mens["Numero_semaine"] == semaine) &
                (Donnees_Mens["Prenom_Nom_Promoteur"] != "Autre") &
                (Donnees_Mens["Prenom_Nom_Promoteur"].notna()) &
                (Donnees_Mens['tata'] == prom)
            ]
        elif password == VALERIE:
            prom = colone[4].selectbox("", ["TATA 1","TATA 2","TATA 3"])
            st.success("ACCES AUTORISE POUR Mme KOFFI")
            Donnees_F = pd.read_excel("Donnees_F.xlsx", engine='openpyxl')
            data_semaine = Donnees_F[
                (Donnees_F["Numero_semaine"] == semaine) &
                (Donnees_F["Prenom_Nom_Promoteur"] != "Autre") &
                (Donnees_F["Prenom_Nom_Promoteur"].notna()) &
                (Donnees_F['tata'] == prom)
            ]
        elif password == OMAR:
            prom = colone[4].selectbox("", ["TATA 1","TATA 2","TATA 3"])
            choix_om=st.sidebar.radio("FICHIER", options=["FICHE", "RAPPORT"])
            if choix_om == "FICHE":
                # Le vrai rapport
                
                st.success("ACCES AUTORISE POUR OMAR AU VERSION 1")
                data_semaine = Donnees_Mens[
                    (Donnees_Mens["Numero_semaine"] == semaine) &
                    (Donnees_Mens["Prenom_Nom_Promoteur"] != "Autre") &
                    (Donnees_Mens["Prenom_Nom_Promoteur"].notna()) &
                    (Donnees_Mens['tata'] == prom)
                ]
            elif choix_om == "RAPPORT":
                # Pour le rapport modifié
                st.success("ACCES AUTORISE POUR OMAR AU VERSION 2")
                Donnees_F = pd.read_excel("Donnees_F.xlsx", engine='openpyxl')
                data_semaine = Donnees_F[
                (Donnees_F["Numero_semaine"] == semaine) &
                (Donnees_F["Prenom_Nom_Promoteur"] != "Autre") &
                (Donnees_F["Prenom_Nom_Promoteur"].notna()) &
                (Donnees_F['tata'] == prom)
            ]
        elif password == "":
            st.warning("Veuillez entrer un code d'accès pour continuer.")
            st.stop()
        else:
            st.error("Code d'accès incorrect. Veuillez réessayer.")
            st.stop()
        jour_min = data_semaine["Date"].min().day
        jour_max = data_semaine["Date"].max().day
        mois_num = data_semaine["Date"].min().month
        annee=data_semaine["Date"].min().year

        mois_fr = {
            1: "JANVIER", 2: "FÉVRIER", 3: "MARS",
            4: "AVRIL", 5: "MAI", 6: "JUIN",
            7: "JUILLET", 8: "AOÛT", 9: "SEPTEMBRE",
            10: "OCTOBRE", 11: "NOVEMBRE", 12: "DÉCEMBRE"
        }

        mois_lettre = mois_fr[mois_num]

        texte_periode = f"DU {jour_min} AU {jour_max} {mois_lettre} {annee}"
        st.markdown(f"""<h4 style='text-align: center;'>FICHE DE PAIE {prom} DU {texte_periode}</h4>""", unsafe_allow_html=True)

        # =========================
        # 🔹 CREATION DE "suivi"
        # =========================

        suivi = data_semaine.groupby(
            ['Prenom_Nom_Promoteur']
        )['Date'].nunique().reset_index()

        suivi.rename(columns={
            'Prenom_Nom_Promoteur': 'Nom',
            'Date': 'Jours travaillés'
        }, inplace=True)

        suivi['Salaire'] = suivi['Jours travaillés'] * 4000

        total = suivi['Salaire'].sum()

        # =========================
        # AFFICHAGE
        # =========================
        affichage=suivi.copy()
        affichage["Nom"] = affichage["Nom"].str.upper()
        st.dataframe(affichage)
        st.metric("💰 Total à payer", f"{total:,.0f} XOF".replace(",", " "))

        # =========================
        # 🔹 GENERATION PDF
        # =========================
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from io import BytesIO
        import os

        def generate_pdf_paie(df, prom, jour_min, jour_max, mois_lettre, annee):
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                    rightMargin=2*cm, leftMargin=2*cm,
                                    topMargin=2*cm, bottomMargin=2*cm)

            styles = getSampleStyleSheet()
            elements = []
            texte_periode = f"DU {jour_min} AU {jour_max} {mois_lettre} {annee}"
            # =========================
            # 🔹 HEADER (LOGO + TATA)
            # =========================

            logo_path = "afrika_leyri_sas_logo.jpeg"  # vérifie bien le nom exact !

            if os.path.exists(logo_path):
                logo = Image(logo_path, width=2.5*cm, height=1.5*cm)
            else:
                logo = Paragraph("", styles["Normal"])

            tata_text = Paragraph(f"<b>{prom}</b>", styles["Heading2"])

            header_table = Table(
                [[logo, tata_text]],
                colWidths=[14*cm, 3*cm]
            )

            header_table.setStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('ALIGN', (1,0), (1,0), 'LEFT'),  # TATA à droite
            ])

            elements.append(header_table)
            elements.append(Spacer(1, 5))

            # =========================
            # 🔹 TITRE
            # =========================

            style_titre = ParagraphStyle(
                name="TitrePerso",
                parent=styles["Title"],
                fontSize=12,   # 👈 taille réelle
                leading=14,
                alignment=1    # centré
            )

            titre = Table(
                [[Paragraph(
                    f"<b>ACTIVATION KAMLAC_PAIE SALAIRES FIXES {texte_periode}</b>",
                    style_titre
                )]],
                colWidths=[16.1*cm]
            )

            titre.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7CC0C")),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('TOPPADDING', (0,0), (-1,-1), 6),
            ]))

            elements.append(titre)
            elements.append(Spacer(0, 0))

            # =========================
            # 🔹 TABLEAU
            # =========================
            data = [["PRENOM & NOM", "JOURS TRAVAILLES", "MONTANT PAYE", "SIGNATURE"]]

            for _, row in df.iterrows():
                data.append([
                    row["Nom"].upper(),
                    row["Jours travaillés"],
                    f"{int(row['Salaire']):,}".replace(",", " "),
                    ""
                ])


            table = Table(data, colWidths=[5*cm, 4*cm, 4*cm, 3*cm])

            table.setStyle(TableStyle([
                # Bordures
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                # 🔥 Bordure extérieure en orange
                ('BOX', (0,0), (-1,-1), 2, colors.HexColor("#F7CC0C")),

                # Header (entête)
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D7D2C9")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

                # 🔥 Cellule spécifique en rose
                ('BACKGROUND', (1,0), (1,0), colors.HexColor("#EECC92")),
                ('TEXTCOLOR', (1,0), (1,0), colors.black),

                # Alignement
                ('ALIGN',(1,1),(-2,-1),'CENTER'),
                ('ALIGN',(0,0),(-1,0),'CENTER'),
                ('ALIGN',(0,-1),(0,-1),'CENTER'),

                # Ligne TOTAL
                ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
                ('TEXTCOLOR', (0,-1), (-1,-1), colors.black),
                ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),

                # Padding
                ('BOTTOMPADDING', (0,0), (-1,-1), 8),
                ('TOPPADDING', (0,0), (-1,-1), 8),
            ]))

            elements.append(table)

            doc.build(elements)
            buffer.seek(0)

            return buffer

        # =========================
        # 🔹 AJOUT LIGNE TOTAL
        # =========================
        df_total = suivi.copy()
        df_total.loc[len(df_total)] = ["TOTAL", "", total]
        
        # =========================
        # 🔹 DOWNLOAD PDF
        # =========================
        pdf_file = generate_pdf_paie(df_total, prom, jour_min, jour_max, mois_lettre, annee)

        st.download_button(
            label="📥 Télécharger la fiche de paie PDF",
            data=pdf_file,
            file_name=f"FICHE DE PAIE {prom} DU {jour_min:02d} AU {jour_max:02d} {mois_num}.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("Disponible uniquement en mode Semaine")