"""Generate the binary fixtures. Run once; the outputs are committed.

    .venv/bin/python tests/fixtures/build_fixtures.py

The point is to produce documents that behave like a data room's, not like clean text:
multi-page with running headers and footers, justified text that wraps mid-sentence, and
one scan with no text layer at all.
"""

from __future__ import annotations

from pathlib import Path

# reportlab and python-docx are needed only to regenerate the fixtures, which are committed.
# They are imported inside the builders so tests can import the constants below without them.

OUT = Path(__file__).parent / "dataroom"

LEASE_TITLE = "COMMERCIAL LEASE AGREEMENT"

# The clause a Verbatim column would be asked to reproduce. It is long enough to wrap
# across several lines once justified, which is the point.
ASSIGNMENT_CLAUSE = (
    "Tenant shall not assign this Lease or sublet all or any portion of the Premises, "
    "whether voluntarily, involuntarily or by operation of law, without first obtaining "
    "the prior written consent of Landlord, which consent shall not be unreasonably "
    "withheld, conditioned or delayed; provided, however, that a transfer of more than "
    "fifty percent (50%) of the direct or indirect beneficial ownership interests in "
    "Tenant, whether in a single transaction or a series of related transactions, shall "
    "constitute an assignment requiring such consent."
)

LEASE_BODY = [
    (
        "1. PREMISES.",
        (
            "Landlord hereby leases to Tenant, and Tenant hereby leases from Landlord, those "
            "certain premises consisting of approximately 24,500 rentable square feet located "
            "on the third floor of the building commonly known as Cedar Point Commerce Center, "
            "1400 Halstead Avenue, Wilmington, Delaware (the “Premises”), together with "
            "the non-exclusive right to use the common areas of the Building."
        ),
    ),
    (
        "2. TERM.",
        (
            "The initial term of this Lease shall commence on June 1, 2021 (the “Commencement "
            "Date”) and shall expire at 11:59 p.m. on May 31, 2031, unless sooner terminated "
            "in accordance with the provisions hereof. Tenant shall have two (2) consecutive "
            "options to extend the initial term for additional periods of five (5) years each, "
            "exercisable by written notice delivered to Landlord not less than twelve (12) "
            "months prior to the expiration of the then-current term."
        ),
    ),
    (
        "3. BASE RENT.",
        (
            "Tenant shall pay to Landlord base rent in the amount of $58,333.33 per month, "
            "payable in advance on the first day of each calendar month, subject to annual "
            "escalation of three percent (3%) on each anniversary of the Commencement Date. "
            "Base rent for any partial month shall be prorated on a per-diem basis."
        ),
    ),
    ("4. ASSIGNMENT AND SUBLETTING.", ASSIGNMENT_CLAUSE),
    (
        "5. CHANGE OF CONTROL.",
        (
            "For purposes of Section 4, a change of control of Tenant shall be deemed an "
            "assignment. Notwithstanding the foregoing, a transfer to an entity controlling, "
            "controlled by or under common control with Tenant shall not require Landlord's "
            "consent, provided that Tenant delivers written notice to Landlord not less than "
            "thirty (30) days prior to the effective date of such transfer and the transferee "
            "assumes in writing all of Tenant's obligations under this Lease."
        ),
    ),
    (
        "6. LANDLORD'S CONSENT TO THE TRANSACTION.",
        (
            "Landlord acknowledges that Tenant has advised Landlord of a contemplated corporate "
            "reorganization. Nothing in this Lease shall be construed as Landlord's consent to "
            "any such transaction, and any consent required under Section 4 or Section 5 must be "
            "obtained separately and in writing."
        ),
    ),
    (
        "7. GOVERNING LAW.",
        (
            "This Lease shall be governed by and construed in accordance with the laws of the "
            "State of Delaware, without regard to its conflict of laws principles. The parties "
            "irrevocably submit to the exclusive jurisdiction of the state and federal courts "
            "sitting in New Castle County, Delaware."
        ),
    ),
    (
        "8. ESTOPPEL CERTIFICATES.",
        (
            "Within ten (10) business days after Landlord's written request, Tenant shall execute "
            "and deliver an estoppel certificate certifying the Commencement Date, the expiration "
            "date, the amount of base rent then payable, and whether, to Tenant's knowledge, any "
            "default exists under this Lease."
        ),
    ),
    (
        "9. NOTICES.",
        (
            "All notices required or permitted under this Lease shall be in writing and shall be "
            "deemed duly given upon personal delivery, upon confirmed receipt if sent by "
            "nationally recognized overnight courier, or three (3) business days after deposit in "
            "the United States mail, certified, return receipt requested, postage prepaid."
        ),
    ),
    (
        "10. ENTIRE AGREEMENT.",
        (
            "This Lease, together with the exhibits attached hereto, constitutes the entire "
            "agreement between the parties with respect to the subject matter hereof and "
            "supersedes all prior negotiations, understandings and agreements, whether oral or "
            "written. This Lease may be amended only by a written instrument signed by both "
            "parties."
        ),
    ),
]


