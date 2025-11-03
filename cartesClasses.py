
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

"""
# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CardDomain", fontSize=12, leading=18, alignment=0, textColor=colors.black, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CardTitle", fontSize=10, leading=12, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=8))
styles.add(ParagraphStyle(name="CardSub", fontSize=9, leading=8, alignment=2, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=4))
styles.add(ParagraphStyle(name="CardText", fontSize=8, leading=9, alignment=4, fontName="Helvetica", spaceAfter=4))
styles.add(ParagraphStyle(name="CardFooter", fontSize=7, leading=8, alignment=0, textColor=colors.grey, fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle(name="CardType", fontSize=10, leading=11, alignment=1, textColor=colors.black, fontName="Helvetica-Oblique", spaceAfter=4, spaceBefore=4))
"""


def get_classes_a_imprimer(classe):
    return "TOUTES"

def ajouter_cartes(story, classe, lang):
    # Détermination des domaines à imprimer (cas pack classes)
    classes_a_imprimer = get_classes_a_imprimer(classe)

    # Charger le JSON
    with open(common.DIR_JSON + f"{lang}/classes_{lang}.json", "r", encoding="utf-8") as f:
        cartes = json.load(f)

    # Ajout des cartes dans la story
    for i, carte in enumerate(cartes):

        # Nom Classe
        titre = f"""{carte["name"].upper()}"""

        pg_titre = [[Paragraph(titre, common.styles["CardTitle"])]]
        tbl_class = Table(pg_titre)
        tbl_class.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),['HORIZONTAL', common.domain_bg_colors.get(carte["domain_1"], colors.white),common.domain_bg_colors.get(carte["domain_2"], colors.white)]),
                                            ]))
        story.append(tbl_class)

        # Domaines
        crt_tp=f"{carte["domain_1"]} - {carte["domain_2"]}"
        pg_type = Paragraph(crt_tp, common.styles["CardSubTitle"])
        story.append(pg_type)
        
        # Description
        resume = common.premieres_phrases(carte["description"], 2)
        pg_desc = Paragraph(resume, common.styles["CardText"])
        story.append(pg_desc)

        # Informations additionnelles
        spe = f"""Spécialisations :  {carte["subclass_1"]}, {carte["subclass_2"]}"""
        pg_spe = Paragraph(spe, common.styles["CardSub"])
        story.append(pg_spe)

        # Passe à la carte suivante
        story.append(FrameBreak())  

        # Classe
        story.append(tbl_class)

        # Sous-Type de carte : Capacité d'Espoir
        crt_tp=f"""{translate("classe espoir", lang)}"""
        pg_type = Paragraph(crt_tp, common.styles["CardSubTitle"])
        story.append(pg_type)

        # Description Capacité d'Espoir
        hope = markdown2.markdown(f"""<b>{carte["hope_feat_name"]}</b>&nbsp;:&nbsp;{carte["hope_feat_text"]}""")
        pg_hope = Paragraph(hope, common.styles["CardText"])
        story.append(pg_hope)

        # Passe à la carte suivante
        story.append(FrameBreak())  

        # Classe
        story.append(tbl_class)

        # Sous-Type de carte : Capacités de classe
        crt_tp=f"""{translate("classe capacites", lang)}"""
        pg_type = Paragraph(crt_tp, common.styles["CardSubTitle"])
        story.append(pg_type)

        # Descriptions Capacités de classe
        for j, capa in enumerate(carte["class_feats"]):
            capacite = markdown2.markdown(f"""<b>{capa["name"]}</b>&nbsp;:&nbsp;{capa["text"]}""")
            pg_capa = Paragraph(capacite, common.styles["CardText"])
            story.append(pg_capa)

        # Passe à la carte suivante
        story.append(FrameBreak())  

def exe_unitaire(classe, lang):

    # Création du document
    doc = BaseDocTemplate(f"pdf/classes_{lang}.pdf", pagesize=A4)

    doc.addPageTemplates(common.creer_template(lang))

    # Construction du contenu
    story = []

    # Première page
    titre_ppage = translate("ppage titre classe", lang)
    sstitre_ppage = f"""{translate("ppage sstitre classe", lang)} {classe}<br/>
    {translate("ppage sstitre langue", lang)} {lang} {translate("ppage sstitre trad", lang)}
    """

    firstPage.ajouter_ppage_legale(story, titre_ppage, sstitre_ppage, "")

    # Pages suivantes : cartes
    story.append(NextPageTemplate('grid'))
    story.append(PageBreak())

    # Pages suivantes
    ajouter_cartes(story, classe, lang)

    # Génération du PDF
    doc.build(story)






