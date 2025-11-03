
import json
import markdown2


from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, Table, TableStyle
from reportlab.platypus import BaseDocTemplate, FrameBreak, PageBreak, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

import common
from translator import translate
import firstPage

def ajouter_cartes(story, type_carte, lang):
    #Choix du JSON
    fichier_json = common.DIR_JSON + f"/{lang}/communities_{lang}.json"
    if type_carte == "ascendance":
        fichier_json = common.DIR_JSON + f"/{lang}/ancestries_{lang}.json"

    # Charger le JSON
    with open(fichier_json, "r", encoding="utf-8") as f:
        cartes = json.load(f)

    # Ajouter les cartes dans la story
    for i, carte in enumerate(cartes):

        # Titre de la carte
        titre=f"&nbsp;{carte["name"].upper()}"

        if type_carte == "origine":
            card_titre_style = ParagraphStyle(
                name="CardTitre_Origine",
                parent=common.styles["CardTitle"],
                #textColor=colors.darkslategray, backColor=colors.darkturquoise
                textColor=colors.darkslategray
            )
        else:
            card_titre_style = ParagraphStyle(
                name="CardTitre_Heritage",
                parent=common.styles["CardTitle"],
                #textColor=colors.maroon, backColor=colors.orange
                textColor=colors.maroon
            )
        
        pg_titre = [[Paragraph(titre, card_titre_style)]]
        
        tbl_titre = Table(pg_titre)
        if type_carte == "origine":
            tbl_titre.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),colors.darkturquoise)]))
        else:
            tbl_titre.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),colors.orange)]))
        story.append(tbl_titre)

        story.append(Spacer(1, 0.2*cm))

        # Présentation
        resume = common.premieres_phrases(carte["description"], 2)
        pg_desc = Paragraph(resume, common.styles["CardPres"])
        story.append(pg_desc)


        # Capacités
        for j, capa in enumerate(carte["feats"]):
            capacite = markdown2.markdown(f"""<b>{capa["name"]}</b>&nbsp;: {capa["text"]}""")
            pg_capa = Paragraph(capacite, common.styles["CardText"])
            story.append(pg_capa)

        # Infos secondaires
        infoSecondaires = f"""
        {translate(type_carte, lang)}
        """
        pg_sub = Paragraph(infoSecondaires, common.styles["CardSub"])
        story.append(pg_sub)

        # Passe à la carte suivante
        story.append(FrameBreak())  
    

def exe_unitaire(type_carte, lang):
        
    fichier_pdf = f"pdf/communities_{lang}.pdf"

    if type_carte == "ascendance":
        fichier_pdf = f"pdf/ancestries_{lang}.pdf"

    # Création du document
    doc = BaseDocTemplate(fichier_pdf, pagesize=A4)
    
    doc.addPageTemplates(common.creer_template(lang))

    # Construction du contenu
    story = []

    # Première page
    titre_ppage = translate("ppage titre " + type_carte, lang)
    sstitre_ppage = f"""{translate("ppage sstitre langue", lang)} {lang}"""
    firstPage.ajouter_ppage_legale(story, titre_ppage, sstitre_ppage)

    # Pages suivantes : cartes
    story.append(NextPageTemplate('grid'))
    story.append(PageBreak())

    ajouter_cartes(story, type_carte, lang)

    # Génération du PDF
    doc.build(story)
