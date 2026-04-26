"""
Reformata um SRT existente para o estilo:
- 2-3 palavras por legenda
- Tudo em MAIÚSCULO
- Tempos proporcionais ao original
"""

import re

PALAVRAS_POR_LEGENDA = 3

entrada = """1
00:00:00,000 --> 00:00:02,500
Pare de ser viciada em migalha.

2
00:00:02,500 --> 00:00:06,500
Migalha é uma das drogas mais eficientes que o mundo moderno já inventou.

3
00:00:06,500 --> 00:00:12,500
Sim, porque em 2026 ainda tem adulto funcional que não se comunica.

4
00:00:12,500 --> 00:00:14,500
Gerencia presença.

5
00:00:14,500 --> 00:00:19,500
Aparece nos seus stories, deixa um coraçãozinho, some.

6
00:00:19,500 --> 00:00:25,000
Volta com um comentário solto, um emoji, uma reação, um foguinho.

7
00:00:25,000 --> 00:00:28,500
O suficiente pra você lembrar que ele existe.

8
00:00:29,000 --> 00:00:33,000
Mas não o suficiente pra estar de verdade na sua vida.

9
00:00:33,000 --> 00:00:37,500
E isso confunde, porque não é ausência, é quase.

10
00:00:37,500 --> 00:00:43,500
Quase interesse, quase iniciativa, quase vontade de te chamar pra sair.

11
00:00:43,500 --> 00:00:49,500
E o cérebro adora isso, porque a intermitência vicia mais que constância.

12
00:00:49,500 --> 00:00:52,500
Você nunca sabe quando vem, então você espera.

13
00:00:52,500 --> 00:00:57,500
E quando vem, parece muito mais intenso do que realmente é.

14
00:00:57,500 --> 00:01:00,500
Mas vamos ser honestas, não tem muito mistério aqui.

15
00:01:00,500 --> 00:01:03,000
Quem quer te ver, te chama pra sair.

16
00:01:03,000 --> 00:01:05,500
O resto é gestão de ego.

17
00:01:05,500 --> 00:01:09,500
É presença mínima pra não desaparecer.

18
00:01:09,500 --> 00:01:13,500
Só o suficiente pra continuar sendo uma opção sua.

19
00:01:13,500 --> 00:01:19,000
E talvez o mais desconfortável seja realmente admitir que não é que você gosta disso.

20
00:01:19,000 --> 00:01:24,500
É que você se acostumou com o estímulo, com a dinâmica, com o quase.

21
00:01:25,000 --> 00:01:30,000
Mas tesão mesmo é difícil manter por quem se comunica só por like.

22
00:01:30,000 --> 00:01:32,500
Porque migalha não é conexão.

23
00:01:32,500 --> 00:01:35,500
É só o mínimo pra você não ir embora.

24
00:01:35,500 --> 00:01:42,500
E posso falar, quando você parar de deixar ele orbitar a sua vida pra nada, vai perceber que ele nem era tão interessante assim.

25
00:01:42,500 --> 00:01:46,500
Ele só parecia pouco o suficiente pra parecer interessante pra você.

26
00:01:46,500 --> 00:01:50,000
Então lembre-se, você não tá apaixonada.

27
00:01:50,000 --> 00:01:54,000
Você só tá viciada em... migalha."""


def tempo_para_segundos(t):
    h, m, s = t.split(":")
    s, ms = s.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000


def segundos_para_tempo(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int(round((s - int(s)) * 1000))
    return f"{h:02}:{m:02}:{sec:02},{ms:03}"


def reformatar(texto, palavras_por_legenda):
    blocos = re.split(r'\n\n+', texto.strip())
    resultado = []
    contador = 1

    for bloco in blocos:
        linhas = bloco.strip().split('\n')
        if len(linhas) < 3:
            continue
        tempo_linha = linhas[1]
        texto_legenda = ' '.join(linhas[2:])
        inicio_str, fim_str = tempo_linha.split(' --> ')
        inicio = tempo_para_segundos(inicio_str.strip())
        fim = tempo_para_segundos(fim_str.strip())
        duracao = fim - inicio

        palavras = texto_legenda.upper().split()
        total = len(palavras)
        if total == 0:
            continue

        grupos = []
        i = 0
        while i < total:
            grupos.append(palavras[i:i + palavras_por_legenda])
            i += palavras_por_legenda

        tempo_por_grupo = duracao / len(grupos)

        for j, grupo in enumerate(grupos):
            t_inicio = inicio + j * tempo_por_grupo
            t_fim = inicio + (j + 1) * tempo_por_grupo
            resultado.append(f"{contador}\n{segundos_para_tempo(t_inicio)} --> {segundos_para_tempo(t_fim)}\n{' '.join(grupo)}")
            contador += 1

    return "\n\n".join(resultado)


srt_final = reformatar(entrada, PALAVRAS_POR_LEGENDA)

with open("NWDS_04_MIGALHAV1_FORMATADO.srt", "w", encoding="utf-8") as f:
    f.write(srt_final)

print("✓ Arquivo NWDS_04_MIGALHAV1_FORMATADO.srt gerado!")
