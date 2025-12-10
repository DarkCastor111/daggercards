
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

def get_niveaux_a_imprimer(tier):
    # Détermination des niveaux à imprimer en fonction du rang
    liste_niveaux = []
    if "1" in tier:
        liste_niveaux.append("1")
        print(liste_niveaux)
    if "2" in tier:
        liste_niveaux.extend(["2","3","4"])
        print(liste_niveaux)
    if "3" in tier:
        liste_niveaux.extend(["5","6","7"])
        print(liste_niveaux)
    if "4" in tier:
        liste_niveaux.extend(["8","9","10"])
        print(liste_niveaux)
    return liste_niveaux

def get_domaines_a_imprimer(classe):
    if classe == "Warior":
        liste_domaines=["Arcana","Blade"]
    else:
        liste_domaines=["Arcana","Blade","Bone","Codex","Grace","Midnight","Sage","Splendor","Valor"]
    return liste_domaines


def ajouter_cartes(story, rang, classe, lang):
    # Charger le JSON
    with open(common.DIR_JSON + f"{lang}/abilities_{lang}.json", "r", encoding="utf-8") as f:
        cartes = json.load(f)

    # Détermination des niveaux à imprimer en fonction du rang
    niveaux_a_imprimer = get_niveaux_a_imprimer(rang)

    # Détermination des domaines à imprimer (cas pack classes)
    domaines_a_imprimer = get_domaines_a_imprimer(classe)


    # Ajout des cartes dans la story
    for domaine in domaines_a_imprimer:

        for i, carte in enumerate(cartes):
            niveau_carte = carte['level']
            domaine_carte = carte['domain']
            if niveau_carte in niveaux_a_imprimer and domaine_carte == domaine :

                # Titre : Domaine - Niveau - Type
                titre = f"""
                &nbsp;{carte["domain"].upper()} - {carte['level']} - {carte['type'].upper()}
                """
                pg_titre = [[Paragraph(titre, common.styles["CardTitle"])]]

                tbl_titre = Table(pg_titre)
                tbl_titre.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),common.domain_bg_colors.get(domaine_carte, colors.white))]))
                story.append(tbl_titre)

                # Domaine et niveau de la Carte
                #story.append(pg_domain)
                
                # Nom de la carte
                pg_title = Paragraph(carte["name"].upper(), common.styles["CardName"])
                story.append(pg_title)


                # Texte
                pg_text = Paragraph(markdown2.markdown(carte["text"].replace("\n", "<br/>")), common.styles["CardText"])
                story.append(pg_text)

                # Infos secondaires
                infoSecondaires = f"""
                <b>{translate("domaine", lang)} - {translate("rappel", lang)}:</b> {carte['recall']} <b>Stress</b>
                """
                pg_sub = Paragraph(infoSecondaires, common.styles["CardSub"])
                story.append(pg_sub)

                # Passe à la carte suivante
                story.append(FrameBreak())  


def exe_unitaire(rang, classe, lang):

    # Création du document
    doc = BaseDocTemplate(f"pdf/abilities_{lang}_{rang}.pdf", pagesize=A4)

    doc.addPageTemplates(common.creer_template(lang))

    # Construction du contenu
    story = []

    # Première page
    titre_ppage = translate("ppage titre domaine", lang)
    sstitre_ppage = f"""{translate("ppage sstitre rang", lang)} {rang}<br/>
    {translate("ppage sstitre langue", lang)} {lang} {translate("ppage sstitre trad", lang)}
    """
    sstitre_ppage += f"""<br/>
        {translate("ppage sstitre version", lang)} {common.VERSION_DOM}"""

    firstPage.ajouter_ppage_legale(story, lang, titre_ppage, sstitre_ppage, "")

    # Pages suivantes : cartes
    story.append(NextPageTemplate('grid'))
    story.append(PageBreak())

    # Pages suivantes
    ajouter_cartes(story, rang, classe, lang)

    # Génération du PDF
    doc.build(story)
