import cartesOrigines, cartesSousClasses, cartesDomaines, cartesClasses


i18n="FR"
tier="1"

"""
"""
cartesOrigines.exe_unitaire("origine", i18n)
cartesOrigines.exe_unitaire("ascendance", i18n)
cartesClasses.exe_unitaire("TOUTES", i18n)
cartesSousClasses.exe_unitaire(tier, i18n)
cartesDomaines.exe_unitaire(tier, "TOUS", i18n)