def _header_footer(canvas, doc) -> None:
    """A running header and footer, which is what interrupts a real PDF's text flow."""
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch

    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(inch, LETTER[1] - 0.6 * inch, "CEDAR POINT COMMERCE CENTER — LEASE AGREEMENT")
    canvas.drawRightString(LETTER[0] - inch, LETTER[1] - 0.6 * inch, "EXECUTION VERSION")
    canvas.drawCentredString(LETTER[0] / 2, 0.55 * inch, f"Page {canvas.getPageNumber()} of 3")
    canvas.drawString(inch, 0.55 * inch, "Confidential")
    canvas.restoreState()


def build_lease(path: Path) -> None:
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer

    doc = BaseDocTemplate(
        str(path),
        pagesize=LETTER,
        leftMargin=inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )
    frame = Frame(inch, inch, LETTER[0] - 2 * inch, LETTER[1] - 2 * inch, id="body")
    doc.addPageTemplates([PageTemplate(id="std", frames=[frame], onPage=_header_footer)])

    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "body",
        parent=styles["Normal"],
        fontName="Times-Roman",
        fontSize=10.5,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
    )
    head = ParagraphStyle("head", parent=body, fontName="Times-Bold", spaceBefore=6)
    title = ParagraphStyle(
        "title", parent=body, fontName="Times-Bold", fontSize=13, alignment=1, spaceAfter=18
    )

    flow = [
        Paragraph(LEASE_TITLE, title),
        Paragraph(
            "This Commercial Lease Agreement (this “Lease”) is made as of May 14, 2021 by and "
            "between Halstead Property Holdings LLC, a Delaware limited liability company "
            "(“Landlord”), and Acme Manufacturing LLC, a Delaware limited liability company "
            "(“Tenant”).",
            body,
        ),
        Spacer(1, 10),
    ]
    for heading, text in LEASE_BODY:
        flow.append(Paragraph(heading, head))
        flow.append(Paragraph(text, body))
    flow.append(Spacer(1, 20))
    flow.append(
        Paragraph(
            "IN WITNESS WHEREOF, the parties have executed this Lease as of the date first "
            "written above.",
            body,
        )
    )
    flow.append(
        Paragraph(
            "HALSTEAD PROPERTY HOLDINGS LLC<br/>By: /s/ Priya Raman<br/>"
            "Name: Priya Raman<br/>Title: Manager",
            body,
        )
    )
    flow.append(
        Paragraph(
            "ACME MANUFACTURING LLC<br/>By: /s/ Morgan Feld<br/>"
            "Name: Morgan Feld<br/>Title: President",
            body,
        )
    )
    doc.build(flow)


#: The text rendered into the scan fixture as an image. OCR must recover it; nothing can
#: extract it, because there is no text layer.
SCAN_TEXT = [
    "EXHIBIT A",
    "MEMORANDUM OF LEASE",
    "",
    "THIS MEMORANDUM OF LEASE is made as of May 14, 2021, by and",
    "between HALSTEAD PROPERTY HOLDINGS LLC, a Delaware limited",
    "liability company, as Landlord, and ACME MANUFACTURING LLC, a",
    "Delaware limited liability company, as Tenant.",
    "",
    "1. Premises. The premises consist of approximately 24,500 rentable",
    "square feet located at 1400 Halstead Avenue, Wilmington, Delaware.",
    "",
    "2. Term. The term commences June 1, 2021 and expires May 31, 2031.",
    "",
    "3. Purpose. This Memorandum is recorded solely to give notice of the",
    "Lease and shall not modify its terms in any respect.",
    "",
    "RECORDED: New Castle County Recorder of Deeds",
    "Instrument No. 2021-0041882",
]

#: A clause a Verbatim column would be asked to reproduce from the scan.
SCAN_VERBATIM = (
    "This Memorandum is recorded solely to give notice of the "
    "Lease and shall not modify its terms in any respect."
)


