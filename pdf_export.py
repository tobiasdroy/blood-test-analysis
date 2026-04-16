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
from reportlab.graphics.shapes import Path as RLPath
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


# ── Inline pill spectrum bar ──────────────────────────────────────────────────
# Bezier kappa constant: approximates a quarter-circle with a cubic curve.
_K = 0.5523

def _pill_segment(d, x0, x1, y0, h, color, round_left=False, round_right=False):
    """Add a coloured bar segment to Drawing d with optional rounded pill ends."""
    if x1 <= x0:
        return
    r  = h / 2
    y1 = y0 + h
    p  = RLPath(fillColor=color, strokeColor=None)
    if round_left and round_right:
        p.moveTo(x0 + r, y0)
        p.lineTo(x1 - r, y0)
        p.curveTo(x1 - r*(1-_K), y0,  x1, y0 + r*(1-_K), x1, y0 + r)
        p.lineTo(x1, y1 - r)
        p.curveTo(x1, y1 - r*(1-_K),  x1 - r*(1-_K), y1, x1 - r, y1)
        p.lineTo(x0 + r, y1)
        p.curveTo(x0 + r*(1-_K), y1,  x0, y1 - r*(1-_K), x0, y1 - r)
        p.lineTo(x0, y0 + r)
        p.curveTo(x0, y0 + r*(1-_K),  x0 + r*(1-_K), y0, x0 + r, y0)
    elif round_left:
        p.moveTo(x0 + r, y0)
        p.lineTo(x1, y0)
        p.lineTo(x1, y1)
        p.lineTo(x0 + r, y1)
        p.curveTo(x0 + r*(1-_K), y1,  x0, y1 - r*(1-_K), x0, y1 - r)
        p.lineTo(x0, y0 + r)
        p.curveTo(x0, y0 + r*(1-_K),  x0 + r*(1-_K), y0, x0 + r, y0)
    elif round_right:
        p.moveTo(x0, y0)
        p.lineTo(x1 - r, y0)
        p.curveTo(x1 - r*(1-_K), y0,  x1, y0 + r*(1-_K), x1, y0 + r)
        p.lineTo(x1, y1 - r)
        p.curveTo(x1, y1 - r*(1-_K),  x1 - r*(1-_K), y1, x1 - r, y1)
        p.lineTo(x0, y1)
        p.lineTo(x0, y0)
    else:
        p.moveTo(x0, y0)
        p.lineTo(x1, y0)
        p.lineTo(x1, y1)
        p.lineTo(x0, y1)
    p.closePath()
    d.add(p)


def _build_inline_spectrum(data, sex, width=120, height=8, show_labels=False):
    """Compact pill-shaped spectrum bar with a value-position marker.

    When show_labels=True the drawing grows: LABEL_H points below the bar for
    range-boundary ticks, and VAL_LABEL_H points above for the result value.
    """
    LABEL_H     = 9    # space below bar for low/high boundary labels
    VAL_LABEL_H = 9    # space above bar for the result value label
    metric_type = data.get('type', 'hilo')
    value       = data['value']
    unit        = data.get('unit', '')
    r           = height / 2
    bar_y0      = LABEL_H if show_labels else 0
    mid_y       = bar_y0 + height / 2
    total_h     = height + (LABEL_H + VAL_LABEL_H if show_labels else 0)
    d           = Drawing(width, total_h)

    if metric_type == 'presence':
        if value == 0:
            _pill_segment(d, 0, width, bar_y0, height, GREEN,
                          round_left=True, round_right=True)
        else:
            fill_x = min(width, width * value / (value * 2.5))
            _pill_segment(d, 0, width,  bar_y0, height, BG_ELEVATED,
                          round_left=True, round_right=True)
            _pill_segment(d, 0, fill_x, bar_y0, height, RED_BAR,
                          round_left=True, round_right=(fill_x >= width))
            marker_x = max(r, min(width - r, fill_x))
            d.add(Circle(marker_x, mid_y, r,
                         fillColor=WHITE, strokeColor=TEXT_SEC, strokeWidth=0.8))
        return d

    low, high = _get_range(data, sex)
    span = (high - low) if high > low else max(low, 1)
    chart_min = min(value, low)  - span * 0.2
    chart_max = max(value, high) + span * 0.2

    if metric_type == 'upper_bound':
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

    low_x  = to_x(low)
    high_x = to_x(high)
    val_x  = max(r, min(width - r, to_x(value)))

    if metric_type == 'lower_bound':
        segs = [(0, low_x, RED_BAR), (low_x, width, GREEN_BAR)]
    elif metric_type == 'upper_bound':
        segs = [(0, high_x, GREEN_BAR), (high_x, width, RED_BAR)]
    else:
        segs = [(0, low_x, RED_BAR), (low_x, high_x, GREEN_BAR), (high_x, width, RED_BAR)]

    for i, (sx0, sx1, color) in enumerate(segs):
        _pill_segment(d, sx0, sx1, bar_y0, height, color,
                      round_left=(i == 0),
                      round_right=(i == len(segs) - 1))

    d.add(Circle(val_x, mid_y, r,
                 fillColor=WHITE, strokeColor=TEXT_SEC, strokeWidth=0.8))

    if show_labels:
        # Value label above the bar, centred on the marker
        vx = max(12.0, min(width - 12.0, val_x))
        d.add(String(vx, bar_y0 + height + 3, str(value),
                     fontName='Figtree', fontSize=6.5,
                     fillColor=TEXT_SEC, textAnchor='middle'))

        # Range-boundary labels below the bar
        if metric_type == 'lower_bound':
            ticks = [(low_x, str(low))]
        elif metric_type == 'upper_bound':
            ticks = [(high_x, str(high))]
        else:
            ticks = [(low_x, str(low)), (high_x, str(high))]
        for tx, label in ticks:
            tx_clamped = max(8.0, min(width - 8.0, tx))
            d.add(String(tx_clamped, 1, label,
                         fontName='Figtree', fontSize=6.5,
                         fillColor=TEXT_SEC, textAnchor='middle'))

    return d




