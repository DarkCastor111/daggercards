
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

def get_specialisation_a_imprimer(tier):
    liste_specialisations = []
    if "1" in tier or "2" in tier:
        liste_specialisations.append("foundations")
    if "3" in tier:
        liste_specialisations.append("specializations")
    if "4" in tier:
        liste_specialisations.append("masteries")


    return liste_specialisations

def ajouter_cartes(story, rang, lang):
    
    specialisations_a_imprimer = get_specialisation_a_imprimer(rang)    
    
    # Charger le JSON
    with open(common.DIR_JSON + f"{lang}/subclasses_{lang}.json", "r", encoding="utf-8") as f:
        cartes = json.load(f)

    for i, carte in enumerate(cartes):

        for carte_type in specialisations_a_imprimer:

            # Nom Sous Classe
            titre = f"""{carte["name"].upper()}"""

            pg_titre = [[Paragraph(titre, common.styles["CardTitle"])]]
            tbl_domain = Table(pg_titre)
            tbl_domain.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),['HORIZONTAL', common.domain_bg_colors.get(carte["domain_1"], colors.white),common.domain_bg_colors.get(carte["domain_2"], colors.white)]),
                                            ]))

            story.append(tbl_domain)

            # Type de Carte
            crt_tp=f"{translate(carte_type, lang)}"
            pg_type = Paragraph(crt_tp, common.styles["CardSubTitle"])
            story.append(pg_type)

            # Description, seulement sur la première carte
            if carte_type == "foundations":
                crt_desc=f"""{carte["description"]}"""
                pg_desc = Paragraph(crt_desc, common.styles["CardText"])
                story.append(pg_desc)
            
            # Capacités du type de carte
            for j, capa in enumerate(carte[carte_type]):
                capacite = f"""<b>{capa["name"]}</b>&nbsp;:&nbsp;{markdown2.markdown(capa["text"].replace("\n", "<br/>"))}"""
                pg_capa = Paragraph(capacite, common.styles["CardText"])
                story.append(pg_capa)

            # Informations additionnelles
            spe = f"""{translate('sous classe de', lang)} {carte["class"].upper()}"""
            pg_spe = Paragraph(spe, common.styles["CardSub"])
            story.append(pg_spe)

            if carte_type == "foundations" and carte.get("spellcast_trait") :
                inc = f"""{translate('trait incantation', lang)} {carte["spellcast_trait"]}"""
                pg_inc = Paragraph(inc, common.styles["CardSub"])
                story.append(pg_inc)

            # Passe à la carte suivante
            story.append(FrameBreak())  




def exe_unitaire(rang, lang):

    liste_specialisations = get_specialisation_a_imprimer(rang)

    # Création du document
    doc = BaseDocTemplate(f"pdf/subclasses_{lang}_{rang}.pdf", pagesize=A4)

    doc.addPageTemplates(common.creer_template(lang))

    # Construction du contenu
    story = []

    # Première page
    titre_ppage = translate("ppage titre sous classe" ,lang)
    sstitre_ppage = f"""{translate("ppage sstitre rang" ,lang)} {rang} - """
    for spe in liste_specialisations:
        spe_traduite = f"{translate(spe, lang)} "
        sstitre_ppage += spe_traduite
    sstitre_ppage += f"""<br/>
    {translate("ppage sstitre langue", lang)} {lang} {translate("ppage sstitre trad", lang)}"""
    sstitre_ppage += f"""<br/>
        {translate("ppage sstitre version", lang)} {common.VERSION_SSC}"""
    firstPage.ajouter_ppage_legale(story, lang, titre_ppage, sstitre_ppage, "")

    story.append(NextPageTemplate('grid'))
    story.append(PageBreak())

    # Pages suivantes : cartes
    ajouter_cartes(story, rang, lang) 

    # Génération du PDF
    doc.build(story)
