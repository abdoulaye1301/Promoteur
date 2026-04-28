import base64
from weasyprint import HTML
# --- Fonction utilitaire pour encoder l'image en base64 (pour le PDF) ---
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return ""
    
# Fonction de formatage avec espace pour les milliers
def format_mille(valeur):
    return "{:,.0f}".format(valeur).replace(",", " ")


# --- Fonction pour afficher le PDF dans Streamlit ---
def display_pdf(pdf_bytes):
    # Encodage en base64 pour l'affichage iframe
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    # Création du code HTML pour l'iframe
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

    # 2. Construction du HTML pour le PDF (Modèle exact du PDF téléchargé)
    logo_b64 = get_image_base64("Logo Afrika Leyri.png")
    
    # Dates dynamiques (à adapter selon votre colonne Date si disponible)
    titre_periode = f"PAIE SALAIRES FIXES SEMAINE {semaine}" 

    # --- Mise à jour du template HTML pour le PDF ---

    html_template = f"""
    <html>
    <head>
        <style>
            @page {{ 
                size: A4; 
                margin: 15mm; 
            }}
            body {{ 
                font-family: 'Helvetica', Arial, sans-serif; 
                color: #000; 
            }}
            
            /* Structure de l'en-tête pour aligner Logo (Gauche) et Nom (Droite) */
            .header-table {{ 
                width: 100%; 
                border-bottom: 2px solid #000; 
                padding-bottom: 10px; 
                margin-bottom: 20px; 
            }}
            .logo-cell {{ 
                text-align: left; 
                vertical-align: middle; 
            }}
            .company-cell {{ 
                text-align: right; 
                vertical-align: middle; 
                font-size: 18pt; 
                font-weight: bold; 
                letter-spacing: 1px;
            }}
            
            .main-title {{ 
                text-align: center; 
                font-size: 12pt; 
                font-weight: bold; 
                margin: 25px 0; 
                text-transform: uppercase; 
                line-height: 1.4; 
            }}
            
            table.data {{ 
                width: 100%; 
                border-collapse: collapse; 
            }}
            th {{ 
                border: 1px solid #000; 
                padding: 10px; 
                background-color: #f2f2f2; 
                font-size: 9pt; 
                text-transform: uppercase;
            }}
            td {{ 
                border: 1px solid #000; 
                padding: 8px; 
                text-align: center; 
                font-size: 10pt; 
            }}
            .total-row {{ 
                font-weight: bold; 
                background-color: #eee; 
            }}
        </style>
    </head>
    <body>
        <table class="header-table">
            <tr>
                <td class="logo-cell">
                    <img src="data:image/png;base64,{logo_b64}" style="width: 140px;">
                </td>
                <td class="company-cell">
                    {prom}
                </td>
            </tr>
        </table>

        <div class="main-title">
            ACTIVATION KAMLAC PAIE SALAIRES FIXES DE LA SEMAINE {semaine})
        </div>

        <table class="data">
            <thead>
                <tr>
                    <th>PRENOM & NOM</th>
                    <th>JOURS TRAVAILLES</th>
                    <th>MONTANT PAYE</th>
                    <th>SIGNATURE</th>
                </tr>
            </thead>
            <tbody>
                {"".join([f"<tr><td style='text-align: left;'>{r['PRENOM & NOM']}</td><td>{r['JOURS TRAVAILLES']}</td><td>{format_mille(r['MONTANT PAYE'])}</td><td></td></tr>" for _, r in suivi_assiduite.iterrows()])}
                <tr class="total-row">
                    <td colspan="2">TOTAL</td>
                    <td>{format_mille(total_montant)}</td>
                    <td></td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    """

    pdf_bytes = HTML(string=html_template).write_pdf()
    # 2. Zone de prévisualisation
    st.subheader("Aperçu de la fiche de paie")
    display_pdf(pdf_bytes)
    
    st.write("---")
    st.download_button(
        label="📥 Télécharger la Fiche de Paie PDF",
        data=pdf_bytes,
        file_name=f"Fiche_Paie_{prom}_S{semaine}.pdf",
        mime="application/pdf"
    )