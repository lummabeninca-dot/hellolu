-- Script Lua para DaVinci Resolve
-- Cria legendas Text+ na timeline a partir do SRT formatado

local srt_path = "/Users/lumabeninca/Documents/NWDS_MIGALHA/NWDS_04_MIGALHAV1_FORMATADO.srt"
local fonte = "Helvetica"
local estilo = "Bold"
local tamanho = 0.08

-- Lê o arquivo SRT
local function ler_arquivo(caminho)
    local f = io.open(caminho, "r")
    if not f then
        print("ERRO: Arquivo não encontrado em " .. caminho)
        return nil
    end
    local conteudo = f:read("*all")
    f:close()
    return conteudo
end

-- Converte tempo SRT (00:00:00,000) para segundos
local function tempo_para_segundos(t)
    local h, m, s, ms = t:match("(%d+):(%d+):(%d+),(%d+)")
    return tonumber(h)*3600 + tonumber(m)*60 + tonumber(s) + tonumber(ms)/1000
end

-- Parseia o SRT e retorna lista de legendas
local function parsear_srt(conteudo)
    local legendas = {}
    for bloco in (conteudo .. "\n\n"):gmatch("(.-)\n\n") do
        local linhas = {}
        for linha in bloco:gmatch("[^\n]+") do
            table.insert(linhas, linha)
        end
        if #linhas >= 3 then
            local inicio_str, fim_str = linhas[2]:match("(.+) %-%-> (.+)")
            if inicio_str and fim_str then
                local texto = ""
                for i = 3, #linhas do
                    texto = texto .. linhas[i]
                end
                table.insert(legendas, {
                    inicio = tempo_para_segundos(inicio_str),
                    fim = tempo_para_segundos(fim_str),
                    texto = texto:upper()
                })
            end
        end
    end
    return legendas
end

-- Conecta ao DaVinci
local resolve = Resolve()
local pm = resolve:GetProjectManager()
local projeto = pm:GetCurrentProject()
local timeline = projeto:GetCurrentTimeline()
local fps = tonumber(projeto:GetSetting("timelineFrameRate"))
local media_pool = projeto:GetMediaPool()

print("Conectado ao projeto: " .. projeto:GetName())
print("FPS: " .. fps)

local conteudo = ler_arquivo(srt_path)
if not conteudo then return end

local legendas = parsear_srt(conteudo)
print("Legendas encontradas: " .. #legendas)

local criadas = 0
for _, leg in ipairs(legendas) do
    local inicio_frame = math.floor(leg.inicio * fps)
    local fim_frame = math.floor(leg.fim * fps)
    local duracao = fim_frame - inicio_frame

    if duracao > 0 then
        local item = media_pool:AppendToTimeline({
            {
                ["mediaType"] = "Fusion Title",
                ["startFrame"] = 0,
                ["endFrame"] = duracao,
            }
        })

        if item and #item > 0 then
            local clip = item[1]
            local comp = clip:GetFusionCompByIndex(1)
            if comp then
                local text_node = comp:FindToolByID("TextPlus")
                if text_node then
                    text_node.StyledText[TIME_UNDEFINED] = leg.texto
                    text_node.Font[TIME_UNDEFINED] = fonte
                    text_node.Style[TIME_UNDEFINED] = estilo
                    text_node.Size[TIME_UNDEFINED] = tamanho
                end
            end
            criadas = criadas + 1
        end
    end
end

print("✓ " .. criadas .. " legendas Text+ criadas!")
