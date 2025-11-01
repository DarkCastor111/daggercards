
import json
import markdown2

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, Table, TableStyle
from reportlab.platypus import BaseDocTemplate, FrameBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors

from footer import add_background
import common
from translator import translate
import firstPage

def get_niveaux_a_imprimer(tier):
    # Détermination des niveaux à imprimer en fonction du rang
    if tier == "1":
        liste_niveaux = ["1"]
    elif tier == "2":
        liste_niveaux = ["1","2","3","4"]
    elif tier == "3":
        liste_niveaux = ["1","2","3","4","5","6","7"]
    else:
        liste_niveaux = ["1","2","3","4","5","6","7","8","9","10"]
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
                <b>{translate("domaine",common.langage)} - {translate("rappel",common.langage)}:</b> {carte['recall']} <b>Stress</b>
                """
                pg_sub = Paragraph(infoSecondaires, common.styles["CardSub"])
                story.append(pg_sub)

                # Passe à la carte suivante
                story.append(FrameBreak())  


def exe_unitaire(rang, classe, lang):

    # Création du document
    doc = BaseDocTemplate(f"pdf/abilities_{lang}_{rang}.pdf", pagesize=A4)

    # Cadre des cartes (3x3 par page)
    frames = common.cards_frames

    # Définition du template pour la première page
    template_ppage = firstPage.ppage_template
    # Définition du template pour les cartes
    template_cartes = PageTemplate(id="grid", frames=frames, onPage=add_background)

    doc.addPageTemplates([template_ppage, template_cartes])

    # Construction du contenu
    story = []

    # Première page
    titre_ppage = translate("ppage titre domaine", lang)
    sstitre_ppage = f"""{translate("ppage sstitre rang", lang)} {rang}<br/>
    {translate("ppage sstitre classe", lang)} {classe}<br/>
    {translate("ppage sstitre langue", lang)} {lang}
    """
    firstPage.ajouter_ppage(story, titre_ppage, sstitre_ppage)

    # Pages suivantes
    ajouter_cartes(story, rang, classe, lang)

    # Génération du PDF
    doc.build(story)
