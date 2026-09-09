"""Email, read as correspondence.

Tables 17, 23 and 25 are built around correspondence, and their review unit is a *matter* —
the initiating communication, the response, the follow-ups, the closing letter. So one
message is one document, and the existing unit assembly groups them into the matter. This
module's job is to turn a message into text a reader can use, and to surface what a generic
text extractor throws away:

- **Headers.** From, To, Cc, Date and Subject are what Table 05 reads to route the message:
  the counterparty, the document date, the subject entity.
- **The quoted chain.** A reply carrying twelve earlier messages duplicates their text into
  every later file. The new content is separated from the history so retrieval ranks what
  was actually written, and so "the most recently dated document" means something.
- **Attachments.** In a data room the attachment is usually the document — the executed
  agreement, the filed return. They are extracted and ingested in their own right, linked
  back to the message that carried them.

`.eml` needs nothing beyond the standard library. `.msg` needs `extract-msg`.
"""

from __future__ import annotations

import email
import email.policy
import re
from dataclasses import dataclass, field
from email.message import EmailMessage
from pathlib import Path

MAIL_SUFFIXES = frozenset({".eml", ".msg"})

#: Where a reply stops being new text and starts quoting what came before.
QUOTE_MARKERS = (
    re.compile(r"^\s*-{2,}\s*Original Message\s*-{2,}", re.I | re.M),
    re.compile(r"^\s*_{5,}\s*$", re.M),
    re.compile(r"^\s*On .{4,120}\bwrote:\s*$", re.I | re.M),
    re.compile(r"^\s*From:.+$\n^\s*Sent:.+$", re.I | re.M),
    re.compile(r"^\s*>{1,}\s?\S", re.M),
)

#: 00a: report the marking and stop. Never assess whether privilege applies.
PRIVILEGE_MARKERS = (
    "privileged and confidential",
    "attorney-client privileged",
    "attorney client privileged",
    "attorney work product",
    "work product",
    "legally privileged",
    "subject to legal professional privilege",
    "privileged & confidential",
)

#: Attachments that are signatures, logos, or tracking pixels rather than documents.
NOISE_ATTACHMENTS = re.compile(r"^(image\d+|oledata|winmail)\.|\.(p7s|p7m|ics|vcf)$", re.I)
MIN_ATTACHMENT_BYTES = 4096


@dataclass(slots=True)
class Attachment:
    filename: str
    content: bytes

    @property
    def is_document(self) -> bool:
        """Whether it looks like a produced document rather than mail furniture."""
        if NOISE_ATTACHMENTS.search(self.filename):
            return False
        return len(self.content) >= MIN_ATTACHMENT_BYTES


@dataclass(slots=True)
class Message:
    sender: str = ""
    to: str = ""
    cc: str = ""
    date: str = ""
    subject: str = ""
    body: str = ""
    quoted: str = ""
    attachments: list[Attachment] = field(default_factory=list)

    @property
    def documents(self) -> list[Attachment]:
        return [a for a in self.attachments if a.is_document]

    def privilege_markings(self) -> list[str]:
        """Markings found in the subject or the new body text. Reported, never assessed."""
        haystack = f"{self.subject}\n{self.body}".lower()
        return [m for m in PRIVILEGE_MARKERS if m in haystack]

    def render(self) -> str:
        """A normalized message: header block, new text, then the quoted history."""
        lines = ["# Email"]
        for label, value in (
            ("From", self.sender),
            ("To", self.to),
            ("Cc", self.cc),
            ("Date", self.date),
            ("Subject", self.subject),
        ):
            if value:
                lines.append(f"{label}: {value}")
        if self.attachments:
            lines.append("Attachments: " + ", ".join(a.filename for a in self.attachments))
        parts = ["\n".join(lines), self.body.strip()]
        if self.quoted.strip():
            parts.append(
                "--- quoted history: text below was written earlier and is repeated here "
                "by the reply ---\n" + self.quoted.strip()
            )
        return "\n\n".join(p for p in parts if p)


def is_mail(suffix: str) -> bool:
    return suffix.lower() in MAIL_SUFFIXES


def split_quoted(body: str) -> tuple[str, str]:
    """Separate what this message says from what it repeats."""
    earliest = len(body)
    for pattern in QUOTE_MARKERS:
        match = pattern.search(body)
        if match and match.start() < earliest:
            earliest = match.start()
    if earliest >= len(body):
        return body.strip(), ""
    return body[:earliest].strip(), body[earliest:].strip()


def _html_to_text(html: str) -> str:
    try:
        from bs4 import BeautifulSoup

        return BeautifulSoup(html, "html.parser").get_text("\n")
    except ImportError:
        return re.sub(r"<[^>]+>", " ", html)


def read_eml(path: Path) -> Message:
    with path.open("rb") as handle:
        parsed: EmailMessage = email.message_from_binary_file(handle, policy=email.policy.default)

    body = ""
    part = parsed.get_body(preferencelist=("plain",))
    if part is not None:
        body = part.get_content()
    else:
        part = parsed.get_body(preferencelist=("html",))
        if part is not None:
            body = _html_to_text(part.get_content())

    attachments: list[Attachment] = []
    for item in parsed.iter_attachments():
        name = item.get_filename()
        if not name:
            continue
        payload = item.get_payload(decode=True)
        if payload:
            attachments.append(Attachment(name, payload))

    new, quoted = split_quoted(body or "")
    return Message(
        sender=str(parsed.get("From", "")),
        to=str(parsed.get("To", "")),
        cc=str(parsed.get("Cc", "")),
        date=str(parsed.get("Date", "")),
        subject=str(parsed.get("Subject", "")),
        body=new,
        quoted=quoted,
        attachments=attachments,
    )


def read_msg(path: Path) -> Message:
    import extract_msg

    with extract_msg.openMsg(str(path)) as msg:
        body = msg.body or ""
        if not body.strip() and getattr(msg, "htmlBody", None):
            raw = msg.htmlBody
            body = _html_to_text(raw.decode("utf-8", "replace") if isinstance(raw, bytes) else raw)
        attachments = []
        for item in msg.attachments:
            name = item.getFilename() or getattr(item, "longFilename", None) or "attachment"
            data = item.data
            if isinstance(data, bytes) and data:
                attachments.append(Attachment(str(name), data))
        new, quoted = split_quoted(body)
        return Message(
            sender=str(msg.sender or ""),
            to=str(msg.to or ""),
            cc=str(msg.cc or ""),
            date=str(msg.date or ""),
            subject=str(msg.subject or ""),
            body=new,
            quoted=quoted,
            attachments=attachments,
        )


def read_message(path: Path) -> Message:
    return read_msg(path) if path.suffix.lower() == ".msg" else read_eml(path)


def privilege_markings_in(text: str) -> list[str]:
    """Markings anywhere in a document's text. 00a: report and stop, never assess."""
    lowered = text.lower()
    return [m for m in PRIVILEGE_MARKERS if m in lowered]
