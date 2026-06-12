from datetime import datetime
from decimal import Decimal
import re

from django.core.exceptions import ValidationError

from app.models import TipoEstagio


class PDFExtractionError(ValidationError):
    pass


def extrair_texto_pdf(arquivo):
    try:
        arquivo.seek(0)
    except Exception:
        pass

    try:
        import pdfplumber

        with pdfplumber.open(arquivo) as pdf:
            texto = '\n'.join(page.extract_text() or '' for page in pdf.pages)
    except Exception as exc:
        raise PDFExtractionError('PDF corrompido ou ilegivel.') from exc
    finally:
        try:
            arquivo.seek(0)
        except Exception:
            pass

    if not texto.strip():
        raise PDFExtractionError('PDF sem texto extraivel para analise automatica.')

    return texto


def extrair_dados_do_texto(texto):
    texto = texto or ''
    dados = {
        'cpf': _buscar_regex(texto, r'\bcpf[:\s]*([0-9\.\-]+)'),
        'cnpj': _buscar_regex(texto, r'\bcnpj[:\s]*([0-9\./\-]+)'),
        'curso': _buscar_regex(texto, r'\bcurso[:\s]*([^\n]+)'),
        'tipo_estagio': _parse_tipo_estagio(_buscar_regex(texto, r'\btipo\s+de\s+estagi[oó][:\s]*([^\n]+)')),
        'data_inicio': _parse_data(_buscar_regex(texto, r'\bdata(?:\s+de)?\s+in[ií]cio[:\s]*([0-9/\-]+)')),
        'data_fim': _parse_data(_buscar_regex(texto, r'\bdata(?:\s+de)?\s+fim[:\s]*([0-9/\-]+)')),
        'carga_horaria_diaria': _parse_decimal(_buscar_regex(texto, r'\bcarga\s+hor[aá]ria\s+di[aá]ria[:\s]*([0-9\.,]+)')),
        'carga_horaria_semanal': _parse_decimal(_buscar_regex(texto, r'\bcarga\s+hor[aá]ria\s+semanal[:\s]*([0-9\.,]+)')),
        'seguro_apolice': _buscar_regex(texto, r'\bseguro(?:\s+ap[oó]lice)?[:\s]*([^\n]+)'),
        'supervisor_nome': _buscar_regex(texto, r'\bsupervisor(?:\s+nome)?[:\s]*([^\n]+)'),
        'professor_orientador': _buscar_regex(texto, r'\bprofessor\s+orientador[:\s]*([^\n]+)'),
        'bolsa_auxilio': _parse_decimal(_buscar_regex(texto, r'\bbolsa(?:\s+aux[ií]lio)?[:\s]*([0-9\.,]+)')),
        'auxilio_transporte': _parse_bool(_buscar_regex(texto, r'\baux[ií]lio(?:\s+transporte)?[:\s]*(sim|nao|não|true|false|1|0)')),
        'atividades': _buscar_regex(texto, r'\batividades[:\s]*([^\n]+)'),
        'plano_atividades': _buscar_regex(texto, r'\bplano\s+de\s+atividades[:\s]*([^\n]+)'),
    }
    return {k: v for k, v in dados.items() if v is not None}


def extrair_dados_pdf(arquivo):
    texto = extrair_texto_pdf(arquivo)
    dados = extrair_dados_do_texto(texto)
    if not dados:
        raise PDFExtractionError('PDF legivel, mas sem dados minimos reconhecidos para analise.')
    return dados


def _buscar_regex(texto, padrao):
    match = re.search(padrao, texto, flags=re.I | re.M)
    return match.group(1).strip() if match else None


def _parse_data(valor):
    if not valor:
        return None
    valor = valor.strip().replace(' ', '')
    for fmt in ('%d/%m/%Y', '%d/%m/%y', '%Y-%m-%d'):
        try:
            return datetime.strptime(valor, fmt).date()
        except ValueError:
            continue
    return None


def _parse_decimal(valor):
    if not valor:
        return None
    normalized = valor.replace('.', '').replace(',', '.')
    try:
        return Decimal(normalized)
    except Exception:
        return None


def _parse_bool(valor):
    if not valor:
        return None
    valor = valor.strip().lower()
    if valor in ('sim', 's', 'true', 'verdadeiro', '1'):
        return True
    if valor in ('nao', 'não', 'n', 'false', 'f', '0'):
        return False
    return None


def _parse_tipo_estagio(valor):
    if not valor:
        return None
    texto = valor.strip().lower()
    if 'nao' in texto or 'não' in texto:
        return TipoEstagio.NAO_OBRIGATORIO
    if 'obrig' in texto:
        return TipoEstagio.OBRIGATORIO
    return None