# ── Header ───────────────────────────────────────────────────────────────────
def _build_header(styles, sex, report_date, content_width, patient_name=""):
    day_str    = f"{report_date.day} {report_date.strftime('%B %Y')}"
    title_para = Paragraph('Blood Test Report', styles['title'])
    subtitle_parts = [day_str, f"Sex: {sex}"]
    if patient_name:
        subtitle_parts.insert(0, patient_name)
    sub_para   = Paragraph(" &nbsp;&middot;&nbsp; ".join(subtitle_parts), styles['subtitle'])

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

    # Info row: your result | normal range | status | spectrum (inline)
    col_i     = inner_w * 0.21
    col_s     = inner_w * 0.37
    value_str = f'{data["value"]} {data["unit"]}'
    range_str = _range_str(data, sex)
    spectrum  = _build_inline_spectrum(data, sex, width=col_s - 8, height=10, show_labels=True)
    info = Table([[
        [Paragraph('Your result',   styles['info_label']), Paragraph(value_str, styles['info_value'])],
        [Paragraph('Normal range',  styles['info_label']), Paragraph(range_str, styles['info_value'])],
        [Paragraph('Status',        styles['info_label']), Paragraph(status,    styles['info_value'])],
        spectrum,
    ]], colWidths=[col_i, col_i, col_i, col_s])
    info.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('VALIGN',        (3, 0), (3, 0),   'MIDDLE'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 0),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 0),
        ('TOPPADDING',    (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING',   (3, 0), (3, 0),   4),
    ]))

    card_content = [
        badge_pill,
        Spacer(1, 6),
        Paragraph(data['name'], styles['metric_name']),
        info,
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
    # 5 columns: Name | Result | Spectrum | Normal range | Status
    col_w = [
        content_width * 0.29,
        content_width * 0.13,
        content_width * 0.24,
        content_width * 0.21,
        content_width * 0.13,
    ]
    spec_col_w = col_w[2] - 10   # inner width for the spectrum bar (minus cell padding)

    rows = [[
        Paragraph('Metric',       styles['th']),
        Paragraph('Result',       styles['th']),
        Paragraph('',             styles['th']),   # spectrum column — no header label
        Paragraph('Normal range', styles['th']),
        Paragraph('Status',       styles['th']),
    ]]

    style_cmds = [
        ('BACKGROUND',    (0, 0), (-1, 0), BG_ELEVATED),
        ('LINEBELOW',     (0, 0), (-1, 0), 1.5, GREEN),
        ('TOPPADDING',    (0, 0), (-1, 0), 6),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
    ]

    for i, (metric, (data, status, explanation, advice)) in enumerate(normal_results.items()):
        row_idx = 1 + i
        spectrum = _build_inline_spectrum(data, sex, width=spec_col_w, height=7)
        rows.append([
            Paragraph(data['name'],                       styles['td_name']),
            Paragraph(f'{data["value"]} {data["unit"]}',  styles['td_center']),
            spectrum,
            Paragraph(_range_str(data, sex),              styles['td_center']),
            Paragraph(status,                             styles['td_status']),
        ])

        bg = GREEN_DIM if i % 2 == 0 else WHITE
        style_cmds += [
            ('BACKGROUND',    (0, row_idx), (-1, row_idx), bg),
            ('TOPPADDING',    (0, row_idx), (-1, row_idx), 7),
            ('BOTTOMPADDING', (0, row_idx), (-1, row_idx), 7),
            ('LINEBELOW',     (0, row_idx), (-1, row_idx), 0.5, ROW_LINE),
        ]

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
def generate_pdf_report(abnormal_results, normal_results, sex, report_date=None, patient_name=""):
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
    story.append(_build_header(styles, sex, report_date, content_w, patient_name))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width='100%', thickness=1, color=ORANGE, spaceAfter=14))

    # Summary strip
    story.append(_build_summary_strip(
        len(abnormal_results), len(normal_results), styles, content_w
    ))
    story.append(Spacer(1, 22))

    # Abnormal results — keep heading + rule together; cards flow independently
    story.append(KeepTogether([
        Paragraph('ABNORMAL RESULTS', styles['section_abn']),
        HRFlowable(width='100%', thickness=1, color=RED, spaceAfter=10),
    ]))
    if abnormal_results:
        for metric, vals in abnormal_results.items():
            story.append(_build_abnormal_card(*vals, sex, styles, content_w))
    else:
        story.append(Paragraph('All results are within normal range.', styles['body']))

    story.append(Spacer(1, 18))

    # Normal results — keep heading + rule with the table
    norm_body = [
        Paragraph('NORMAL RESULTS', styles['section_norm']),
        HRFlowable(width='100%', thickness=1, color=GREEN, spaceAfter=10),
    ]
    if normal_results:
        norm_body.append(_build_normal_table(normal_results, sex, styles, content_w))
    else:
        norm_body.append(Paragraph('No results in the normal range.', styles['body']))
    story.append(KeepTogether(norm_body))

    doc.build(story)
    return buf.getvalue()
