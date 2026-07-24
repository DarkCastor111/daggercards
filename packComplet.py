import sys

from reportlab.platypus import BaseDocTemplate, PageBreak, NextPageTemplate

import common
import translator
import firstPage
import cartesOrigines, cartesSousClasses, cartesDomaines, cartesClasses, cartesFormeBestiale


print("Nom du script :", sys.argv[0])
### Packs de classe
# python packComplet.py EN Tous warrior
# python packComplet.py EN Tous wizard
# python packComplet.py EN Tous rogue

### Packs de classe
# python packComplet.py EN Tous bard
# python packComplet.py EN Tous guardian
# python packComplet.py EN Tous ranger

### Packs de classe
# python packComplet.py EN Tous druid
# python packComplet.py EN Tous seraph
# python packComplet.py EN Tous sorcerer

PARAM_LANG = "FR"
PARAM_RANG = "Complet"
PARAM_RANG_STR = "Complet"
PARAM_CLASSE = "TOUS"
PARAM_CLASSE_STR = "TOUS"
PARAM_CLASSE_STR_COURT = "TOUS"


if len(sys.argv) > 1:
    print("Premier paramètre : PARAM_LANG = ", sys.argv[1])
    PARAM_LANG = sys.argv[1]
    #common.langage = PARAM_LANG
    #print("common.langage = ", common.langage)
if len(sys.argv) > 2:
    print("Deuxième paramètre : PARAM_RANG = ", sys.argv[2])
    PARAM_RANG = sys.argv[2]
    if PARAM_RANG == "Tous":
        PARAM_RANG_STR = "1-4"
    else:
        PARAM_RANG_STR = PARAM_RANG
if len(sys.argv) > 3:
    print("Deuxième paramètre : PARAM_CLASSE = ", sys.argv[3])
    # PARAM_CLASSE, Nom des classes dans les json, pour passage de paramètre
    PARAM_CLASSE = translator.translate("classe " + sys.argv[3], PARAM_LANG)

    # PARAM_CLASSE_STR et PARAM_CLASSE_STR_COURT, pour affichage
    if sys.argv[3] == "Tous":
        PARAM_CLASSE_STR = translator.translate("ppage pack complet", PARAM_LANG)
        PARAM_CLASSE_STR_COURT = translator.translate("ppage pack complet", PARAM_LANG)
    else:
        PARAM_CLASSE_STR = translator.translate("ppage pack " + sys.argv[3], PARAM_LANG)
        PARAM_CLASSE_STR_COURT = sys.argv[3].upper()


fichier_pdf = f"pdf/Pack_{PARAM_CLASSE_STR_COURT}_{PARAM_LANG}_{common.FORMAT_PAGE_STR}_{common.VERSION_PCK}.pdf"

# Création du document
doc = BaseDocTemplate(fichier_pdf, pagesize=common.FORMAT_PAGE)

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
- 3 {translator.translate("ppage titre classe", PARAM_LANG).capitalize()} <br/>
- 6 {translator.translate("ppage titre sous classe", PARAM_LANG).capitalize()} - {translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG_STR}<br/>
- 42 {translator.translate("ppage titre domaine", PARAM_LANG).capitalize()} {liste_domaines} - {translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG_STR}<br/>
"""
if PARAM_CLASSE in ['Druid', 'Druide']:
    sommaire_ppage += f"""- 25 {translator.translate("ppage titre beastform", PARAM_LANG).capitalize()} - {translator.translate("ppage sstitre rang", PARAM_LANG)} {PARAM_RANG_STR}"""

version_ppage = f"""<br/>
    {translator.translate("ppage sstitre version", PARAM_LANG)} {common.VERSION_PCK}"""

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

# Pages suivantes : si Druide, cartes formes bestiales
if PARAM_CLASSE in ['Druid', 'Druide']:
    cartesFormeBestiale.ajouter_cartes(story, PARAM_RANG, PARAM_LANG)


# Génération du PDF
doc.build(story)
