#!/usr/bin/env python3
"""
Script para rodar no console do DaVinci Resolve.
Cria clipes Text+ na timeline a partir do SRT formatado.

COMO USAR:
1. Abra o DaVinci Resolve
2. Abra o projeto nowdays_04
3. Vá em: Workspace > Console
4. Cole todo esse código e aperte Enter
"""

import re

SRT_PATH = "/Users/lumabeninca/Documents/NWDS_MIGALHA/NWDS_04_MIGALHAV1_FORMATADO.srt"
FONTE = "Helvetica"
ESTILO = "Bold"
TAMANHO = 0.08  # Ajuste entre 0.05 e 0.12 conforme precisar
COR = [1, 1, 1, 1]  # Branco


def tempo_para_frames(tempo_str, fps=24):
    h, m, s = tempo_str.split(":")
    s, ms = s.split(",")
    total_segundos = int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    return int(total_segundos * fps)


def ler_srt(caminho):
    with open(caminho, "r", encoding="utf-8") as f:
        conteudo = f.read()

    blocos = re.split(r'\n\n+', conteudo.strip())
    legendas = []

    for bloco in blocos:
        linhas = bloco.strip().split('\n')
        if len(linhas) < 3:
            continue
        inicio_str, fim_str = linhas[1].split(' --> ')
        texto = ' '.join(linhas[2:])
        legendas.append({
            'inicio': tempo_para_frames(inicio_str.strip()),
            'fim': tempo_para_frames(fim_str.strip()),
            'texto': texto.upper()
        })

    return legendas


# Conecta ao DaVinci Resolve
resolve = bmd.scriptapp("Resolve")
pm = resolve.GetProjectManager()
projeto = pm.GetCurrentProject()
timeline = projeto.GetCurrentTimeline()
fps = int(projeto.GetSetting("timelineFrameRate"))
media_pool = projeto.GetMediaPool()

legendas = ler_srt(SRT_PATH)
criadas = 0

for leg in legendas:
    clip_info = {
        "startFrame": leg['inicio'],
        "endFrame": leg['fim'],
        "mediaType": "Fusion Title",
        "mediaPoolItem": None
    }

    # Adiciona Text+ na track de vídeo 2
    item = timeline.InsertFusionTitleIntoTimeline("Text+")

    if item:
        comp = item.GetFusionCompByIndex(1)
        if comp:
            text_node = comp.FindToolByID("TextPlus")
            if text_node:
                text_node.StyledText[1] = leg['texto']
                text_node.Font[1] = FONTE
                text_node.Style[1] = ESTILO
                text_node.Size[1] = TAMANHO
                text_node.Red1[1] = COR[0]
                text_node.Green1[1] = COR[1]
                text_node.Blue1[1] = COR[2]
        criadas += 1

print(f"✓ {criadas} legendas Text+ criadas na timeline!")
