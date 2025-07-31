import os
from lxml import etree
from signxml import XMLSigner, methods
from zeep import Client
from zeep.transports import Transport
from requests import Session
from requests_pkcs12 import Pkcs12Adapter
from dotenv import load_dotenv
from cryptography.hazmat.primitives.serialization import pkcs12

# Carrega variáveis do .env
load_dotenv()
pfx_path = "C:\\Python\\Ativo\\24217653000195.pfx"
pfx_password = os.getenv("PFX_PASSWORD")

def gerar_xml_nfts():
    root = etree.Element("PedidoEnvioNFTS", Versao="1")
    cabecalho = etree.SubElement(root, "Cabecalho", Versao="1")
    remetente = etree.SubElement(cabecalho, "Remetente")
    cpfcnpj = etree.SubElement(remetente, "CPFCNPJ")
    etree.SubElement(cpfcnpj, "CNPJ").text = "24217653000195"

    nfts = etree.SubElement(root, "NFTS")
    etree.SubElement(nfts, "TipoDocumento").text = "2"

    chave = etree.SubElement(nfts, "ChaveDocumento")
    etree.SubElement(chave, "InscricaoMunicipal").text = "12345678"
    etree.SubElement(chave, "SerieNFTS").text = "E"
    etree.SubElement(chave, "NumeroDocumento").text = "13"

    etree.SubElement(nfts, "DataPrestacao").text = "2025-05-06T00:00:00"
    etree.SubElement(nfts, "StatusNFTS").text = "N"
    etree.SubElement(nfts, "TributacaoNFTS").text = "T"
    etree.SubElement(nfts, "ValorServicos").text = "48.50"
    etree.SubElement(nfts, "ValorDeducoes").text = "0.00"
    etree.SubElement(nfts, "CodigoServico").text = "1104"
    etree.SubElement(nfts, "AliquotaServicos").text = "0.05"
    etree.SubElement(nfts, "ISSRetidoTomador").text = "false"

    prestador = etree.SubElement(nfts, "Prestador")
    etree.SubElement(etree.SubElement(prestador, "CPFCNPJ"), "CNPJ").text = "24039270000174"

    etree.SubElement(nfts, "RegimeTributacao").text = "0"
    etree.SubElement(nfts, "Discriminacao").text = (
        "Serviços prestados no período de 01/04/2025 a 15/04/2025. Pedido: 4800016476"
    )
    etree.SubElement(nfts, "TipoNFTS").text = "1"

    tomador = etree.SubElement(nfts, "Tomador")
    etree.SubElement(etree.SubElement(tomador, "CPFCNPJ"), "CNPJ").text = "24217653000195"
    etree.SubElement(tomador, "RazaoSocial").text = "L4B LOGISTICA LTDA."

    etree.SubElement(nfts, "Assinatura").text = ""

    return etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True)

def assinar_xml(xml_bytes, pfx_path, pfx_password):
    with open(pfx_path, "rb") as f:
        pfx_data = f.read()

    private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
        pfx_data, pfx_password.encode()
    )

    signer = XMLSigner(
        method=methods.enveloped,
        signature_algorithm="rsa-sha256",
        digest_algorithm="sha256"
        # Se precisar usar SHA1, adicione allow_weak_hashes=True (não recomendado)
    )

    cert_chain = [certificate]
    if additional_certificates:
        cert_chain.extend(additional_certificates)

    signed = signer.sign(
        etree.fromstring(xml_bytes),
        key=private_key,
        cert=cert_chain
    )

    return etree.tostring(signed, pretty_print=True, encoding="utf-8", xml_declaration=True)

def enviar_nfts(xml_assinado, pfx_path, pfx_password):
    session = Session()
    session.mount("https://", Pkcs12Adapter(pkcs12_filename=pfx_path, pkcs12_password=pfx_password))
    transport = Transport(session=session)
    client = Client("https://nfe.prefeitura.sp.gov.br/ws/LoteNFTS.asmx?WSDL", transport=transport)
    versao_schema = 1
    xml_string = xml_assinado.decode("utf-8")
    resultado = client.service.EnvioNFTS(versao_schema, xml_string)
    return resultado

if __name__ == "__main__":
    import sys

    if not pfx_path or not pfx_password:
        print("Variáveis de ambiente PFX_PATH ou PFX_PASSWORD não definidas.")
        sys.exit(1)

    if not os.path.isfile(pfx_path):
        print(f"Arquivo .pfx não encontrado no caminho: {pfx_path}")
        sys.exit(1)

    xml = gerar_xml_nfts()
    xml_assinado = assinar_xml(xml, pfx_path, pfx_password)

    with open("xml_assinado_para_envio.xml", "wb") as f:
        f.write(xml_assinado)
    print("✅ XML Assinado salvo em xml_assinado_para_envio.xml")

    resultado = enviar_nfts(xml_assinado, pfx_path, pfx_password)
    print("📨 Resposta do WebService:")
    print(resultado)
