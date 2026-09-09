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


def build_scan(path: Path) -> None:
    """A PDF with no text layer, as a scanned exhibit would be."""
    from reportlab.lib.pagesizes import LETTER
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas as pdfcanvas

    c = pdfcanvas.Canvas(str(path), pagesize=LETTER)
    # Grey blocks standing in for scanned lines. No text is drawn, so nothing extracts.
    c.setFillGray(0.75)
    for i in range(24):
        c.rect(
            inch,
            LETTER[1] - 1.5 * inch - i * 0.28 * inch,
            (LETTER[0] - 2 * inch) * (0.95 if i % 5 else 0.55),
            8,
            stroke=0,
            fill=1,
        )
    c.showPage()
    c.save()


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


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    build_lease(OUT / "cedar-point-lease.pdf")
    build_amendment(OUT / "cedar-point-lease-amendment-1.docx")
    build_scan(OUT / "cedar-point-exhibit-a-scan.pdf")
    for p in sorted(OUT.iterdir()):
        print(f"  {p.name:44s} {p.stat().st_size:>8,d} bytes")
