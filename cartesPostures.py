
import json
import markdown2

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Frame, PageTemplate, Table, TableStyle
from reportlab.platypus import BaseDocTemplate, FrameBreak, PageBreak, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.lib.units import cm

import common
from translator import translate
import firstPage

def get_rangs_a_imprimer(tier):
    # Détermination des niveaux à imprimer en fonction du rang
    liste_rang = []
    if "1" in tier:
        liste_rang.append("1")
        print("POSTURES : Paliers : ", liste_rang)
    if "2" in tier:
        liste_rang.extend(["1","2"])
        print("POSTURES : Paliers : ", liste_rang)
    if "3" in tier:
        liste_rang.extend(["1","2","3"])
        print("POSTURES : Paliers : ", liste_rang)
    if "4" in tier or "Tous" in tier:
        liste_rang.extend(["1","2","3","4"])
        print("POSTURES : Paliers : ", liste_rang)
    return liste_rang

def ajouter_cartes(story, rang, lang):
    
    # Charger le JSON
    with open(common.DIR_JSON + f"{lang}/classes_brawler_stance_{lang}.json", "r", encoding="utf-8") as f:
        cartes = json.load(f)

    # Ajout des cartes dans la story
    for i, fichier in enumerate(cartes):

        # Livre de règle
        id_ruleb = f"""{fichier["rulebook"].upper()}"""
        #print("LIVRE DE REGLE : ", id_ruleb)

        # Nom Cartes de règles
        for k, regle in enumerate(fichier["rules"]):

            titre = f"""{translate("stance tit", lang).upper()}"""

            pg_titre = [[Paragraph(titre, common.styles["CardTitle"])]]
            tbl_capa = Table(pg_titre)
            tbl_capa.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),['HORIZONTAL', common.domain_bg_colors.get("Valor", colors.white),common.domain_bg_colors.get("Bone", colors.white)]),
                                                ]))
            story.append(tbl_capa)

            # Sous-Type de carte : Description
            crt_tp=f"""{regle["name"]}"""
            pg_type = Paragraph(crt_tp, common.styles["CardSubTitle"])
            story.append(pg_type)
            
            # Texte Description
            desc = markdown2.markdown(f"""{regle["text"].replace("\n", "<br/>")}""")
            pg_desc = Paragraph(desc, common.styles["CardText"])
            story.append(pg_desc)

            # Infos secondaires : Type de carte
            infoSecondaires = f"""{translate("stances sub", lang)}"""
            pg_sub = Paragraph(infoSecondaires, common.styles["CardSub"])
            story.append(pg_sub)

            # Passe à la carte suivante
            story.append(FrameBreak())  

def ajouter_mini_cartes(story, rang, lang):
    # Charger le JSON
    with open(common.DIR_JSON + f"{lang}/classes_brawler_stance_{lang}.json", "r", encoding="utf-8") as f:
        cartes = json.load(f)

    # STANCES
    rangs_a_imprimer = get_rangs_a_imprimer(rang)

    for i, carte in enumerate(cartes):
        for j, stn in enumerate(carte["stances"]):

            if stn["tier"] in rangs_a_imprimer:
                # Nom Carte
                titre = f"""{stn["tier"]} - {stn["name"].upper()}"""

                pg_titre = [[Paragraph(titre, common.styles["MiniCardTitle"])]]
                tbl_capa = Table(pg_titre)
                tbl_capa.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),['HORIZONTAL', common.domain_bg_colors.get("Valor", colors.white),common.domain_bg_colors.get("Bone", colors.white)]),
                                                ]))
                story.append(tbl_capa)
                
                story.append(Spacer(1, 0.5*cm))


                # Descriptions des Postures
                capacite = markdown2.markdown(f"""{stn["text"].replace("\n", "<br/>")}""")
                pg_capa = Paragraph(capacite, common.styles["MiniCardText"])
                story.append(pg_capa)

                # Infos secondaires : Type de carte
                infoSecondaires = f"""{translate("stance sub", lang)}"""
                pg_sub = Paragraph(infoSecondaires, common.styles["MiniCardSub"])
                story.append(pg_sub)
                
                # Passe à la carte suivante
                story.append(FrameBreak())  




def exe_unitaire(rang, lang):

    fichier_pdf=f"pdf/class_brawler_stances_{rang}_{lang}_{common.FORMAT_PAGE_STR}_{common.VERSION_STA}.pdf"

    # Création du document
    doc = BaseDocTemplate(fichier_pdf, pagesize=common.FORMAT_PAGE)

    doc.addPageTemplates(common.creer_template_postures(lang))

    # Construction du contenu
    story = []

    # Première page
    titre_ppage = translate("ppage titre stances" ,lang)
    #sstitre_ppage = f"""{translate("ppage sstitre rang" ,lang)} 1-{rang}"""
    sstitre_ppage = f"""<br/>
    {translate("ppage sstitre langue", lang)} {lang} {translate("ppage sstitre trad", lang)}"""

    version_ppage = f"""{translate("ppage sstitre version", lang)} {common.VERSION_STA}"""

    firstPage.ajouter_ppage_legale(story, lang, titre_ppage, sstitre_ppage, "", version_ppage)

    story.append(NextPageTemplate('grid'))
    story.append(PageBreak())

    # Deuxième page : Cartes de Règles
    ajouter_cartes(story, rang, lang)

    story.append(NextPageTemplate('minigrid'))
    story.append(PageBreak())
   
    # Pages suivantes : cartes de posture
    ajouter_mini_cartes(story, rang, lang)

    # Génération du PDF
    doc.build(story)
