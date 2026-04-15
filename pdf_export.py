# pdf_export.py
"""PDF report generation for blood test results."""

import io
from datetime import date
from pathlib import Path
from PIL import Image as PILImage

from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, Image,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Circle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit

# ── Paths ───────────────────────────────────────────────────────────────────
_HERE   = Path(__file__).parent
_STATIC = _HERE / "static"
_ASSETS = _HERE / "assets"

# ── Colours ─────────────────────────────────────────────────────────────────
ORANGE       = HexColor('#FF671D')
RED          = HexColor('#C52536')
RED_DIM      = HexColor('#FFF5F6')
GREEN        = HexColor('#1F8C47')
GREEN_DIM    = HexColor('#F4FBF6')
GREEN_BAR    = HexColor('#3DB866')
RED_BAR      = HexColor('#D93545')
BG_ELEVATED  = HexColor('#EEEEF1')
TEXT_PRIMARY = HexColor('#1A1B1E')
TEXT_SEC     = HexColor('#4A4B55')
TEXT_MUTED   = HexColor('#767783')
ROW_LINE     = HexColor('#E8E8EC')
WHITE        = white

# ── Font registration ────────────────────────────────────────────────────────
_FONTS_REGISTERED = False

def _register_fonts():
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    pdfmetrics.registerFont(TTFont('Poppins',        str(_STATIC / 'Poppins-Regular.ttf')))
    pdfmetrics.registerFont(TTFont('Poppins-Medium', str(_STATIC / 'Poppins-Medium.ttf')))
    pdfmetrics.registerFont(TTFont('Figtree',        str(_STATIC / 'Figtree-VariableFont_wght.ttf')))
    pdfmetrics.registerFont(TTFont('Figtree-Italic', str(_STATIC / 'Figtree-Italic-VariableFont_wght.ttf')))
    _FONTS_REGISTERED = True


# ── Styles ───────────────────────────────────────────────────────────────────
def _build_styles():
    return {
        'title': ParagraphStyle('title',
            fontName='Poppins-Medium', fontSize=20, leading=24,
            textColor=ORANGE, spaceAfter=2),
        'subtitle': ParagraphStyle('subtitle',
            fontName='Figtree', fontSize=10, leading=14,
            textColor=TEXT_SEC),
        'section_abn': ParagraphStyle('section_abn',
            fontName='Poppins-Medium', fontSize=9, leading=12,
            textColor=RED, spaceAfter=4, spaceBefore=4),
        'section_norm': ParagraphStyle('section_norm',
            fontName='Poppins-Medium', fontSize=9, leading=12,
            textColor=GREEN, spaceAfter=4, spaceBefore=4),
        'metric_name': ParagraphStyle('metric_name',
            fontName='Poppins-Medium', fontSize=12, leading=16,
            textColor=TEXT_PRIMARY, spaceAfter=6),
        'badge': ParagraphStyle('badge',
            fontName='Poppins-Medium', fontSize=8, leading=10,
            textColor=WHITE),
        'info_label': ParagraphStyle('info_label',
            fontName='Figtree', fontSize=8, leading=11,
            textColor=TEXT_MUTED),
        'info_value': ParagraphStyle('info_value',
            fontName='Poppins-Medium', fontSize=10, leading=13,
            textColor=TEXT_PRIMARY),
        'body': ParagraphStyle('body',
            fontName='Figtree', fontSize=9, leading=14,
            textColor=TEXT_SEC),
        'body_label': ParagraphStyle('body_label',
            fontName='Poppins-Medium', fontSize=9, leading=12,
            textColor=TEXT_PRIMARY, spaceAfter=2),
        'th': ParagraphStyle('th',
            fontName='Poppins-Medium', fontSize=8, leading=11,
            textColor=TEXT_MUTED, alignment=TA_CENTER),
        'td_name': ParagraphStyle('td_name',
            fontName='Figtree', fontSize=9, leading=12,
            textColor=TEXT_PRIMARY),
        'td_center': ParagraphStyle('td_center',
            fontName='Figtree', fontSize=9, leading=12,
            textColor=TEXT_PRIMARY, alignment=TA_CENTER),
        'td_status': ParagraphStyle('td_status',
            fontName='Poppins-Medium', fontSize=8, leading=11,
            textColor=GREEN, alignment=TA_CENTER),
        'summary_n': ParagraphStyle('summary_n',
            fontName='Poppins-Medium', fontSize=22, leading=26,
            textColor=WHITE),
        'summary_lbl': ParagraphStyle('summary_lbl',
            fontName='Figtree', fontSize=9, leading=12,
            textColor=WHITE),
        'disclaimer': ParagraphStyle('disclaimer',
            fontName='Figtree', fontSize=7.5, leading=11,
            textColor=TEXT_MUTED),
    }


