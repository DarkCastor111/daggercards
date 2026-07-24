import cartesOrigines, cartesSousClasses, cartesDomaines, cartesClasses, cartesFormeBestiale


i18n="EN"
tier="Tous"

# python unitaire.py

cartesFormeBestiale.exe_unitaire(tier, i18n)

cartesOrigines.exe_unitaire("origine", i18n)
cartesOrigines.exe_unitaire("ascendance", i18n)
cartesClasses.exe_unitaire("Tous", i18n)
cartesSousClasses.exe_unitaire(tier, "Tous", i18n)
cartesDomaines.exe_unitaire(tier, "ToutesClasses", i18n)

