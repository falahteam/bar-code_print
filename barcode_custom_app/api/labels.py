# import frappe
# from io import BytesIO
# from reportlab.lib.pagesizes import mm
# from reportlab.pdfgen import canvas
# from reportlab.graphics.barcode import eanbc, code128
# from reportlab.graphics.shapes import Drawing
# from reportlab.graphics import renderPDF

# @frappe.whitelist()
# def generate_barcode_labels(docname):
#     doc = frappe.get_doc("Purchase Invoice", docname)

#     buffer = BytesIO()
#     sticker_width = 39 * mm
#     sticker_height = 29 * mm
#     margin_top = 3 * mm

#     c = canvas.Canvas(buffer, pagesize=(sticker_width, sticker_height))

#     for item in doc.items:
#         qty = int(item.qty or 1)

#         # Get barcode value (trimmed)
#         raw_barcode = frappe.db.get_value("Item Barcode", {
#             "parent": item.item_code,
#             "barcode_type": "EAN"
#         }, "barcode") or item.item_code

#         barcode_val = str(raw_barcode).strip()[:30]  # Clip max 30 chars
#         item_name = item.item_name or ""
#         company = frappe.db.get_value("Company", doc.company, "company_name") or ""
#         currency = doc.currency or frappe.db.get_value("Company", doc.company, "default_currency") or ""
#         price_val = frappe.db.get_value("Item Price", {
#             "item_code": item.item_code,
#             "price_list": "Standard Selling"
#         }, "price_list_rate")
#         price_label = f"{currency} {price_val:.2f}" if price_val else "NA"

#         for _ in range(qty):
#             # Company Name
#             c.setFont("Helvetica-Bold", 7)
#             c.drawCentredString(sticker_width / 2, sticker_height - margin_top, company[:25])

#             try:
#                 # EAN-13 must be exactly 12 digits (13th is checksum)
#                 if len(barcode_val) == 12 and barcode_val.isdigit():
#                     barcode = eanbc.Ean13BarcodeWidget(barcode_val)
#                     bounds = barcode.getBounds()
#                     width = bounds[2] - bounds[0]
#                     height = bounds[3] - bounds[1]
#                     d = Drawing(width, height)
#                     d.add(barcode)
#                     renderPDF.draw(d, c, (sticker_width - width) / 2, 11.5 * mm)
#                 else:
#                     raise ValueError("Invalid EAN13 barcode")
#             except Exception:
#                 # Fallback to Code128 for anything else
#                 barcode = code128.Code128(barcode_val, barWidth=0.25 * mm, barHeight=12 * mm)
#                 barcode_x = (sticker_width - barcode.width) / 2
#                 barcode.drawOn(c, barcode_x, 11.5 * mm)

#             # Barcode number
#             c.setFont("Helvetica", 6.5)
#             c.drawCentredString(sticker_width / 2, 9.3 * mm, barcode_val)

#             # Item name
#             c.setFont("Helvetica", 6)
#             c.drawCentredString(sticker_width / 2, 7.3 * mm, item_name[:24])

#             # Price
#             c.setFont("Helvetica-Bold", 6)
#             c.drawCentredString(sticker_width / 2, 5.3 * mm, f"Price: {price_label}")

#             c.showPage()

#     c.save()

#     # Serve PDF inline in browser
#     frappe.local.response.filename = f"Barcode-Labels-{docname}.pdf"
#     frappe.local.response.filecontent = buffer.getvalue()
#     frappe.local.response.type = "pdf"
#     frappe.local.response.headers = {
#         "Content-Disposition": f'inline; filename="Barcode-Labels-{docname}.pdf"'
#     }


import frappe
from io import BytesIO
from reportlab.lib.pagesizes import mm
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128

@frappe.whitelist()
def generate_barcode_labels(docname):
    doc = frappe.get_doc("Purchase Invoice", docname)

    buffer = BytesIO()
    sticker_width = 50 * mm
    sticker_height = 38 * mm
    # margin_left = 3 * mm

    c = canvas.Canvas(buffer, pagesize=(sticker_width, sticker_height))

    for item in doc.items:
        qty = int(item.qty or 1)
        barcode_val = frappe.db.get_value("Item Barcode", {
            "parent": item.item_code,
            "barcode_type": "Code 128"
        }, "barcode") or item.item_code
        barcode_val = str(barcode_val).strip()[:30]  # Clip max 30 chars
        item_name = item.item_name or ""
        item_code = item.item_code or ""
        company = frappe.db.get_value("Company", doc.company, "company_name") or ""
        currency = doc.currency or frappe.db.get_value("Company", doc.company, "default_currency") or ""
        price_val = frappe.db.get_value("Item Price", {
            "item_code": item.item_code,
            "price_list": "Standard Selling"
        }, "price_list_rate")
        price_label = f"{currency} {price_val:.2f}" if price_val else "NA"

        for _ in range(qty):
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(sticker_width / 2, sticker_height - 7 * mm, "Shifa Enterprices")

            # Code 128 barcode
            barcode = code128.Code128(barcode_val, barWidth=0.25 * mm, barHeight=12 * mm)
            barcode_x = (sticker_width - barcode.width) / 2
            barcode.drawOn(c, barcode_x, 15 * mm)

            c.setFont("Helvetica", 7)
            c.drawCentredString(sticker_width / 2, 12 * mm, barcode_val)

            c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(sticker_width / 2, 8 * mm, f"{item_name[:25]} {item_code[:25]}")
			
			c.setFont("Helvetica-Bold", 7)
            c.drawCentredString(sticker_width / 2, 4 * mm, f"Price: {custom_single_peace_price}")
			
			c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(sticker_width / 2, 4 * mm, f"Price: {price_label}")



			c.showPage()

    c.save()

    frappe.local.response.filename = f"Barcode-Labels-{docname}.pdf"
    frappe.local.response.filecontent = buffer.getvalue()
    frappe.local.response.type = "pdf"
    frappe.local.response.headers = {
        "Content-Disposition": f'inline; filename="Barcode-Labels-{docname}.pdf"'
    }