# ── Helpers ──────────────────────────────────────────────────────────────────
def _get_range(data, sex):
    if data['gender_specific']:
        return (data['range'][0], data['range'][1]) if sex == 'Female' \
               else (data['range'][2], data['range'][3])
    return data['range'][0], data['range'][1]


def _range_str(data, sex):
    t    = data.get('type', 'hilo')
    unit = data.get('unit', '')
    if t == 'presence':
        return 'Not detected'
    low, high = _get_range(data, sex)
    if t == 'upper_bound':
        return f'< {high} {unit}'
    if t == 'lower_bound':
        return f'> {low} {unit}'
    return f'{low} \u2013 {high} {unit}'


# ── Spectrum bar ─────────────────────────────────────────────────────────────
def _build_spectrum_drawing(data, sex, width=440):
    H       = 36          # total drawing height
    BAR_Y0  = 10          # bar bottom
    BAR_Y1  = 22          # bar top
    BAR_H   = BAR_Y1 - BAR_Y0
    TICK_Y  = 2           # tick label baseline
    VAL_Y   = BAR_Y1 + 3  # value label baseline

    metric_type = data.get('type', 'hilo')
    value       = data['value']
    unit        = data.get('unit', '')
    d           = Drawing(width, H)

    # ── Presence type ──
    if metric_type == 'presence':
        if value == 0:
            d.add(Rect(0, BAR_Y0, width, BAR_H, fillColor=GREEN, strokeColor=None))
            d.add(String(width / 2, BAR_Y0 + 3, 'Not detected',
                         fontName='Figtree', fontSize=8,
                         fillColor=WHITE, textAnchor='middle'))
        else:
            chart_max = value * 2.5
            bar_px = min(width, width * (value / chart_max))
            d.add(Rect(0, BAR_Y0, width, BAR_H, fillColor=BG_ELEVATED, strokeColor=None))
            d.add(Rect(0, BAR_Y0, bar_px, BAR_H, fillColor=RED_BAR, strokeColor=None))
            d.add(Circle(min(bar_px, width - 5), (BAR_Y0 + BAR_Y1) / 2, 5,
                         fillColor=WHITE, strokeColor=TEXT_PRIMARY, strokeWidth=1))
        return d

    # ── Regular spectrum ──
    low, high = _get_range(data, sex)
    span = (high - low) if high > low else max(low, 1)

    chart_min = min(value, low)  - span * 0.2
    chart_max = max(value, high) + span * 0.2

    if metric_type in ('upper_bound', 'presence'):
        chart_min = 0
    elif metric_type == 'lower_bound':
        eff = value if value != low else (low * 1.3 if low > 0 else low + 1)
        if eff >= low:
            chart_min = max(0, (3 * low - eff) / 2)
            chart_max = chart_min + (eff - chart_min) / 0.60
        else:
            chart_min = max(0, 2.2 * eff - 1.2 * low)
            chart_max = chart_min + (low - chart_min) / 0.55

    total = chart_max - chart_min or 1

    def to_x(v):
        return max(0.0, min(float(width), width * (v - chart_min) / total))

    low_x = to_x(low)
    high_x = to_x(high)
    val_x  = to_x(value)

    # Zone rects
    if metric_type == 'lower_bound':
        d.add(Rect(low_x, BAR_Y0, width - low_x, BAR_H, fillColor=GREEN_BAR, strokeColor=None))
        if chart_min < low:
            d.add(Rect(0, BAR_Y0, low_x, BAR_H, fillColor=RED_BAR, strokeColor=None))
    elif metric_type == 'upper_bound':
        d.add(Rect(0, BAR_Y0, high_x, BAR_H, fillColor=GREEN_BAR, strokeColor=None))
        if chart_max > high:
            d.add(Rect(high_x, BAR_Y0, width - high_x, BAR_H, fillColor=RED_BAR, strokeColor=None))
    else:  # hilo
        d.add(Rect(low_x, BAR_Y0, high_x - low_x, BAR_H, fillColor=GREEN_BAR, strokeColor=None))
        if chart_min < low:
            d.add(Rect(0, BAR_Y0, low_x, BAR_H, fillColor=RED_BAR, strokeColor=None))
        if chart_max > high:
            d.add(Rect(high_x, BAR_Y0, width - high_x, BAR_H, fillColor=RED_BAR, strokeColor=None))

    # Tick labels
    if metric_type == 'lower_bound':
        d.add(String(low_x, TICK_Y, str(low),
                     fontName='Figtree', fontSize=7, fillColor=TEXT_SEC, textAnchor='middle'))
    elif metric_type == 'upper_bound':
        d.add(String(high_x, TICK_Y, str(high),
                     fontName='Figtree', fontSize=7, fillColor=TEXT_SEC, textAnchor='middle'))
    else:
        d.add(String(low_x,  TICK_Y, str(low),
                     fontName='Figtree', fontSize=7, fillColor=TEXT_SEC, textAnchor='middle'))
        d.add(String(high_x, TICK_Y, str(high),
                     fontName='Figtree', fontSize=7, fillColor=TEXT_SEC, textAnchor='middle'))

    # Value marker and label
    d.add(Circle(val_x, (BAR_Y0 + BAR_Y1) / 2, 6,
                 fillColor=WHITE, strokeColor=TEXT_PRIMARY, strokeWidth=1.5))
    d.add(String(val_x, VAL_Y, f'{value} {unit}',
                 fontName='Figtree', fontSize=7.5, fillColor=TEXT_PRIMARY, textAnchor='middle'))

    return d