def build_scan(path: Path) -> None:
    """A PDF whose only content is an image of text, as a recorded exhibit would be.

    Nothing extracts from it: there is no text layer. OCR has to read the picture, which is
    the point — the fixture exercises a real transcription, not an empty page.
    """
    from PIL import Image, ImageDraw, ImageFont
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas as pdfcanvas

    scale = 3  # render large, then let the PDF scale it down: roughly 200 dpi of detail
    width, height = 612 * scale, 792 * scale
    image = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(image)

    font = None
    for candidate in (
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ):
        if Path(candidate).exists():
            font = ImageFont.truetype(candidate, 13 * scale)
            break
    if font is None:  # pragma: no cover - only on a host with none of these fonts
        font = ImageFont.load_default()

    y = 90 * scale
    for line in SCAN_TEXT:
        draw.text((80 * scale, y), line, fill=30, font=font)
        y += 22 * scale

    # A little grey, as a photocopy has: realistic, but not enough to defeat OCR.
    image = image.point(lambda v: min(255, int(v * 0.94 + 12)))

    png = path.with_suffix(".png")
    image.save(png, "PNG")
    c = pdfcanvas.Canvas(str(path), pagesize=LETTER)
    c.drawImage(str(png), 0, 0, width=LETTER[0], height=LETTER[1])
    c.showPage()
    c.save()
    png.unlink()


def build_amendment(path: Path) -> None:
    from docx import Document as Docx

    d = Docx()
    d.add_heading("FIRST AMENDMENT TO COMMERCIAL LEASE AGREEMENT", level=1)
    d.add_paragraph(
        "This First Amendment to Commercial Lease Agreement (this “Amendment”) is made "
        "as of March 2, 2024 by and between Halstead Property Holdings LLC (“Landlord”) "
        "and Acme Manufacturing LLC (“Tenant”), and amends that certain Commercial Lease "
        "Agreement dated as of May 14, 2021 (the “Lease”). Capitalized terms used but not "
        "defined herein have the meanings given in the Lease."
    )
    d.add_paragraph(
        "1. Section 3 (Base Rent) of the Lease is amended to provide that base rent shall be "
        "$61,250.00 per month effective April 1, 2024."
    )
    d.add_paragraph(
        "2. Section 4 (Assignment and Subletting) of the Lease is amended by adding the "
        "following sentence at the end thereof: “Landlord's consent shall not be required "
        "in connection with an assignment to a successor by merger, consolidation, or sale of "
        "all or substantially all of Tenant's assets, provided the successor's tangible net "
        "worth immediately following such transaction is not less than that of Tenant "
        "immediately prior thereto.”"
    )
    d.add_paragraph(
        "3. Except as expressly amended hereby, the Lease remains in full force and effect."
    )
    d.add_paragraph("HALSTEAD PROPERTY HOLDINGS LLC\nBy: /s/ Priya Raman")
    d.add_paragraph("ACME MANUFACTURING LLC\nBy: /s/ Morgan Feld")
    d.save(str(path))


#: Rows of the cap table fixture, so a test can assert what came back.
CAP_TABLE_ROWS = [
    ("Morgan Feld", "Common Units", "Class A", 4500000, "2019-03-01", 0.0001, "45.0%"),
    ("Priya Raman", "Common Units", "Class A", 2500000, "2019-03-01", 0.0001, "25.0%"),
    ("Cedar Ventures LP", "Preferred Units", "Series A", 2000000, "2021-06-15", 1.25, "20.0%"),
    ("Option Pool (unallocated)", "Options", "Class A", 800000, "2021-06-15", None, "8.0%"),
    ("J. Okafor", "Options", "Class A", 120000, "2022-01-10", 0.85, "1.2%"),
]
CENSUS_ROWS = 40
CAP_TABLE_AS_OF = "2026-06-30"


def build_workbook(path: Path) -> None:
    """A cap table and an employee census in one workbook.

    00a calls these Records: they report facts as at a date, and the as-of date is what makes
    one usable. Two sheets in one file is the ordinary case, and the reason sheet boundaries
    have to survive ingestion.
    """
    from openpyxl import Workbook

    wb = Workbook()
    ws = wb.active
    ws.title = "Cap Table"
    ws.append(["Acme Manufacturing LLC — Capitalization Table"])
    ws.append(["As of", CAP_TABLE_AS_OF])
    ws.append([])
    ws.append(
        ["Holder", "Security", "Class", "Units", "Issue Date", "Price per Unit", "Fully Diluted %"]
    )
    for row in CAP_TABLE_ROWS:
        ws.append(list(row))

    census = wb.create_sheet("Employee Census")
    census.append(
        [
            "Employee ID",
            "Name",
            "Title",
            "Location",
            "Hire Date",
            "Base Salary",
            "Bonus Target %",
            "Visa Status",
        ]
    )
    for i in range(1, CENSUS_ROWS + 1):
        census.append(
            [
                f"E{1000 + i}",
                f"Employee {i}",
                "Engineer II" if i % 3 else "Manager",
                "Wilmington, DE" if i % 2 else "Austin, TX",
                f"20{18 + i % 7}-0{1 + i % 9}-15",
                82000 + i * 1350,
                10 if i % 3 else 20,
                "H-1B" if i % 11 == 0 else "US Citizen",
            ]
        )
    wb.save(str(path))


