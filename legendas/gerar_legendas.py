"""
GERADOR DE LEGENDAS - Estilo dinâmico 2-3 palavras, maiúsculo
Para importar no DaVinci Resolve como arquivo .srt

COMO USAR:
1. Cole o texto do vídeo na variável TRANSCRICAO abaixo
2. Rode o script: python gerar_legendas.py
3. O arquivo legendas.srt será gerado nesta pasta
4. No DaVinci: File > Import > Subtitles > selecione o arquivo
5. Ajuste a fonte para Helvetica Bold nas configurações de legenda
"""

TRANSCRICAO = """
Cole aqui o texto falado no vídeo.
Pode ser um parágrafo longo, o script vai quebrar tudo automaticamente.
"""

# Quantas palavras por legenda (2 ou 3)
PALAVRAS_POR_LEGENDA = 3

# Duração de cada legenda em segundos
DURACAO_POR_LEGENDA = 0.8


def formatar_tempo(segundos):
    h = int(segundos // 3600)
    m = int((segundos % 3600) // 60)
    s = int(segundos % 60)
    ms = int((segundos - int(segundos)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def gerar_srt(texto, palavras_por_legenda, duracao):
    palavras = texto.upper().split()
    legendas = []
    tempo = 0.0
    contador = 1

    i = 0
    while i < len(palavras):
        grupo = palavras[i:i + palavras_por_legenda]
        inicio = formatar_tempo(tempo)
        fim = formatar_tempo(tempo + duracao)
        legendas.append(f"{contador}\n{inicio} --> {fim}\n{' '.join(grupo)}\n")
        tempo += duracao
        contador += 1
        i += palavras_por_legenda

    return "\n".join(legendas)


srt = gerar_srt(TRANSCRICAO.strip(), PALAVRAS_POR_LEGENDA, DURACAO_POR_LEGENDA)

with open("legendas.srt", "w", encoding="utf-8") as f:
    f.write(srt)

print("✓ Arquivo legendas.srt gerado com sucesso!")
print(f"  Total de legendas: {srt.count(chr(10)+chr(10)) + 1}")
