import sys

from reportlab.platypus import BaseDocTemplate, PageBreak, NextPageTemplate
from reportlab.lib.pagesizes import A4

import common
import translator
import firstPage
import cartesOrigines, cartesSousClasses, cartesDomaines, cartesClasses 


print("Nom du script :", sys.argv[0])
### Packs de démarrage
# python packDemarrage.py FR


PARAM_LANG = "FR"
PARAM_RANG = "1"
PARAM_RANG_STR = "1"
PARAM_CLASSE = "Tous"
PARAM_CLASSE_STR = "Starter"
PARAM_CLASSE_STR_COURT = "Starter"


if len(sys.argv) > 1:
    print("Premier paramètre : PARAM_LANG = ", sys.argv[1])
    PARAM_LANG = sys.argv[1]
    #common.langage = PARAM_LANG
    #print("common.langage = ", common.langage)


fichier_pdf = f"pdf/Pack_{PARAM_CLASSE_STR_COURT}_{PARAM_LANG}_{common.VERSION_STP}.pdf"

# Création du document
doc = BaseDocTemplate(fichier_pdf, pagesize=A4)

doc.addPageTemplates(common.creer_template(PARAM_LANG))

# Construction du contenu
story = []

# Première page
titre_ppage = f"""{PARAM_CLASSE_STR.upper()} {translator.translate("ppage pack", PARAM_LANG)}"""
sstitre_ppage = f"""{translator.translate("ppage sstitre langue", PARAM_LANG)} {PARAM_LANG} {translator.translate("ppage sstitre trad", PARAM_LANG)}<br/> 
{translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG_STR}
"""

liste_domaines = common.get_domaines_a_imprimer(PARAM_CLASSE)

sommaire_ppage = f"""
- 9 {translator.translate("ppage titre origine", PARAM_LANG).capitalize()} <br/>
- 18 {translator.translate("ppage titre ascendance", PARAM_LANG).capitalize()} <br/>
- 27 {translator.translate("ppage titre classe", PARAM_LANG).capitalize()} <br/>
- 18 {translator.translate("ppage titre sous classe", PARAM_LANG).capitalize()} - {translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG_STR}<br/>
- 27 {translator.translate("ppage titre domaine", PARAM_LANG).capitalize()} - {translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG_STR}<br/>
"""
version_ppage = f"""<br/>
    {translator.translate("ppage sstitre version", PARAM_LANG)} {common.VERSION_STP}"""

firstPage.ajouter_ppage_legale(story, PARAM_LANG, titre_ppage, sstitre_ppage, sommaire_ppage, version_ppage)

# Pages suivantes : cartes origines

story.append(NextPageTemplate('grid'))
story.append(PageBreak())
cartesOrigines.ajouter_cartes(story, "origine", PARAM_LANG)

# Pages suivantes : cartes ascendances
cartesOrigines.ajouter_cartes(story, "ascendance", PARAM_LANG)

# Pages suivantes : cartes classes
cartesClasses.ajouter_cartes(story, PARAM_CLASSE, PARAM_LANG)

# Pages suivantes : cartes sous classes
cartesSousClasses.ajouter_cartes(story, PARAM_RANG, PARAM_CLASSE, PARAM_LANG)

# Pages suivantes : cartes domaines
cartesDomaines.ajouter_cartes(story, PARAM_RANG, PARAM_CLASSE, PARAM_LANG)


# Génération du PDF
doc.build(story)
