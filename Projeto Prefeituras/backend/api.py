from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import io
import sys

# Adiciona o diretório raiz do projeto ao PYTHONPATH
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from modules.saoPaulo import nfts_SP
from modules.cajamar import nfts_Cajamar
from modules.recife import nfts_Recife

app = FastAPI(
    title="API Prefeituras",
    description="API para geração de arquivos NFTs",
    version="0.1.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:8080"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para Recife
@app.post("/recife/")
async def gerar_txt_recife(
    template_file: UploadFile = File(...),
    dtinicio: str = Form(...),
    dtfim: str = Form(...),
    inMunicipal: str = Form(...),
    cnpj: str = Form(...),
):
    temp_file_path = f"temp_{template_file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await template_file.read())
    try:
        content = nfts_Recife(temp_file_path, dtinicio, dtfim, inMunicipal, cnpj)
        if not content:
            return {"erro": "Arquivo não foi gerado."}
        output_filename = f"recife.txt"
        return StreamingResponse(
            io.StringIO(content),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )
    except Exception as e:
        return {"erro": str(e)}
    finally:
        os.remove(temp_file_path)

@app.post("/sao-paulo/")
async def gerar_txt_sao_paulo(
    template_file: UploadFile = File(...),
    dtint: str = Form(...),
    dtfim: str = Form(...),
    inMunicipal: str = Form(...),
    filial: str = Form(...)
):
    temp_file_path = f"temp_{template_file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await template_file.read())
    try:
        content = nfts_SP(temp_file_path, dtint, dtfim, inMunicipal)
        if not content:
            return {"erro": "Arquivo não foi gerado."}
        output_filename = f"sao_paulo_{filial}.txt"
        return StreamingResponse(
            io.StringIO(content),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )
    except Exception as e:
        return {"erro": str(e)}
    finally:
        os.remove(temp_file_path)

@app.post("/cajamar/")
async def gerar_txt_cajamar(
    template_file: UploadFile = File(...),
    data: str = Form(...),
    cnpj: str = Form(...),
    filial: str = Form(...)
):
    temp_file_path = f"temp_{template_file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await template_file.read())
    try:
        content = nfts_Cajamar(temp_file_path, data, cnpj)
        if not content:
            return {"erro": "Arquivo não foi gerado."}
        output_filename = f"cajamar_{filial}.txt"
        return StreamingResponse(
            io.StringIO(content),
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={output_filename}"}
        )
    except Exception as e:
        return {"erro": str(e)}
    finally:
        os.remove(temp_file_path)
