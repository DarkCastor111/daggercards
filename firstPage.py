from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Frame, PageTemplate, Paragraph, PageBreak, NextPageTemplate, Image, Spacer
from reportlab.lib import colors
from reportlab.lib.units import cm

from common import page_height, page_width
from translator import translate


style_ptitre = ParagraphStyle(name="FPagePreTitle", fontSize=36, leading=38, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=4)
style_titre = ParagraphStyle(name="FPageTitle", fontSize=26, leading=24, alignment=1, textColor=colors.black, fontName="Helvetica-Bold", spaceAfter=4)
style_sstitre = ParagraphStyle(name="FPageSubTitle", fontSize=12, leading=14, alignment=1, textColor=colors.black, fontName="Helvetica", spaceAfter=4)
style_legal = ParagraphStyle(name="FPageLegal", fontSize=12, leading=13, alignment=4, textColor=colors.black, fontName="Helvetica", spaceAfter=4)


cadre_ppage = Frame(
    1*cm, 1*cm,
    page_width - 2*cm, page_height - 2*cm,
    showBoundary=0
)

ppage_template = PageTemplate(id="title", frames=[cadre_ppage])

def getFPageParagraph(titre):

    title_text = titre
    # use a Spacer to center vertically: split usable height in half
    """
    usable_height = page_height - 2*cm
    spacer_height = usable_height / 2.0 - (style_titre.fontSize * 0.6)  # approximate centering
    if spacer_height < 0:
        spacer_height = 0
    """

    return Paragraph(title_text, style_titre)

def ajouter_ppage_legale(story, titre, sstitre):

    # Pré-Titre
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("DAGGERHEART", style_ptitre))

    # Titre
    story.append(Paragraph(titre, style_titre))

    logo_mydhblog = Image("Images/LogoBlogAtlante_Trp.png", width=4*cm, height=4*cm)
    logo_mydhblog.hAlign = 'CENTER'
    story.append(Spacer(1, 0.5*cm))

    # Sous Titre
    sous_titre=sstitre
    story.append(Paragraph(sous_titre, style_sstitre))
    story.append(Spacer(1, 1.5*cm))

    # Logo du blog
    story.append(logo_mydhblog)
    story.append(Spacer(1, 6*cm))


    dh_compat = Image("Images/DH_CGL_logos_final_full_color.png", width=9.0*cm, height=2.19*cm)
    dh_compat.hAlign = 'RIGHT'
 
    story.append(dh_compat)
    story.append(Spacer(1, 0.5*cm))


    txt_copyright = f"""{translate("fp copyright", "EN")}"""
    story.append(Paragraph(txt_copyright, style_legal))
    txt_logo = f"{translate("fp logo", "EN")}"
    story.append(Paragraph(txt_logo, style_legal))

    return story

def ajouter_ppage_secondaire(story, titre):
    # Pré-Titre
    story.append(Spacer(1, 3*cm))
    # Titre
    story.append(Paragraph(titre, style_titre))

    return story


