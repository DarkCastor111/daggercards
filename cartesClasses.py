
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
with open(common.DIR_JSON + f"{common.langage}/classes_{common.langage}.json", "r", encoding="utf-8") as f:
    cartes = json.load(f)

# Création du document
doc = BaseDocTemplate(f"pdf/classes_{common.langage}.pdf", pagesize=A4)

# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CardDomain", fontSize=12, leading=18, alignment=0, textColor=colors.black, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CardTitle", fontSize=10, leading=12, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=8))
styles.add(ParagraphStyle(name="CardSub", fontSize=9, leading=8, alignment=2, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=4))
styles.add(ParagraphStyle(name="CardText", fontSize=8, leading=9, alignment=4, fontName="Helvetica", spaceAfter=4))
styles.add(ParagraphStyle(name="CardFooter", fontSize=7, leading=8, alignment=0, textColor=colors.grey, fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle(name="CardType", fontSize=10, leading=11, alignment=1, textColor=colors.black, fontName="Helvetica-Oblique", spaceAfter=4, spaceBefore=4))

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
titre_ppage = translate("ppage titre classe" ,common.langage)
sstitre_ppage = "Sous-titre des cartes classe"
firstPage.ajouter_ppage(story, titre_ppage, sstitre_ppage)
# Pages suivantes
"""
# Créer les cadres (3x3 par page)
frames = []
for row in range(rows):
    for col in range(cols):
        # x = col * card_width
        # y = page_height - (row + 1) * card_height
        x = 1*cm + col * (card_width + 0.2*cm)
        y = page_height - (1*cm + (row + 1) * (card_height + 0.3*cm))
        frames.append(
            Frame(
                x, y,
                card_width, card_height,
                showBoundary=1  # Affiche le contour de la carte
            )
        )




def draw_card_background(canvas, doc):
    for row in range(rows):
        for col in range(cols):
            x = 1*cm + col * card_width
            y = page_height - (1*cm + (row + 1) * card_height
            )
            # Draw image at the top-left of each card, size 2x2 cm
            canvas.drawImage(
                bg_image,
                x + 0.2*cm, y + card_height - 2.3*cm,  # top-left inside card
                2*cm, 2*cm,
                preserveAspectRatio=True,
                mask='auto'
            )
"""



# Gabarit avec 9 cadres
# Image de fond
#    bg_path = "Images/Domain" + domaine + "40.png"
#    bg_image = ImageReader(bg_path)
#    template = PageTemplate(id="grid", frames=frames, onPage=draw_card_background)


"""
template = PageTemplate(id="grid", frames=frames, onPage=add_footer)
doc.addPageTemplates([template])

# Construction du contenu
story = []
"""


for i, carte in enumerate(cartes):
    # Récupération des informations
    #carte_classe = carte['class']
    #carte_sousclasse = carte['name']
    #carte_desc = carte['description']


    # Classe
    card_titre_style = ParagraphStyle(
        name="CardDomain_" + carte["name"],
        parent=styles["CardDomain"],
        #backColor=titre_bg_colors.get(carte["class"], colors.white),
        textColor=colors.snow
    )


    titre = f"""
    {carte["name"].upper()}
    """
    #pg_domain = Paragraph(titre, card_domain_style)
    pg_titre = [[Paragraph(titre, card_titre_style)]]
    tbl_domain = Table(pg_titre)
    tbl_domain.setStyle(TableStyle([('BACKGROUND',(0,0),(0,0),['HORIZONTAL', common.domain_bg_colors.get(carte["domain_1"], colors.white),common.domain_bg_colors.get(carte["domain_2"], colors.white)]),
                                    ]))
    story.append(tbl_domain)

    # Domaines
    crt_tp=f"{carte["domain_1"]} - {carte["domain_2"]}"
    pg_type = Paragraph(crt_tp, styles["CardType"])
    story.append(pg_type)
    
    # Description
    resume = common.premieres_phrases(carte["description"], 2)
    pg_desc = Paragraph(resume, styles["CardText"])
    story.append(pg_desc)

    # Informations additionnelles
    spe = f"""Spécialisations :  {carte["subclass_1"]}, {carte["subclass_2"]}"""
    pg_spe = Paragraph(spe, styles["CardSub"])
    story.append(pg_spe)

    # Passe à la carte suivante
    story.append(FrameBreak())  

    # Classe
    story.append(tbl_domain)

    # Sous-Type de carte : Capacité d'Espoir
    crt_tp="Capacité d'Espoir"
    pg_type = Paragraph(crt_tp, styles["CardType"])
    story.append(pg_type)

    # Capacité d'Espoir
    hope = markdown2.markdown(f"""<b>{carte["hope_feat_name"]}</b>&nbsp;:&nbsp;{carte["hope_feat_text"]}""")
    pg_hope = Paragraph(hope, styles["CardText"])
    story.append(pg_hope)

    # Passe à la carte suivante
    story.append(FrameBreak())  

    # Classe
    story.append(tbl_domain)

    # Sous-Type de carte : Capacités de classe
    crt_tp="Capacités de classe"
    pg_type = Paragraph(crt_tp, styles["CardType"])
    story.append(pg_type)

    # Capacités de classe
    for j, capa in enumerate(carte["class_feats"]):
        capacite = markdown2.markdown(f"""<b>{capa["name"]}</b>&nbsp;:&nbsp;{capa["text"]}""")
        pg_capa = Paragraph(capacite, styles["CardText"])
        story.append(pg_capa)

    # Passe à la carte suivante
    story.append(FrameBreak())  

# Génération du PDF
doc.build(story)
