from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Frame, PageTemplate, Paragraph, PageBreak, NextPageTemplate, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm

from common import page_height, page_width, VERSION_APP
from translator import translate


style_ptitre = ParagraphStyle(name="FPagePreTitle", fontSize=36, leading=38, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=4)
style_titre = ParagraphStyle(name="FPageTitle", fontSize=26, leading=24, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=4)
style_sstitre = ParagraphStyle(name="FPageSubTitle", fontSize=12, leading=14, alignment=1, textColor=colors.black, fontName="Helvetica", spaceAfter=4)
style_sommaire = ParagraphStyle(name="FPageEntries", fontSize=12, leading=14, alignment=0, textColor=colors.black, fontName="Helvetica", spaceAfter=4)
style_version = ParagraphStyle(name="FPageVersion", fontSize=10, leading=11, alignment=2, textColor=colors.black, fontName="Helvetica", spaceAfter=2)
style_subversion = ParagraphStyle(name="FPageSubVersion", fontSize=10, leading=11, alignment=2, textColor=colors.white, fontName="Helvetica", spaceAfter=2)
style_legal = ParagraphStyle(name="FPageLegal", fontSize=12, leading=13, alignment=4, textColor=colors.black, fontName="Helvetica", spaceAfter=4)


#ppage_template = PageTemplate(id="title", frames=[cadre_ppage])

def getFPageParagraph(titre):

    title_text = titre

    return Paragraph(title_text, style_titre)

def ajouter_ppage_legale(story, lang, titre, sstitre, sommaire, version):

    # Versions
    story.append(Paragraph(version, style_version))
    story.append(Paragraph(VERSION_APP, style_subversion))


    # Pré-Titre
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("DAGGERHEART", style_ptitre))

    # Titre
    story.append(Paragraph(titre, style_titre))
    story.append(Spacer(1, 0.25*cm))

    # Sous Titre
    sous_titre=sstitre
    story.append(Paragraph(sous_titre, style_sstitre))
    story.append(Spacer(1, 0.25*cm))

    story.append(Paragraph(f"""{translate("ppage sstitre process", lang)}""", style_sstitre))
    story.append(Paragraph("https://mydhblog.com/naissance-des-cartes/", style_sstitre))                    
    story.append(Spacer(1, 0.5*cm))

    # Logo du blog
    logo_mydhblog = Image("Images/LogoBlogAtlante_Trp.png", width=3*cm, height=3*cm)
    logo_mydhblog.hAlign = 'CENTER'
    story.append(logo_mydhblog)
    story.append(Paragraph(f"""{translate("ppage sstitre materiel blog", lang)} >> https://myDHblog.com << <br/> {translate("ppage sstitre materiel patreon", lang)} >> https://www.patreon.com/cw/DarkCastor <<""", style_sstitre))
    story.append(Spacer(1, 1*cm))

    # Contenu du pack
    story.append(Paragraph(sommaire, style_sommaire))
    story.append(Spacer(1, 1*cm))



    dh_compat = Image("Images/DH_CGL_logos_final_full_color.png", width=9.0*cm, height=2.19*cm)
    dh_compat.hAlign = 'RIGHT'
 
    story.append(dh_compat)
    story.append(Spacer(1, 0.5*cm))

    # Mentions légales
    txt_copyright = f"""{translate("ppage copyright", lang)}"""
    story.append(Paragraph(txt_copyright, style_legal))
    txt_copyright_bbe = f"""{translate("ppage copyright bbe", lang)}"""
    story.append(Paragraph(txt_copyright_bbe, style_legal))
    txt_logo = f"{translate("ppage logo", lang)}"
    story.append(Paragraph(txt_logo, style_legal))

    return story

def ajouter_ppage_secondaire(story, titre):
    # Pré-Titre
    story.append(Spacer(1, 3*cm))
    # Titre
    story.append(Paragraph(titre, style_titre))

    return story


