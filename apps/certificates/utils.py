import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

from django_project.settings.base import FONT_PATH

KR_FONT = "NanumGothic"
pdfmetrics.registerFont(TTFont(KR_FONT, FONT_PATH))


def generate_certificate_pdf(user, original_certificate, transfers):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    header_font_size = 20
    section_header_font_size = 16
    body_font_size = 14
    section_spacing = 40
    line_spacing = 24

    # Apply font
    p.setFont(KR_FONT, header_font_size)

    # Header
    p.drawCentredString(
        width / 2,
        height - 100,
        f"{user.name}님이 {original_certificate.creation_date.strftime('%Y-%m-%d')}에",
    )
    p.drawCentredString(width / 2, height - 120, "송금하신 거래내역")

    # <hr>
    p.line(70, height - 150, width - 70, height - 150)

    # User Details Section
    p.setFont(KR_FONT, section_header_font_size)
    p.drawString(70, height - 190, "요청 고객 섹션")

    p.setFont(KR_FONT, body_font_size)
    p.drawString(70, height - 210, f"이름: {user.name}")
    p.drawString(
        70,
        height - 230,
        f"계좌 정보: {user.get_bank_name_display()} {user.bank_account}",
    )

    # Transfer Details Section
    p.setFont(KR_FONT, section_header_font_size)
    p.drawString(70, height - 270, "송금 상세내역")

    p.setFont(KR_FONT, body_font_size)
    current_height = height - 290
    for transfer in transfers:
        p.drawString(
            70,
            current_height,
            f"- {transfer.transfer_id}은행 {transfer.transfer_id}계좌번호에서",
        )
        current_height -= line_spacing

    current_height -= section_spacing
    p.line(70, current_height, width - 70, current_height)

    # Footer / QR Code Placeholder
    current_height -= line_spacing
    p.drawString(
        70,
        current_height,
        "본 문서의 진위 여부는 아래 주소에서 확인할 수 있습니다.",
    )
    current_height -= line_spacing
    # TODO: generate QR image
    p.drawString(
        70,
        current_height,
        "[QR 이미지]: https://toss.im/verify-deposit",
    )

    p.showPage()
    p.save()
    buffer.seek(0)

    return buffer


class AttrDict(dict):
    """
    Dict-like object that exposes its keys as attributes.

    Examples
    --------
    >>> d = AttrDict({'a': 1, 'b': 2})
    >>> d.a
    1
    >>> d = AttrDict({'a': 1, 'b': {'c': 3, 'd': 4}})
    >>> d.b.c
    3
    """

    def __getattr__(self, attr):
        value = self[attr]
        if isinstance(value, dict):
            return AttrDict(value)
        return value