# ── Header ───────────────────────────────────────────────────────────────────
def _build_header(styles, sex, report_date, content_width):
    day_str    = f"{report_date.day} {report_date.strftime('%B %Y')}"
    title_para = Paragraph('Blood Test Report', styles['title'])
    sub_para   = Paragraph(f"{day_str} &nbsp;&middot;&nbsp; Sex: {sex}", styles['subtitle'])

    logo_path = _ASSETS / 'logo.png'
    if logo_path.exists():
        with PILImage.open(str(logo_path)) as pil_img:
            img_w, img_h = pil_img.size
        max_w, max_h = 120, 50
        scale    = min(max_w / img_w, max_h / img_h)
        logo_img = Image(str(logo_path), width=img_w * scale, height=img_h * scale)
        data     = [[logo_img, [title_para, sub_para]]]
        col_w    = [max_w + 10, content_width - max_w - 10]
    else:
        data  = [[[title_para, sub_para]]]
        col_w = [content_width]

    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
        ('TOPPADDING',    (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    return t


# ── Summary strip ────────────────────────────────────────────────────────────
def _build_summary_strip(n_abn, n_norm, styles, content_width):
    half = (content_width - 6) / 2

    abn_cell  = [Paragraph(str(n_abn),  styles['summary_n']),
                 Paragraph(f'Abnormal result{"s" if n_abn  != 1 else ""}', styles['summary_lbl'])]
    norm_cell = [Paragraph(str(n_norm), styles['summary_n']),
                 Paragraph(f'Normal result{"s" if n_norm != 1 else ""}',   styles['summary_lbl'])]

    t = Table([[abn_cell, norm_cell]], colWidths=[half, half])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, 0), RED),
        ('BACKGROUND',    (1, 0), (1, 0), GREEN),
        ('TOPPADDING',    (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING',   (0, 0), (-1, -1), 18),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 18),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


# ── Abnormal card ─────────────────────────────────────────────────────────────
def _build_abnormal_card(data, status, explanation, advice, sex, styles, content_width):
    PAD     = 14
    inner_w = content_width - PAD * 2

    # Badge pill
    badge_bg   = RED if status == 'High' else ORANGE
    badge_text = 'HIGH' if status == 'High' else 'LOW'
    badge_pill = Table([[Paragraph(badge_text, styles['badge'])]],
                       colWidths=[None])
    badge_pill.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, 0), badge_bg),
        ('TOPPADDING',    (0, 0), (0, 0), 3),
        ('BOTTOMPADDING', (0, 0), (0, 0), 3),
        ('LEFTPADDING',   (0, 0), (0, 0), 8),
        ('RIGHTPADDING',  (0, 0), (0, 0), 8),
    ]))

    # Info row: your result | normal range | status
    third     = inner_w / 3
    value_str = f'{data["value"]} {data["unit"]}'
    range_str = _range_str(data, sex)
    info = Table([[
        [Paragraph('Your result',   styles['info_label']), Paragraph(value_str, styles['info_value'])],
        [Paragraph('Normal range',  styles['info_label']), Paragraph(range_str, styles['info_value'])],
        [Paragraph('Status',        styles['info_label']), Paragraph(status,    styles['info_value'])],
    ]], colWidths=[third, third, third])
    info.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
        ('TOPPADDING',    (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    spectrum = _build_spectrum_drawing(data, sex, width=inner_w)

    card_content = [
        badge_pill,
        Spacer(1, 6),
        Paragraph(data['name'], styles['metric_name']),
        info,
        Spacer(1, 10),
        spectrum,
        Spacer(1, 10),
        Paragraph('What this means', styles['body_label']),
        Paragraph(explanation, styles['body']),
        Spacer(1, 6),
        Paragraph('Advice', styles['body_label']),
        Paragraph(advice, styles['body']),
    ]

    card = Table([[card_content]], colWidths=[content_width])
    card.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (0, 0), RED_DIM),
        ('BOX',           (0, 0), (0, 0), 1.5, RED),
        ('TOPPADDING',    (0, 0), (0, 0), PAD),
        ('BOTTOMPADDING', (0, 0), (0, 0), PAD),
        ('LEFTPADDING',   (0, 0), (0, 0), PAD),
        ('RIGHTPADDING',  (0, 0), (0, 0), PAD),
        ('VALIGN',        (0, 0), (0, 0), 'TOP'),
    ]))
    return KeepTogether([card, Spacer(1, 10)])


