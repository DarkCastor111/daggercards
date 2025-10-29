
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

rang = 4
if rang == 1:
    specialisations_a_imprimer = ["foundations"]
elif rang == 2:
    specialisations_a_imprimer = ["foundations"]
elif rang == 3:
    specialisations_a_imprimer = ["foundations", "specializations"]
else:
    specialisations_a_imprimer = ["foundations", "specializations", "masteries"]


# Charger le JSON
with open(common.DIR_JSON + f"{common.langage}/subclasses_{common.langage}.json", "r", encoding="utf-8") as f:
    cartes = json.load(f)

# Création du document
doc = BaseDocTemplate(f"pdf/subclasses_{common.langage}.pdf", pagesize=A4)

# Styles
"""
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CardDomain", fontSize=11, leading=18, alignment=0, textColor=colors.black, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CardTitle", fontSize=10, leading=12, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=8))
styles.add(ParagraphStyle(name="CardSub", fontSize=9, leading=10, alignment=2, textColor=colors.black, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CardText", fontSize=8, leading=9, alignment=4, fontName="Helvetica", spaceAfter=4))
styles.add(ParagraphStyle(name="CardFooter", fontSize=7, leading=8, alignment=0, textColor=colors.grey, fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle(name="CardSubTitle", fontSize=10, leading=11, alignment=1, textColor=colors.black, fontName="Helvetica-Oblique", spaceAfter=4, spaceBefore=4))
"""


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
titre_ppage = translate("ppage titre sous classe" ,common.langage)
sstitre_ppage = f"""{translate("ppage sstitre rang" ,common.langage)} {rang} - """
for spe in specialisations_a_imprimer:
    spe_traduite = f"{translate(spe, common.langage)} "
    sstitre_ppage += spe_traduite
sstitre_ppage += f"""<br/>
{translate("ppage sstitre langue", common.langage)} {common.langage}"""

firstPage.ajouter_ppage(story, titre_ppage, sstitre_ppage)

# Pages suivantes
for i, carte in enumerate(cartes):

    for carte_type in specialisations_a_imprimer:

        # Nom Specialisation
        """
        card_titre_style = ParagraphStyle(
            name="CardTitre_" + carte["class"],
            parent=common.styles["CardTitle"],
            textColor=colors.snow
        )
        """

        titre = f"""
        {carte["name"].upper()}
        """
        #pg_domain = Paragraph(titre, card_domain_style)
        pg_titre = [[Paragraph(titre, common.styles["CardTitle"])]]
        tbl_domain = Table(pg_titre)
        tbl_domain.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),['HORIZONTAL', common.domain_bg_colors.get(carte["domain_1"], colors.white),common.domain_bg_colors.get(carte["domain_2"], colors.white)]),
                                        ]))

        story.append(tbl_domain)

        # Type de Carte
        crt_tp=f"{translate(carte_type, common.langage)}"
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
        spe = f"""{translate('sous classe de',common.langage)} {carte["class"].upper()}"""
        pg_spe = Paragraph(spe, common.styles["CardSub"])
        story.append(pg_spe)

        if carte_type == "foundations" and carte.get("spellcast_trait") :
            inc = f"""{translate('trait incantation',common.langage)} {carte["spellcast_trait"]}"""
            pg_inc = Paragraph(inc, common.styles["CardSub"])
            story.append(pg_inc)

        # Passe à la carte suivante
        story.append(FrameBreak())  

# Génération du PDF
doc.build(story)
