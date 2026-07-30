# Hermes Fork Baseline

## Status

`INDEPENDENT_REVIEW_APPROVED`

Data da validação: 2026-07-29

## Identificação

- Fork: `Saaimingo/hermes-agent`
- Upstream: `NousResearch/hermes-agent`
- Branch: `chore/harness-hermes-baseline`
- Commit-base congelado: `71e7eb3c168a49fdd3179efb8a921ad78f6e8e1d`
- Commit observado posteriormente em `upstream/main`: `cff9728587da4f3c0beed0786f9bea528e489f13`
- O avanço do upstream não foi incorporado ao baseline.

## Objetivo

Preservar e validar uma base upstream exata antes de qualquer alteração específica do Harness Cognitivo.

Este baseline não inclui:

- integração com o MEC;
- localização para português do Brasil;
- alterações de arquitetura;
- atualizações de dependências;
- correções de código upstream;
- merge, tag ou release.

## Ambiente Linux de validação utilizado

- WSL2
- Ubuntu 24.04 LTS
- Python 3.11.15
- uv 0.12.0
- Node.js 22.23.2
- npm 10.9.8
- Git 2.43.0
- Git LFS 3.4.1
- GitHub CLI 2.45.0

Checkout Linux:

`/home/saimon/Projects/hermes-agent`

## Instalação

Dependências Python:

`uv sync --locked --python 3.11 --extra all --extra dev`

Resultado:

- ambiente criado em `.venv`;
- pacotes compatíveis;
- importações resolvidas a partir do checkout;
- código de saída 0.

Dependências JavaScript:

`npm ci`

Resultado:

- 1.312 pacotes adicionados;
- código de saída 0;
- nenhuma modificação no repositório.

O npm relatou 28 vulnerabilidades no grafo congelado:

- 1 baixa;
- 26 altas;
- 1 crítica.

Nenhum `npm audit fix`, atualização forçada ou alteração do lockfile foi executado.

## Validações JavaScript e TypeScript

Comando:

`npm run check`

Resultado:

- TypeScript typecheck aprovado;
- 3 arquivos de teste aprovados;
- 9 testes aprovados;
- lint com 25 avisos e zero erros;
- código de saída 0.

Os avisos existentes foram preservados como características do baseline upstream.

## Validações Python

### Ruff

Comando:

`uv run ruff check .`

Resultado:

- todos os checks aprovados;
- código de saída 0;
- aviso não bloqueante sobre diretiva `noqa` em `run_agent.py`.

### Windows footguns

Comando:

`uv run python scripts/check-windows-footguns.py --all`

Resultado:

- 830 arquivos examinados;
- nenhuma armadilha Windows encontrada;
- código de saída 0.

## Suíte Python completa

Comando principal:

`scripts/run_tests.sh`

A execução inicial reportou:

- 5 testes falhos;
- 2 arquivos sem conclusão;
- código de saída 1.

A investigação direcionada demonstrou que não havia falha funcional confirmada no baseline.

### Computer Use overlay

Arquivo:

`tests/computer_use/test_cua_no_overlay.py`

Resultado:

- 19 testes aprovados;
- 2 falhas.

Classificação:

`WSL_ENVIRONMENT_LEAKAGE`

Os testes simulam Linux desktop alterando `sys.platform` e `DISPLAY`, mas não simulam `/proc/version`. Dentro do WSL, a implementação encontra `microsoft` em `/proc/version` e aplica corretamente a política de WSL.

Nenhuma alteração foi realizada.

### Voice mode

Arquivo:

`tests/tools/test_voice_mode.py`

Resultado:

- 80 testes aprovados;
- 3 falhas.

Classificação:

`WSL_ENVIRONMENT_LEAKAGE`

Os testes simulam Docker com `PIPEWIRE_REMOTE`, mas continuam lendo o `/proc/version` real do WSL. Isso adiciona a advertência específica do WSL e faz `available` retornar falso.

Nenhuma alteração foi realizada.

### Skip memory store

Arquivo:

`tests/agent/test_skip_memory_store_65429.py`

A execução original demorou durante a resolução da URL fictícia:

`http://test`

A pilha mostrou espera em:

- `socket.getaddrinfo`;
- `httpx`;
- `agent/model_metadata.py`;
- detecção de servidor local.

Com falha de rede imediata e controlada, o resultado foi:

- 4 testes aprovados;
- zero falhas;
- duração de 1,08 segundo;
- código de saída 0.

Classificação:

`NON_HERMETIC_NETWORK_PROBE`

### Hermes state

Arquivo:

`tests/test_hermes_state.py`

Resultado:

- 465 testes aprovados;
- zero falhas;
- duração de 373,24 segundos;
- código de saída 0.

O teste mais lento foi:

`test_optimize_fts_storage_vacuum_reports_truthful_size`

Duração aproximada:

95,95 segundos.

O aviso do `faulthandler` aos 90 segundos foi apenas diagnóstico; a execução continuou e foi aprovada.

## Auditoria complementar no Windows

O checkout nativo Windows foi tratado como auditoria de compatibilidade, não como gate canônico upstream.

Resultados principais registrados:

- CLI help, version e status aprovados;
- JavaScript instalado com sucesso;
- 44.709 testes aprovados;
- 763 testes falhos;
- 532 ignorados;
- 1 erro;
- falhas concentradas em caminhos, POSIX, permissões, SQLite, processos e timeouts específicos do Windows.

Classificação:

`WINDOWS_COMPATIBILITY_AUDIT`

## Estado do repositório

Após todas as instalações e validações:

- branch correta;
- commit-base preservado;
- working tree limpo;
- nenhum arquivo upstream alterado;
- nenhuma dependência atualizada;
- nenhum push realizado;
- nenhum merge realizado;
- nenhuma tag criada;
- nenhuma release criada.

## Evidências locais

Os logs direcionados estão preservados fora do repositório em:

`~/hermes-baseline-evidence`

Arquivos principais:

- `test_cua_no_overlay.log`
- `test_voice_mode.log`
- `test_skip_memory_store_diagnostic.log`
- `test_skip_memory_store_fast.log`
- `test_hermes_state.log`

## Conclusão preliminar

O commit-base congelado está tecnicamente apto para servir como fundação controlada do Harness Cognitivo.

As cinco falhas remanescentes da execução WSL foram classificadas como testes não completamente isolados do ambiente real. Os dois arquivos inicialmente incompletos foram aprovados em execuções direcionadas.

Nenhuma evidência encontrada exige modificação do código upstream para estabelecer o baseline.

A aprovação final depende de revisão independente deste documento e das evidências registradas.
