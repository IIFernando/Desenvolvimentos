import os
import tempfile
from lxml import etree
from signxml import XMLSigner, methods
import requests
from cryptography.hazmat.primitives.serialization import pkcs12, Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.backends import default_backend

# === CONFIGURAÇÕES ===
PFX_PATH = "G:\\Drives compartilhados\\Finance 2.0\\11. Tax\\Certificados Digitais\\L4B - Certificado\\Ativo\\L4B LOGISTICA LTDA._24217653000195.pfx"
with open("C:\\Python\\Recebimento\\senha_certificado.txt") as f:
    PFX_PASSWORD = f.read().strip()

CNPJ = "24217653000195"
CCM = "54271860"
DATA_INICIO = "2025-07-01"
DATA_FIM = "2025-07-14"
NUMERO_PAGINA = 1

# === CONVERTE PFX PARA PEM TEMPORÁRIO ===
def converter_pfx_para_pem(pfx_path, password):
    with open(pfx_path, "rb") as f:
        pfx_data = f.read()

    private_key, cert, additional_certs = pkcs12.load_key_and_certificates(
        data=pfx_data,
        password=password.encode(),
        backend=default_backend()
    )

    key_pem = private_key.private_bytes(
        Encoding.PEM,
        PrivateFormat.PKCS8,
        NoEncryption()
    )

    cert_pem = cert.public_bytes(Encoding.PEM)

    if additional_certs:
        for ca in additional_certs:
            cert_pem += ca.public_bytes(Encoding.PEM)

    return key_pem, cert_pem

# === MONTA XML ===
def montar_xml(cnpj, ccm, dt_inicio, dt_fim, pagina):
    root = etree.Element("PedidoConsultaNFeRecebidas", Versao="1")
    etree.SubElement(root, "CPFCNPJRemetente").text = cnpj
    etree.SubElement(root, "CPFCNPJ").text = cnpj
    etree.SubElement(root, "InscricaoMunicipal").text = ccm
    etree.SubElement(root, "dtInicio").text = dt_inicio
    etree.SubElement(root, "dtFim").text = dt_fim
    etree.SubElement(root, "NumeroPagina").text = str(pagina)
    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")

# === ASSINA XML ===
def assinar_xml(xml_bytes, key_pem, cert_pem):
    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha1",
        digest_algorithm="sha1",
        allow_legacy=True  # <- CORRETO na versão 4.x
    )

    doc = etree.fromstring(xml_bytes)
    signed = signer.sign(doc, key=key_pem, cert=cert_pem)
    signed_xml = etree.tostring(signed, pretty_print=True, xml_declaration=True, encoding="utf-8")

    # Salva o XML assinado para validação
    with open("xml_assinado.xml", "wb") as f:
        f.write(signed_xml)
    print("\n[INFO] XML assinado salvo em 'xml_assinado.xml' para validação.")

    return signed_xml

# === ENVIA REQUISIÇÃO E TRATA RESPOSTA ===
def enviar_requisicao(xml_assinado, cert_path, key_path):
    envelope = f"""<?xml version="1.0" encoding="utf-8"?>
    <soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                     xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                     xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
      <soap12:Body>
        <ConsultaNFeRecebidas xmlns="http://www.prefeitura.sp.gov.br/nfe">
          <VersaoSchema>1</VersaoSchema>
          <MensagemXML><![CDATA[{xml_assinado.decode("utf-8")}]]></MensagemXML>
        </ConsultaNFeRecebidas>
      </soap12:Body>
    </soap12:Envelope>"""

    url = "https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx"
    headers = {
        "Content-Type": "application/soap+xml; charset=utf-8"
    }

    try:
        response = requests.post(
            url,
            data=envelope.encode("utf-8"),
            headers=headers,
            cert=(cert_path, key_path),
            verify=True
        )

        print("\n=== Status Code ===")
        print(response.status_code)

        print("\n=== Resposta Bruta ===")
        print(response.content.decode("utf-8", errors="replace"))

        with open("resposta_raw.txt", "w", encoding="utf-8") as f:
            f.write(response.text)

        tratar_resposta(response.content)

    except Exception as e:
        print(f"\n[ERRO na requisição HTTPS]: {e}")

# === TRATA A RESPOSTA DO SERVIÇO ===
def tratar_resposta(xml_soap):
    try:
        if not xml_soap.strip().startswith(b"<"):
            print("\n[ERRO] Resposta não é XML. Veja o conteúdo salvo em 'resposta_raw.txt'.")
            return

        namespaces = {
            "soap": "http://www.w3.org/2003/05/soap-envelope",
            "ns": "http://www.prefeitura.sp.gov.br/nfe"
        }

        tree = etree.fromstring(xml_soap)
        body = tree.find(".//soap:Body", namespaces)
        if body is None:
            print("\n[ERRO] Corpo da resposta SOAP não encontrado.")
            return

        fault = body.find(".//soap:Fault", namespaces)
        if fault is not None:
            fault_code = fault.findtext("soap:Code")
            fault_reason = fault.findtext("soap:Reason")
            print(f"\n[ERRO SOAP] Código: {fault_code}\nMotivo: {fault_reason}")
            return

        result = body.find(".//ns:ConsultaNFeRecebidasResult", namespaces)
        if result is None or result.text is None:
            print("\n[AVISO] Nenhum resultado encontrado.")
            return

        retorno_xml = result.text.strip()
        print("\n=== XML de Resposta Decodificado ===")
        print(retorno_xml)

        try:
            xml_notas = etree.fromstring(retorno_xml.encode("utf-8"))
            notas = xml_notas.findall(".//NFe")
            print(f"\n=== {len(notas)} nota(s) fiscal(is) encontrada(s) ===")
            for i, nota in enumerate(notas, 1):
                print(f"\n--- Nota {i} ---")
                print(etree.tostring(nota, pretty_print=True).decode("utf-8"))
        except Exception as e:
            print(f"\n[ERRO ao interpretar o XML de retorno]: {e}")

    except Exception as e:
        print(f"\n[ERRO ao tratar resposta SOAP]: {e}")

# === EXECUÇÃO PRINCIPAL ===
key_pem, cert_pem = converter_pfx_para_pem(PFX_PATH, PFX_PASSWORD)
xml = montar_xml(CNPJ, CCM, DATA_INICIO, DATA_FIM, NUMERO_PAGINA)
xml_assinado = assinar_xml(xml, key_pem, cert_pem)

temp_key_file = tempfile.NamedTemporaryFile(delete=False, mode="wb")
temp_cert_file = tempfile.NamedTemporaryFile(delete=False, mode="wb")

try:
    temp_key_file.write(key_pem)
    temp_cert_file.write(cert_pem)
    temp_key_file.close()
    temp_cert_file.close()

    enviar_requisicao(xml_assinado, temp_cert_file.name, temp_key_file.name)

finally:
    os.unlink(temp_key_file.name)
    os.unlink(temp_cert_file.name)
