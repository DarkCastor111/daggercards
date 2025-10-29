from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Frame
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import re
import os



langage = "FR"
#langage = "EN"
#langage = "FR"
#langage = "ES"

# Directory containing JSON resources. Prefer environment variable `DIR_JSON`.
# If not set, fall back to the project's original default path.
_default_dir_json = r"json/"
DIR_JSON = os.environ.get('DIR_JSON', _default_dir_json)
# Normalize to OS path and ensure it ends with a separator when used to join filenames
DIR_JSON = os.path.normpath(DIR_JSON) + os.path.sep

# Paramètres
#############################
# Dimensions page et cartes
page_width, page_height = A4
cols, rows = 3, 3
#card_width = page_width / cols
card_width = 6.35*cm
#card_width = 6.2*cm
#card_height = page_height / rows
card_height = 8.8*cm
#card_height = 8.7*cm

# Couleurs
#############################
domain_bg_colors = {
    "Arcana": colors.indigo,
    "Bone": colors.dimgray,
    "Blade": colors.firebrick,
    "Codex": colors.navy,
    "Grace": colors.mediumvioletred,
    "Midnight": colors.darkslategray,
    "Sage": colors.darkgreen,
    "Splendor": colors.goldenrod,
    "Valor": colors.darkorange,
}

domain_txt_colors = {
    "Arcana": colors.snow,
    "Bone": colors.snow,
    "Blade": colors.snow,
    "Codex": colors.snow,
    "Grace": colors.snow,
    "Midnight": colors.snow,
    "Sage": colors.snow,
    "Splendor": colors.snow,
    "Valor": colors.snow,
}

# Styles
#############################
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CardTitle", fontSize=11, leading=18, alignment=0, textColor=colors.snow, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CardSubTitle", fontSize=10, leading=11, alignment=1, textColor=colors.black, fontName="Helvetica-Oblique", spaceAfter=4, spaceBefore=4))
styles.add(ParagraphStyle(name="CardName", fontSize=10, leading=12, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceBefore=4, spaceAfter=4))
styles.add(ParagraphStyle(name="CardPres", fontSize=8, leading=9, alignment=4, textColor=colors.black, fontName="Helvetica-Oblique", spaceAfter=4))
styles.add(ParagraphStyle(name="CardText", fontSize=8, leading=9, alignment=4, fontName="Helvetica", spaceAfter=4))
styles.add(ParagraphStyle(name="CardFooter", fontSize=7, leading=8, alignment=0, textColor=colors.grey, fontName="Helvetica-Oblique"))
styles.add(ParagraphStyle(name="CardSub", fontSize=9, leading=10, alignment=2, textColor=colors.black, fontName="Helvetica-Bold"))

# Cadre des cartes (3x3 par page)
cards_frames = []
for row in range(rows):
    for col in range(cols):
        # x = col * card_width
        # y = page_height - (row + 1) * card_height
        x = 1*cm + col * (card_width + 0*cm)
        y = page_height - (1*cm + (row + 1) * (card_height + 0*cm))
        cards_frames.append(
            Frame(
                x, y,
                card_width, card_height,
                showBoundary=1  # Affiche le contour de la carte
            )
        )

def premieres_phrases(text, nb_phrases):
    matches = re.findall(r'[^.?!]*[.?!]', text)
    if matches:
        return ''.join(matches[:nb_phrases]).strip()
    else:
        return text.strip()  # fallback: return the whole text if no sentence end found
    

    


