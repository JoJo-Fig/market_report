#generate_report.py
import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
from utils.logger import Logger

logger = Logger("logs")

def generate_report_from_json(data: list[dict]) -> str | None:
    if not data:
        logger.error("No data provided to generate report.")
        return None

    report_dir = os.path.join("reports")
    os.makedirs(report_dir, exist_ok=True)
    chart_dir = os.path.join(report_dir, "charts")
    os.makedirs(chart_dir, exist_ok=True)

    pdf_filename = f"market_report_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    pdf_path = os.path.join(report_dir, pdf_filename)

    # Reusable header for each page
    def header(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 16)
        canvas.drawString(72, 750, "Market Report")
        canvas.setFont('Helvetica', 10)
        canvas.drawString(72, 735, f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        canvas.restoreState()

    doc = BaseDocTemplate(pdf_path, pagesize=letter)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
    doc.addPageTemplates([PageTemplate(id='StockReport', frames=frame, onPage=header)])

    styles = getSampleStyleSheet()
    story = []

    for i, row in enumerate(data):
        try:
            symbol = row.get('symbol', 'N/A')
            company_name = row.get('company_name', 'N/A')
            story.append(Paragraph(f"{symbol} - {company_name}", styles['Heading2']))
            story.append(Spacer(1,6))

            # Price / Indicator table
            price_data = [
                ["Latest Close", row.get("latest_close", "N/A")],
                ["EMA", row.get("ema", "N/A")],
                ["RSI", row.get("rsi", "N/A")],
                ["ATR", row.get("atr", "N/A")],
            ]
            t = Table(price_data, colWidths=[100,100])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('ALIGN', (0,0), (0,-1), 'LEFT'),
                ('ALIGN', (1,0), (1,-1), 'RIGHT')
            ]))
            story.append(t)
            story.append(Spacer(1,12))

            # Support/Resistance
            sr_data = row.get("support_resistance", {})
            support_levels = sr_data.get("support", [])
            resistance_levels = sr_data.get("resistance", [])
            story.append(Paragraph(
                "Support Levels: " + (', '.join(map(str, support_levels)) if support_levels else "N/A"),
                styles['Normal']
            ))
            story.append(Paragraph(
                "Resistance Levels: " + (', '.join(map(str, resistance_levels)) if resistance_levels else "N/A"),
                styles['Normal']
            ))
            story.append(Spacer(1,12))

            # News headlines
            news_list = row.get("news", [])
            if news_list:
                story.append(Paragraph("Recent News:", styles['Heading3']))
                for news_item in news_list[:5]:
                    headline = news_item.get('headline', 'N/A')
                    source = news_item.get('source', 'N/A')
                    url = news_item.get('url', 'N/A')
                    story.append(Paragraph(f"- {headline} ({source})", styles['Normal']))
                    story.append(Paragraph(f"  {url}", styles['Normal']))
                story.append(Spacer(1,12))

            # Price history chart
            price_history = row.get("price_history", [])
            if price_history:
                plt.figure(figsize=(5,2))
                plt.plot(price_history, marker='o', linestyle='-')
                plt.title(f"{symbol} Price History")
                plt.xlabel("Time")
                plt.ylabel("Price")
                plt.grid(True)
                chart_path = os.path.join(chart_dir, f"{symbol}_chart.png")
                plt.tight_layout()
                plt.savefig(chart_path)
                plt.close()
                story.append(Image(chart_path, width=400, height=200))
                story.append(Spacer(1,12))

            # Page break after each stock except the last one
            if i < len(data) - 1:
                story.append(PageBreak())

        except Exception as e:
            logger.error(f"Error processing row {row.get('symbol', 'N/A')}: {e}")
            continue

    try:
        doc.build(story)
        logger.info(f"PDF report generated: {pdf_path}")
        return pdf_path
    except Exception as e:
        logger.error(f"Failed to build PDF report: {e}")
        return None
