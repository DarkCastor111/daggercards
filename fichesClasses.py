import json
from reportlab.lib.pagesizes import A5
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Frame, NextPageTemplate, PageTemplate
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors

def generate_daggerheart_pdf(json_data_path, output_filename="daggerheart_classes.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=A5,
                            leftMargin=0.5*inch, rightMargin=0.5*inch,
                            topMargin=0.5*inch, bottomMargin=0.5*inch)

    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    styles.add(ParagraphStyle(name='ClassTitle', alignment=TA_CENTER, fontSize=18, fontName='Helvetica-Bold', textColor=colors.darkred, spaceAfter=0.1*inch))
    styles.add(ParagraphStyle(name='SectionTitle', alignment=TA_LEFT, fontSize=12, fontName='Helvetica-Bold', textColor=colors.darkblue, spaceBefore=0.1*inch, spaceAfter=0.05*inch))
    styles.add(ParagraphStyle(name='NormalText', alignment=TA_LEFT, fontSize=9, fontName='Helvetica', textColor=colors.black, leading=10, spaceAfter=0.05*inch))
    styles.add(ParagraphStyle(name='StatsText', alignment=TA_LEFT, fontSize=9, fontName='Helvetica-Bold', textColor=colors.darkgreen, leading=10, spaceAfter=0.05*inch))

    main_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='main_frame')
    doc.addPageTemplates([PageTemplate(id='ClassCard', frames=[main_frame])])

    try:
        with open(json_data_path, 'r', encoding='utf-8') as f:
            classes_data = json.load(f)
    except FileNotFoundError:
        print(f"Erreur : Le fichier JSON '{json_data_path}' n'a pas été trouvé.")
        return
    except json.JSONDecodeError:
        print(f"Erreur : Impossible de décoder le fichier JSON '{json_data_path}'. Vérifiez sa syntaxe.")
        return

    for class_data in classes_data:
        story.append(NextPageTemplate('ClassCard'))
        
        # Class Title
        class_name = class_data.get("name", "Nom de Classe Inconnu")
        story.append(Paragraph(class_name, styles['ClassTitle']))
        story.append(Spacer(1, 0.05 * inch))

        # Description
        story.append(Paragraph("Description :", styles['SectionTitle']))
        story.append(Paragraph(class_data.get("description", ""), styles['NormalText']))
        story.append(Spacer(1, 0.05 * inch))

        # Domaines
        domain_1 = class_data.get("domain_1", "N/A")
        domain_2 = class_data.get("domain_2", "N/A")
        story.append(Paragraph(f"Domaines : {domain_1}, {domain_2}", styles['NormalText']))
        story.append(Spacer(1, 0.05 * inch))

        # Sous-classes
        subclass_1 = class_data.get("subclass_1", "N/A")
        subclass_2 = class_data.get("subclass_2", "N/A")
        story.append(Paragraph("Archétypes :", styles['SectionTitle']))
        story.append(Paragraph(f"{subclass_1}, {subclass_2}", styles['NormalText']))
        story.append(Spacer(1, 0.05 * inch))

        # Statistiques Clés
        story.append(Paragraph("Statistiques Clés :", styles['SectionTitle']))
        story.append(Paragraph(f"Évasion : {class_data.get('evasion', '')}", styles['StatsText']))
        story.append(Paragraph(f"Points de Vie : {class_data.get('hp', '')}", styles['StatsText']))
        story.append(Spacer(1, 0.05 * inch))

        # Capacité d'Espoir
        hope_feat_name = class_data.get("hope_feat_name", "N/A")
        hope_feat_text = class_data.get("hope_feat_text", "")
        story.append(Paragraph(f"Capacité d'Espoir : {hope_feat_name}", styles['SectionTitle']))
        story.append(Paragraph(hope_feat_text, styles['NormalText']))
        story.append(Spacer(1, 0.05 * inch))

        # Capacités de Classe
        class_feats = class_data.get("class_feats", [])
        if class_feats:
            story.append(Paragraph("Capacités de Classe :", styles['SectionTitle']))
            for feat in class_feats:
                story.append(Paragraph(f"<b>{feat.get('name', '')}</b> : {feat.get('text', '')}", styles['NormalText']))
            story.append(Spacer(1, 0.05 * inch))

        # Équipement
        story.append(Paragraph("Objets de Départ :", styles['SectionTitle']))
        story.append(Paragraph(class_data.get("items", ""), styles['NormalText']))
        story.append(Spacer(1, 0.05 * inch))

        # Suggestions d'Équipement et d'Attributs
        story.append(Paragraph("Suggestions d'Équipement et d'Attributs :", styles['SectionTitle']))
        story.append(Paragraph(f"Traits suggérés : {class_data.get('suggested_traits', '')}", styles['NormalText']))
        story.append(Paragraph(f"Arme principale suggérée : {class_data.get('suggested_primary', '')}", styles['NormalText']))
        story.append(Paragraph(f"Arme secondaire suggérée : {class_data.get('suggested_secondary', '')}", styles['NormalText']))
        story.append(Paragraph(f"Armure suggérée : {class_data.get('suggested_armor', '')}", styles['NormalText']))
        story.append(Spacer(1, 0.05 * inch))

        # Questions d'Historique (Backgrounds)
        backgrounds = class_data.get("backgrounds", [])
        if backgrounds:
            story.append(Paragraph("Questions de Background :", styles['SectionTitle']))
            for bg_q in backgrounds:
                story.append(Paragraph(f"- {bg_q.get('question', '')}", styles['NormalText']))
            story.append(Spacer(1, 0.05 * inch))

        # Questions de Connexions
        connections = class_data.get("connections", [])
        if connections:
            story.append(Paragraph("Connexions avec les autres PJs :", styles['SectionTitle']))
            for conn_q in connections:
                story.append(Paragraph(f"- {conn_q.get('question', '')}", styles['NormalText']))
            story.append(Spacer(1, 0.05 * inch))

        story.append(PageBreak())

    try:
        doc.build(story)
        print(f"Le PDF '{output_filename}' a été généré avec succès.")
    except Exception as e:
        print(f"Une erreur est survenue lors de la génération du PDF : {e}")

if __name__ == '__main__':
    generate_daggerheart_pdf('daggerheart_classes.json')
