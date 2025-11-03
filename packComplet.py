import sys

from reportlab.platypus import BaseDocTemplate, PageBreak, NextPageTemplate
from reportlab.lib.pagesizes import A4

import common
import translator
import firstPage
import cartesOrigines, cartesSousClasses, cartesDomaines # cartesClasses 

print("Nom du script :", sys.argv[0])

PARAM_LANG = "EN"
PARAM_RANG = "1"
PARAM_CLASSE = "TOUS"


if len(sys.argv) > 1:
    print("Premier paramètre : PARAM_LANG = ", sys.argv[1])
    PARAM_LANG = sys.argv[1]
    #common.langage = PARAM_LANG
    #print("common.langage = ", common.langage)
if len(sys.argv) > 2:
    print("Deuxième paramètre : PARAM_RANG = ", sys.argv[2])
    PARAM_RANG = sys.argv[2]
if len(sys.argv) > 3:
    print("Deuxième paramètre : PARAM_CLASSE = ", sys.argv[3])
    PARAM_CLASSE = sys.argv[3]

fichier_pdf = f"pdf/packComplet_{PARAM_LANG}_{PARAM_RANG}.pdf"

# Création du document
doc = BaseDocTemplate(fichier_pdf, pagesize=A4)

doc.addPageTemplates(common.creer_template(PARAM_LANG))

# Construction du contenu
story = []

# Première page
titre_ppage = translator.translate("ppage pack complet", PARAM_LANG)
sstitre_ppage = f"""{translator.translate("ppage sstitre langue", PARAM_LANG)} {PARAM_LANG} {translator.translate("ppage sstitre trad", PARAM_LANG)}<br/> 
{translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG}
"""

sommaire_ppage = f"""
- {translator.translate("ppage titre ascendance", PARAM_LANG).capitalize()} <br/>
- {translator.translate("ppage titre origine", PARAM_LANG).capitalize()} <br/>
- {translator.translate("ppage titre classe", PARAM_LANG).capitalize()} <br/>
- {translator.translate("ppage titre sous classe", PARAM_LANG).capitalize()} {translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG}<br/>
- {translator.translate("ppage titre domaine", PARAM_LANG).capitalize()} {translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG}<br/>
"""

firstPage.ajouter_ppage_legale(story, titre_ppage, sstitre_ppage, sommaire_ppage)

# Pages suivantes : cartes origines

story.append(NextPageTemplate('grid'))
story.append(PageBreak())
cartesOrigines.ajouter_cartes(story, "origine", PARAM_LANG)

# Pages suivantes : cartes ascendances
cartesOrigines.ajouter_cartes(story, "ascendance", PARAM_LANG)

# Pages suivantes : cartes classes
# cartesClasses.

# Pages suivantes : cartes sous classes
cartesSousClasses.ajouter_cartes(story, PARAM_RANG, PARAM_LANG)

# Pages suivantes : cartes domaines
cartesDomaines.ajouter_cartes(story, PARAM_RANG, PARAM_CLASSE, PARAM_LANG)


# Génération du PDF
doc.build(story)
