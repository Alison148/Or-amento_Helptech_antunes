from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, PositiveFloat
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pathlib import Path
from datetime import datetime
import tempfile, os, shutil

app = FastAPI(title="HelpTech Antunes - Orçamentos")

# --- Helpers --------------------------------------------------------------

def brl(v: float) -> str:
    """Formata número no padrão brasileiro de moeda."""
    return ("R$ " + f"{v:,.2f}").replace(",", "X").replace(".", ",").replace("X", ".")

def cleanup(path: str):
    """Remove o PDF e a pasta temporária após o envio."""
    try:
        p = Path(path)
        if p.exists():
            p.unlink(missing_ok=True)
        # remove também o diretório temporário criado
        shutil.rmtree(p.parent.as_posix(), ignore_errors=True)
    except Exception:
        pass

def gerar_pdf_arquivo(dados: dict) -> str:
    """Gera o PDF em arquivo temporário e retorna o caminho."""
    tmp_dir = tempfile.mkdtemp(prefix="helptech_")
    numero = dados.get("numero") or datetime.now().strftime("%Y%m%d%H%M")
    file_path = os.path.join(tmp_dir, f"orcamento-{numero}.pdf")

    c = canvas.Canvas(file_path, pagesize=A4)
    w, h = A4
    left = 20 * mm
    right = w - 20 * mm
    y = h - 20 * mm

    # Título
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.18, 0.49, 0.20)  # verde
    c.drawString(left, y, "Orçamento - HelpTech Antunes")

    # Meta
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)
    c.drawString(left, y - 8 * mm, f"Nº: {numero}")
    c.drawRightString(right, y - 8 * mm, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    c.line(left, y - 10 * mm, right, y - 10 * mm)
    y -= 18 * mm

    # Cliente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left, y, "Cliente")
    c.setFont("Helvetica", 10)
    c.drawString(left, y - 5 * mm, f"Nome: {dados['cliente']}")
    if dados.get("contato"):
        c.drawString(left, y - 10 * mm, f"Contato: {dados['contato']}")
    y -= 18 * mm

    # Serviço
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left, y, "Serviço")
    c.setFont("Helvetica", 10)
    c.drawString(left, y - 5 * mm, dados["servico"])
    y -= 12 * mm

    # Valor
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left, y, "Valor")
    c.setFont("Helvetica", 11)
    c.drawString(left, y - 5 * mm, brl(dados["valor"]))
    y -= 14 * mm

    # Observações (quebra simples por linha)
    obs = dados.get("observacoes")
    if obs:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(left, y, "Observações")
        c.setFont("Helvetica", 10)
        text = c.beginText(left, y - 6 * mm)
        text.setLeading(14)
        for line in obs.splitlines():
            text.textLine(line)
        c.drawText(text)
        y -= (6 * mm + 14 * max(1, len(obs.splitlines())))

    # Rodapé
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(left, 15 * mm, "Gerado automaticamente pelo sistema HelpTech.")
    c.showPage()
    c.save()
    return file_path

# --- Schemas -------------------------------------------------------------

class Orcamento(BaseModel):
    cliente: str = Field(..., description="Nome do cliente")
    servico: str = Field(..., description="Descrição do serviço")
    valor: PositiveFloat = Field(..., description="Valor do serviço em BRL")
    contato: str | None = Field(None, description="Telefone/WhatsApp ou e-mail")
    numero: str | None = Field(None, description="Número do orçamento")
    observacoes: str | None = Field(None, description="Observações adicionais")

# --- Rotas ---------------------------------------------------------------

@app.get("/")
def home():
    return {"message": "API HelpTech Antunes rodando com FastAPI + PDF"}

@app.post("/gerar-pdf", response_class=FileResponse)
def gerar_pdf(orc: Orcamento, background_tasks: BackgroundTasks):
    path = gerar_pdf_arquivo(orc.model_dump())
    filename = Path(path).name
    # agenda limpeza após a resposta ser enviada
    background_tasks.add_task(cleanup, path)
    return FileResponse(path, media_type="application/pdf", filename=filename)

# Opcional: manter compatibilidade via GET (parâmetros querystring)
@app.get("/gerar-pdf")
def gerar_pdf_get(
    cliente: str = "Cliente Teste",
    servico: str = "Serviço X",
    valor: float = 100.0,
    contato: str | None = None,
    numero: str | None = None,
    observacoes: str | None = None,
    background_tasks: BackgroundTasks = None,
):
    orc = Orcamento(cliente=cliente, servico=servico, valor=valor,
                    contato=contato, numero=numero, observacoes=observacoes)
    path = gerar_pdf_arquivo(orc.model_dump())
    filename = Path(path).name
    if background_tasks:
        background_tasks.add_task(cleanup, path)
    return FileResponse(path, media_type="application/pdf", filename=filename)