# ── Normal results table ─────────────────────────────────────────────────────
def _build_normal_table(normal_results, sex, styles, content_width):
    col_w = [
        content_width * 0.38,
        content_width * 0.20,
        content_width * 0.28,
        content_width * 0.14,
    ]

    rows = [[
        Paragraph('Metric',       styles['th']),
        Paragraph('Result',       styles['th']),
        Paragraph('Normal range', styles['th']),
        Paragraph('Status',       styles['th']),
    ]]

    for metric, (data, status, explanation, advice) in normal_results.items():
        rows.append([
            Paragraph(data['name'],                        styles['td_name']),
            Paragraph(f'{data["value"]} {data["unit"]}',   styles['td_center']),
            Paragraph(_range_str(data, sex),               styles['td_center']),
            Paragraph(status,                              styles['td_status']),
        ])

    style_cmds = [
        ('BACKGROUND',  (0, 0), (-1, 0), BG_ELEVATED),
        ('LINEBELOW',   (0, 0), (-1, 0), 1.5, GREEN),
        ('TOPPADDING',  (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW',   (0, 1), (-1, -1), 0.5, ROW_LINE),
    ]
    for i in range(1, len(rows)):
        bg = GREEN_DIM if i % 2 == 0 else WHITE
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

    t = Table(rows, colWidths=col_w, repeatRows=1)
    t.setStyle(TableStyle(style_cmds))
    return t


# ── Page footer ───────────────────────────────────────────────────────────────
_DISCLAIMER = (
    "This report is for informational purposes only and is not a substitute for "
    "professional medical advice, diagnosis, or treatment. "
    "Please consult a qualified healthcare professional regarding your results."
)

def _page_footer(canvas, doc):
    canvas.saveState()
    page_w, _ = A4
    margin     = 2 * cm
    font_name  = 'Figtree'
    font_size  = 7.5
    line_h     = 10
    page_num   = f'Page {doc.page}'

    # Measure page number width to reserve space
    pn_width = canvas.stringWidth(page_num, font_name, font_size)
    text_w   = page_w - 2 * margin - pn_width - 10

    # Wrap disclaimer to fit
    lines = simpleSplit(_DISCLAIMER, font_name, font_size, text_w)
    total_h = len(lines) * line_h

    rule_y  = margin * 0.8 + total_h
    text_y0 = rule_y - line_h

    canvas.setStrokeColor(ORANGE)
    canvas.setLineWidth(0.8)
    canvas.line(margin, rule_y, page_w - margin, rule_y)

    canvas.setFont(font_name, font_size)
    canvas.setFillColor(TEXT_MUTED)
    for i, line in enumerate(lines):
        canvas.drawString(margin, text_y0 - i * line_h, line)

    canvas.drawRightString(page_w - margin, text_y0, page_num)
    canvas.restoreState()


# ── Public entry point ────────────────────────────────────────────────────────
def generate_pdf_report(abnormal_results, normal_results, sex, report_date=None):
    """Build and return a PDF blood test report as bytes."""
    if report_date is None:
        report_date = date.today()

    _register_fonts()
    styles = _build_styles()

    buf         = io.BytesIO()
    page_w, _   = A4
    margin      = 2 * cm
    footer_h    = 2.0 * cm
    content_w   = page_w - 2 * margin

    frame = Frame(
        margin, margin + footer_h,
        content_w, A4[1] - 2 * margin - footer_h,
        id='main',
        leftPadding=0, rightPadding=0,
        topPadding=0, bottomPadding=0,
    )

    doc = BaseDocTemplate(
        buf, pagesize=A4,
        leftMargin=margin, rightMargin=margin,
        topMargin=margin, bottomMargin=margin + footer_h,
    )
    doc.addPageTemplates([PageTemplate(
        id='main', frames=[frame], onPage=_page_footer
    )])

    story = []

    # Header + rule
    story.append(_build_header(styles, sex, report_date, content_w))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width='100%', thickness=1, color=ORANGE, spaceAfter=14))

    # Summary strip
    story.append(_build_summary_strip(
        len(abnormal_results), len(normal_results), styles, content_w
    ))
    story.append(Spacer(1, 22))

    # Abnormal results
    story.append(Paragraph('ABNORMAL RESULTS', styles['section_abn']))
    story.append(HRFlowable(width='100%', thickness=1, color=RED, spaceAfter=10))

    if abnormal_results:
        for metric, (data, status, explanation, advice) in abnormal_results.items():
            story.append(_build_abnormal_card(
                data, status, explanation, advice, sex, styles, content_w
            ))
    else:
        story.append(Paragraph('All results are within normal range.', styles['body']))

    story.append(Spacer(1, 18))

    # Normal results
    story.append(Paragraph('NORMAL RESULTS', styles['section_norm']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN, spaceAfter=10))

    if normal_results:
        story.append(_build_normal_table(normal_results, sex, styles, content_w))
    else:
        story.append(Paragraph('No results in the normal range.', styles['body']))

    doc.build(story)
    return buf.getvalue()