def build_lien_schedule(path: Path) -> None:
    """A CSV schedule, the other shape a data room delivers a register in."""
    import csv as csv_mod

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv_mod.writer(handle)
        writer.writerow(
            [
                "Filing Number",
                "Debtor",
                "Secured Party",
                "Filed Date",
                "Jurisdiction",
                "Collateral Description",
                "Status",
            ]
        )
        writer.writerows(
            [
                [
                    "2019-3348217",
                    "Acme Manufacturing LLC",
                    "Cedar Bank, N.A.",
                    "2019-04-02",
                    "Delaware SOS",
                    "All assets",
                    "Active",
                ],
                [
                    "2021-6612904",
                    "Acme Manufacturing LLC",
                    "Halstead Equipment Finance LLC",
                    "2021-08-19",
                    "Delaware SOS",
                    "Specific equipment",
                    "Active",
                ],
                [
                    "2016-1120388",
                    "Acme Manufacturing LLC",
                    "Northwind Capital Partners",
                    "2016-11-30",
                    "Delaware SOS",
                    "All assets",
                    "Lapsed",
                ],
            ]
        )


#: The new text of the reply, as distinct from the history it quotes.
EMAIL_NEW_TEXT = (
    "Counsel,\n\n"
    "Attached is the executed First Amendment to the Cedar Point lease, together with the\n"
    "landlord's consent letter. The landlord has confirmed it will not require a further\n"
    "consent for the contemplated reorganization, subject to the notice provision in\n"
    "Section 5.\n\n"
    "Please confirm whether you consider the notice requirement satisfied by the letter of\n"
    "12 February.\n\n"
    "Morgan"
)

EMAIL_QUOTED_TEXT = (
    "-----Original Message-----\n"
    "From: Priya Raman <p.raman@halsteadproperty.example>\n"
    "Sent: 12 February 2026 09:14\n"
    "To: Morgan Feld <m.feld@acmemfg.example>\n"
    "Subject: Cedar Point - consent\n\n"
    "Morgan,\n\n"
    "We are content to proceed on the basis discussed. Landlord will not withhold consent.\n\n"
    "Priya"
)

EMAIL_SUBJECT = "PRIVILEGED AND CONFIDENTIAL - Cedar Point lease consent"


def build_email(path: Path, attachment: Path) -> None:
    """A reply carrying a quoted chain, a privilege marking, and the real document attached.

    All three are the things a generic text extractor loses: the header block Table 05 routes
    on, the boundary between new text and repeated history, and the agreement itself.
    """
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["From"] = "Morgan Feld <m.feld@acmemfg.example>"
    msg["To"] = "Jordan Alvarez <j.alvarez@counsel.example>"
    msg["Cc"] = "Priya Raman <p.raman@halsteadproperty.example>"
    msg["Date"] = "Thu, 19 Feb 2026 16:42:11 +0000"
    msg["Subject"] = EMAIL_SUBJECT
    msg.set_content(EMAIL_NEW_TEXT + "\n\n" + EMAIL_QUOTED_TEXT)
    msg.add_attachment(
        attachment.read_bytes(),
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=attachment.name,
    )
    # A signature image, which is mail furniture rather than a produced document.
    msg.add_attachment(
        b"\x89PNG\r\n\x1a\n" + b"0" * 200, maintype="image", subtype="png", filename="image001.png"
    )
    path.write_bytes(msg.as_bytes())


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_lease(OUT / "cedar-point-lease.pdf")
    build_amendment(OUT / "cedar-point-lease-amendment-1.docx")
    build_scan(OUT / "cedar-point-exhibit-a-scan.pdf")
    build_workbook(OUT / "cap-table-and-census.xlsx")
    build_lien_schedule(OUT / "ucc-lien-schedule.csv")
    build_email(OUT / "cedar-point-consent-thread.eml", OUT / "cedar-point-lease-amendment-1.docx")
    for p in sorted(OUT.iterdir()):
        print(f"  {p.name:44s} {p.stat().st_size:>8,d} bytes")
