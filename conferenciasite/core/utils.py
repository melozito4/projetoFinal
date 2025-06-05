from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer, SimpleDocTemplate, Image
from datetime import datetime
import os
from django.conf import settings

def gerar_fatura_pdf(inscricao):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=50, bottomMargin=30)
    elementos = []

    styles = getSampleStyleSheet()
    estilo_normal = styles['Normal']

    # Topo com Fatura e Logo alinhado
    caminho_logo = os.path.join(settings.STATICFILES_DIRS[0], "img", "logo3.png")
    logo = Image(caminho_logo, width=40, height=40)
    header_data = [
        [
            Paragraph('<font size=26 color="#0b2b56"><b>FATURA</b></font>', estilo_normal),
            logo,
            Paragraph('<b style="font-size:16px">Conference Hub</b>', estilo_normal)
        ]
    ]
    tabela_header = Table(header_data, colWidths=[90*mm, 20*mm, 60*mm])
    tabela_header.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('ALIGN', (2, 0), (2, 0), 'LEFT'),
        ('LEFTPADDING', (1, 0), (1, 0), 5),
    ]))
    elementos.append(tabela_header)
    elementos.append(Spacer(1, 20))

    # Blocos de info
    dados_fatura = [
        [
            Paragraph('<b>Cobrar a:</b><br/>' + inscricao.nome + '<br/>' + inscricao.email + '<br/>NIF: ' + inscricao.nif, estilo_normal),
            Paragraph('<b>Fatura nº:</b> CFH-{:05d}<br/><b>Data:</b> {}<br/><b>Tipo:</b> {}'.format(
                inscricao.id, inscricao.data_inscricao.strftime('%d/%m/%Y'), inscricao.tipo_registo
            ), estilo_normal)
        ]
    ]
    tabela_info = Table(dados_fatura, colWidths=[100*mm, 70*mm])
    tabela_info.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    elementos.append(tabela_info)
    elementos.append(Spacer(1, 20))

    # Tabela de descrição
    dados_tabela = [
        ['QTD', 'DESCRIÇÃO', 'PREÇO', 'TOTAL'],
        ['1', 'Inscrição no evento', '20€', '20€'],
    ]

    tabela = Table(dados_tabela, colWidths=[40*mm, 70*mm, 30*mm, 30*mm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0b2b56")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('TOPPADDING', (0, 0), (-1, 0), 6),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 20))

    # Totais
    elementos.append(Paragraph('<b>Subtotal:</b> 20€', estilo_normal))
    elementos.append(Paragraph('<b>IVA incluído:</b> Sim', estilo_normal))
    elementos.append(Paragraph('<b>Total:</b> 20€', estilo_normal))
    elementos.append(Spacer(1, 30))

    # Rodapé
    rodape_texto = "O pagamento inclui IVA. O reembolso pode ser solicitado até 1 mês antes do evento."
    elementos.append(Paragraph('<font size=10 color="#666666">{}</font>'.format(rodape_texto), estilo_normal))
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph('<font size=14><b>Obrigado!</b></font>', estilo_normal))

    doc.build(elementos)
    buffer.seek(0)
    return buffer
