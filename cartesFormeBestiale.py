
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

def get_rangs_a_imprimer(tier):
    # Détermination des niveaux à imprimer en fonction du rang
    liste_rang = []
    if "1" in tier:
        liste_rang.append("1")
        print(liste_rang)
    if "2" in tier:
        liste_rang.extend(["1","2"])
        print(liste_rang)
    if "3" in tier:
        liste_rang.extend(["1","2","3"])
        print(liste_rang)
    if "4" in tier:
        liste_rang.extend(["1","2","3","4"])
        print(liste_rang)
    return liste_rang

def ajouter_cartes(story, rang, lang):
    
    # Charger le JSON
    with open(common.DIR_JSON + f"{lang}/classes_druid_beastform_{lang}.json", "r", encoding="utf-8") as f:
        cartes = json.load(f)

    # Ajout des cartes dans la story
    for i, carte in enumerate(cartes):

        # Nom Carte
        titre = f"""{carte["name"].upper()} """

        pg_titre = [[Paragraph(titre, common.styles["CardTitle"])]]
        tbl_capa = Table(pg_titre)
        tbl_capa.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),['HORIZONTAL', common.domain_bg_colors.get("Sage", colors.white),common.domain_bg_colors.get("Arcana", colors.white)]),
                                            ]))
        story.append(tbl_capa)

        # Sous-Type de carte : Description
        crt_tp=f"""{translate("beastform description", lang)}"""
        pg_type = Paragraph(crt_tp, common.styles["CardSubTitle"])
        story.append(pg_type)
        
        # Texte Description
        desc = markdown2.markdown(f"""{carte["text"].replace("\n", "<br/>")}""")
        pg_desc = Paragraph(desc, common.styles["CardText"])
        story.append(pg_desc)

        # Infos secondaires : Type de carte
        infoSecondaires = f"""{translate("beastform sub", lang)}"""
        pg_sub = Paragraph(infoSecondaires, common.styles["CardSub"])
        story.append(pg_sub)

        # Passe à la carte suivante
        story.append(FrameBreak())  

        # Nom Carte
        #story.append(tbl_capa)

        # Sous-Type de carte : Options
        #crt_tp=f"""{translate("beastform options", lang)}"""
        #pg_type = Paragraph(crt_tp, common.styles["CardSubTitle"])
        #story.append(pg_type)

        # Texte Options
        #options = markdown2.markdown(f"""{carte["option_text"]}""")
        #pg_hope = Paragraph(options, common.styles["CardText"])
        #story.append(pg_hope)

        # Passe à la carte suivante
        #story.append(FrameBreak())

        # OPTIONS
        rangs_a_imprimer = get_rangs_a_imprimer(rang)

        for j, opt in enumerate(carte["options"]):

            if opt["tier"] in rangs_a_imprimer:
                # Nom Carte
                titre = f"""{opt["tier"]} - {opt["name"].upper()}"""

                pg_titre = [[Paragraph(titre, common.styles["CardTitle"])]]
                tbl_capa = Table(pg_titre)
                tbl_capa.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),['HORIZONTAL', common.domain_bg_colors.get("Sage", colors.white),common.domain_bg_colors.get("Arcana", colors.white)]),
                                                ]))
                story.append(tbl_capa)

                # Exemples d'animaux
                ani_txt = f"""{opt["examples"]}"""
                pg_ani = Paragraph(ani_txt, common.styles["CardSubTitle"])
                story.append(pg_ani)

                # Bonus Traits
                bonus_txt = f"""{opt["bonus"]}"""
                pg_bonus = Paragraph(bonus_txt, common.styles["CardText"])
                story.append(pg_bonus)

                # Attaque
                atk_txt = f"""{opt["attack"]}"""
                pg_atk = Paragraph(atk_txt, common.styles["CardText"])
                story.append(pg_atk)

                # Avantages
                spe = f"""<b>{translate("beastform adv", lang)}:</b>  {opt["advantage"]}"""
                pg_spe = Paragraph(spe, common.styles["CardText"])
                story.append(pg_spe)

                # Descriptions Capacités de Forme Animale
                for j, capa in enumerate(opt["feats"]):
                    capacite = markdown2.markdown(f"""<b>{capa["name"]}</b>&nbsp;:&nbsp;{capa["text"].replace("\n", "<br/>")}""")
                    pg_capa = Paragraph(capacite, common.styles["CardText"])
                    story.append(pg_capa)

                # Infos secondaires : Type de carte
                infoSecondaires = f"""{translate("beastform sub", lang)}"""
                pg_sub = Paragraph(infoSecondaires, common.styles["CardSub"])
                story.append(pg_sub)
                
                # Passe à la carte suivante
                story.append(FrameBreak())  




def exe_unitaire(rang, lang):

    # Création du document
    doc = BaseDocTemplate(f"pdf/class_druid_beastform_{lang}_{rang}.pdf", pagesize=A4)

    doc.addPageTemplates(common.creer_template(lang))

    # Construction du contenu
    story = []

    # Première page
    titre_ppage = translate("ppage titre beastform" ,lang)
    sstitre_ppage = f"""{translate("ppage sstitre rang" ,lang)} 1-{rang}"""
    sstitre_ppage += f"""<br/>
    {translate("ppage sstitre langue", lang)} {lang} {translate("ppage sstitre trad", lang)}"""

    version_ppage = f"""{translate("ppage sstitre version", lang)} {common.VERSION_FMB}"""

    firstPage.ajouter_ppage_legale(story, lang, titre_ppage, sstitre_ppage, "", version_ppage)

    story.append(NextPageTemplate('grid'))
    story.append(PageBreak())

    # Pages suivantes : cartes
    ajouter_cartes(story, rang, lang) 

    # Génération du PDF
    doc.build(story)
