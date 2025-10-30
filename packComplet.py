import sys

from reportlab.platypus import BaseDocTemplate
from reportlab.lib.pagesizes import A4

import common
import translator
import firstPage
import cartesOrigines

print("Nom du script :", sys.argv[0])

PARAM_LANG = "EN"
PARAM_RANG = 1


if len(sys.argv) > 1:
    print("Premier paramètre : PARAM_LANG = ", sys.argv[1])
    PARAM_LANG = sys.argv[1]
    common.langage = PARAM_LANG
    print("common.langage = ", common.langage)
if len(sys.argv) > 2:
    print("Deuxième paramètre : PARAM_RANG = ", sys.argv[2])
    PARAM_RANG = sys.argv[2]
if len(sys.argv) > 3:
    print("Deuxième paramètre : PARAM_CLASSE = ", sys.argv[3])
    PARAM_CLASSE = sys.argv[3]

fichier_pdf = f"pdf/packComplet_{PARAM_LANG}_{PARAM_RANG}.pdf"

# Création du document
doc = BaseDocTemplate(fichier_pdf, pagesize=A4)

doc.addPageTemplates(common.creer_template())

# Construction du contenu
story = []

# Première page
titre_ppage = translator.translate("ppage pack complet", common.langage)
sstitre_ppage = f"""{translator.translate("ppage sstitre langue", common.langage)} {common.langage} {translator.translate("ppage sstitre rang", common.langage)} {PARAM_RANG}
"""
firstPage.ajouter_ppage(story, titre_ppage, sstitre_ppage)

# Pages suivantes : cartes origines
cartesOrigines.ajouter_cartes(story, "origine", PARAM_LANG)
# Pages suivantes : cartes ascendance
cartesOrigines.ajouter_cartes(story, "ascendance", PARAM_LANG)

# Génération du PDF
doc.build(story)
