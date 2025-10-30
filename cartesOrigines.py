
import json
import markdown2


from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, Table, TableStyle
from reportlab.platypus import BaseDocTemplate, FrameBreak, PageBreak, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

from footer import add_background
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
        {translate(type_carte, common.langage)}
        """
        pg_sub = Paragraph(infoSecondaires, common.styles["CardSub"])
        story.append(pg_sub)

        # Passe à la carte suivante
        story.append(FrameBreak())  
    

def exe():
        

    titre_carte="origine"
    #titre_carte="ascendance"

    fichier_json = common.DIR_JSON + f"/{common.langage}/communities_{common.langage}.json"
    fichier_pdf = f"pdf/communities_{common.langage}.pdf"

    if titre_carte == "ascendance":
        fichier_json = common.DIR_JSON + f"/{common.langage}/ancestries_{common.langage}.json"
        fichier_pdf = f"pdf/ancestries_{common.langage}.pdf"

    # Charger le JSON
    with open(fichier_json, "r", encoding="utf-8") as f:
        cartes = json.load(f)

    # Création du document
    doc = BaseDocTemplate(fichier_pdf, pagesize=A4)


    # Styles de première page
    #styles.add(firstPage.style_titre)


    # Cadre des cartes (3x3 par page)
    frames = common.cards_frames

    # Définition du template pour la première page
    template_ppage = firstPage.ppage_template
    # Définition du template pour les cartes
    template_cartes = PageTemplate(id="grid", frames=frames, onPage=add_background)

    doc.addPageTemplates([firstPage.ppage_template, template_cartes])

    # Construction du contenu
    story = []

    # Première page
    titre_ppage = translate("ppage titre " + titre_carte, common.langage)
    sstitre_ppage = f"""{translate("ppage sstitre langue", common.langage)} {common.langage}
    """
    firstPage.ajouter_ppage(story, titre_ppage, sstitre_ppage)

    # Pages suivantes
    for i, carte in enumerate(cartes):

        # Titre de la carte
        titre=f"&nbsp;{carte["name"].upper()}"

        if titre_carte == "origine":
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
        if titre_carte == "origine":
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
        {translate(titre_carte, common.langage)}
        """
        pg_sub = Paragraph(infoSecondaires, common.styles["CardSub"])
        story.append(pg_sub)


        # Passe à la carte suivante
        story.append(FrameBreak())  

    # Génération du PDF
    doc.build(story)
