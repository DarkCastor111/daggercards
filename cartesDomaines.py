
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

# Charger le JSON
with open(common.DIR_JSON + f"{common.langage}/abilities_{common.langage}.json", "r", encoding="utf-8") as f:
    cartes = json.load(f)

# Création du document
doc = BaseDocTemplate(f"pdf/abilities_{common.langage}.pdf", pagesize=A4)



domaines_a_imprimer = ["Arcana","Blade","Bone","Codex","Grace","Midnight","Sage","Splendor","Valor"]
#domaines_a_imprimer = ["Arcana","Bone","Blade"]

rang = 1
if rang == 1:
    niveaux_a_imprimer = ["1"]
elif rang == 2:
    niveaux_a_imprimer = ["1","2","3","4"]
elif rang == 3:
    niveaux_a_imprimer = ["1","2","3","4","5","6","7"]
else:
    niveaux_a_imprimer = ["1","2","3","4","5","6","7","8","9","10"]



# Styles
"""
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CardType", fontSize=11, leading=18, alignment=0, textColor=colors.black, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CardTitle", fontSize=10, leading=12, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceBefore=4, spaceAfter=4))
styles.add(ParagraphStyle(name="CardSub", fontSize=9, leading=8, alignment=2, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=4))
styles.add(ParagraphStyle(name="CardText", fontSize=8, leading=9, alignment=4, fontName="Helvetica", spaceAfter=4))
styles.add(ParagraphStyle(name="CardFooter", fontSize=7, leading=8, alignment=0, textColor=colors.grey, fontName="Helvetica-Oblique"))
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
titre_ppage = translate("ppage titre domaine", common.langage)
sstitre_ppage = f"""{translate("ppage sstitre rang", common.langage)} {rang}<br/>
{translate("ppage sstitre langue", common.langage)} {common.langage}
"""
firstPage.ajouter_ppage(story, titre_ppage, sstitre_ppage)

# Pages suivantes
for domaine in domaines_a_imprimer:

    for i, carte in enumerate(cartes):
        niveau_carte = carte['level']
        domaine_carte = carte['domain']
        if niveau_carte in niveaux_a_imprimer and domaine_carte == domaine :
            """
            # Dynamically create a style with the background color for this domain
            card_domain_style = ParagraphStyle(
                name="CardTitle_" + domaine_carte,
                parent=common.styles["CardTitle"],
                #backColor=domain_bg_colors.get(domaine_carte, colors.white),
                textColor=common.domain_txt_colors.get(domaine_carte, colors.black)
            )
            """

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

# Génération du PDF
doc.build(story)
