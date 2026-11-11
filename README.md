# Luminescent Platinum - Playthrough & Encounter Tracker

Rastreador de encontros e progresso de playthrough para **Pokémon Luminescent Platinum**. Permite consultar Pokémon por rota/localização (na ordem da campanha), método de encontro, período do dia e controlar quais espécies já foram capturadas.

## Funcionalidades

- **Filtro por ordem de progressão**: rotas ordenadas em `ordered_locations.json` combinadas com a base `luminescent_encounters.json`.
- **Modo "Disponível Agora"**: filtra automaticamente os encontros considerando o horário atual do sistema (Manhã, Dia ou Noite), a rota selecionada e ocultando Pokémon já capturados.
- **Progresso persistente**: salva as capturas e preferências no `localStorage` (em `%APPDATA%\LumiTracker` no modo desktop), com suporte a **Backup / Importação JSON**.
- **Modo Desktop ou Navegador**: executa em janela nativa via `pywebview` (`app.py`) ou em servidor HTTP local de contingência (`server.py`).

## Pré-requisitos

- **Python 3.10+**
- **Microsoft Edge WebView2** (já presente por padrão no Windows 10/11, necessário para o `pywebview` no modo desktop).
- **Conexão com a internet**: a interface em `index.html` carrega o Tailwind CSS via CDN (`cdn.tailwindcss.com`) e sprites via Pokémon Showdown / PokéAPI.

## Como Executar

### 1. Instalar dependências

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Iniciar o aplicativo

* **App Desktop (recomendado):**
  ```bash
  python app.py
  ```
  Ou clique duas vezes em `iniciar_app.bat` (que detecta `.venv` / `venv`, instala o `pywebview` se faltar e usa `server.py` caso o modo desktop falhe).

* **Servidor Web Local (navegador padrão):**
  ```bash
  python server.py
  ```
  Ou execute `iniciar_servidor.bat`.

## Compilação do Executável (`.exe`)

Para gerar o executável único (`dist/LuminescentTracker.exe`) no Windows:

```bash
pip install -r requirements-dev.txt
python build_exe.py
```

Ou execute `compilar_exe.bat`.

> As compilações oficiais também são geradas automaticamente pelo GitHub Actions na aba **Releases** sempre que uma tag `v*` é publicada.

## Atualização da Base de Encontros

Os arquivos `luminescent_encounters.json` e `ordered_locations.json` já estão prontos para uso. Caso queira reprocessar os dados a partir do projeto oficial [TeamLumi/luminescent-team](https://github.com/TeamLumi/luminescent-team):

1. Clone o repositório de origem dentro da pasta `lumi-repo`:
   ```bash
   git clone https://github.com/TeamLumi/luminescent-team lumi-repo
   ```
2. Execute o extrator:
   ```bash
   python parse_encounters.py
   ```

## Estrutura do Projeto

- `app.py`: lançador desktop nativo usando `pywebview`.
- `server.py`: servidor HTTP local de contingência (`localhost:8000+`).
- `index.html`: interface web e lógica do tracker.
- `luminescent_encounters.json`: base normalizada de encontros.
- `ordered_locations.json`: lista ordenada de locais da campanha.
- `parse_encounters.py`: script para extrair e normalizar dados de `lumi-repo/`.
- `build_exe.py`: empacotador PyInstaller para Windows.
- `iniciar_app.bat`, `iniciar_servidor.bat`, `compilar_exe.bat`: atalhos para Windows.

## Créditos

- Dados de encontros e localizações baseados no projeto [Luminescent Platinum (TeamLumi/luminescent-team)](https://github.com/TeamLumi/luminescent-team).
- Sprites carregados via [Pokémon Showdown](https://play.pokemonshowdown.com/sprites/) e [PokéAPI](https://github.com/PokeAPI/sprites).

