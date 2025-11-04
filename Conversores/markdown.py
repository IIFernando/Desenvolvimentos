from markitdown import MarkItDown

lcp214 = '/home/fernandoaraujo_logg/Desenvolvimentos/Conversores/arquivos/LCP214.pdf'

md = MarkItDown(enable_plugins=True)
result = md.convert(lcp214)

#Salva o resultado em um arquivo .md chamado LCP214.md e em UTF-8
with open(f'/home/fernandoaraujo_logg/Desenvolvimentos/ADK/markdowns/LC214.md', 'w', encoding='utf-8') as file:
    file.write(result.markdown)
print("Arquivo LCP214.md salvo com sucesso!")
