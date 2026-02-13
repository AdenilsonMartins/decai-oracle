# ⏳ DecAI Oracle Network — Pendências e Próximos Passos

> **Última Atualização**: 2026-02-13  
> **Status Geral**: 95% Concluído (V2 Prod-Ready ✅ → Falta: Dashboard Cloud)  

---

## 📊 Visão Geral de Progresso

```
Fase 1: Preparação      [██████████] 100% ✅
Fase 2: Implementação   [██████████] 100% ✅
Fase 3: Validação       [██████████] 100% ✅
Fase 4: Deploy          [██████████] 100% ✅ (API Active)
Fase 5: Hardening V2.1  [████░░░░░░]  40% 🔄 (Audit ✅)
```

---

## 🔴 PENDÊNCIAS CRÍTICAS (Deploy e Produção)

### 1. Deploy do Contrato V2 no Sepolia (Novo Deploy)

**Status**: ✅ **CONCLUÍDO** (Verificado em 2026-02-11)

- **Endereço V2**: `0x0E8B23cb4Dcdd2AA3bc7a5db0070a2E9CB1c4252`
- **Features Ativas**: AccessControl, Pausable, Gas Optimization.
- **Testes**: Script de verificação de Roles V2 ✅ | Testes de Integração E2E ✅

**Ações Realizadas:**
- [x] Contrato V2 deployado (`0x0E8B...`)
- [x] Atualizar `PREDICTION_ORACLE_ADDRESS` no `.env`
- [x] Atribuir `PREDICTOR_ROLE` à wallet da API (Verificado via script)
- [x] Executar testes E2E com novo contrato (Tests passed: `tests/integration/test_blockchain.py`)

**Observação**: O documento anterior incorretamente listava `0x0E8B...` como V1. Verificação técnica confirmou que este endereço contém o bytecode V2 com AccessControl.

---

### 2. Deploy do Backend em Cloud
**Status**: ✅ **CONCLUÍDO** (Deploy no Railway ativo)

**Tarefas:**
- [x] Escolher plataforma (Railway)
- [x] Criar `Dockerfile` para a API FastAPI
- [x] Criar `docker-compose.yml` (API + Redis)
- [x] Configurar variáveis de ambiente em produção (`.env.production.example`)
- [x] Deploy e verificar endpoints remotamente (Status: Active)
- [ ] Configurar domínio customizado (opcional)
- [ ] Configurar HTTPS/TLS (Automático no Railway)

---

### 3. Deploy do Dashboard (Streamlit Cloud)

**Status**: ❌ Não iniciado. Dashboard roda apenas localmente.

**Tarefas:**
- [ ] Criar conta no [Streamlit Cloud](https://share.streamlit.io/)
- [ ] Conectar repositório GitHub
- [ ] Configurar app (branch: `main`, file: `dashboard/app.py`)
- [ ] Adicionar secrets (variáveis do `.env`) no Streamlit Cloud
- [ ] Deploy e testar URL pública
- [ ] Verificar performance (< 3s load time)
- [ ] Testar responsividade mobile

---

### 4. Redis para Produção

**Status**: ⚠️ Middleware funciona sem Redis (graceful fallback), mas para produção Redis é necessário.

**Tarefas:**
- [ ] Configurar Redis instance (Docker ou managed: Upstash, Redis Cloud)
- [ ] Atualizar `REDIS_URL` no `.env` de produção
- [ ] Verificar rate limiting com Redis ativo
- [ ] Verificar caching com Redis ativo

---

## 🟡 PENDÊNCIAS IMPORTANTES (Hardening V2.1)

### 5. Auditoria Automatizada do Contrato
**Status**: ✅ **CONCLUÍDO** (Slither Report ✅)

**Tarefas:**
- [x] Criar script de auditoria: `scripts/security_audit.py`
- [x] Executar via Docker: `run_audit.bat` (Result: 0 High/Med Issues)
- [x] Corrigir findings de severidade **High** e **Medium** (Nada encontrado)
- [x] Documentar resultados em `docs/security/AUDIT_REPORT_V2.md`

---

### 6. Cobertura de Testes

**Status**: 🔄 Em Progresso (51% Total)

**Tarefas:**
- [x] Executar: `pytest --cov=src tests/ --cov-report=html` (Relatório gerado)
- [x] **Adicionar testes para `src/resilient_oracle.py` (Cobertura 65% ✅)**
- [ ] Meta: > 80% de cobertura (Atual: 51%)
- [ ] Adicionar testes para `src/social/twitter_bot.py`
- [ ] Adicionar testes para `src/api/middleware.py`
- [ ] Adicionar testes para `src/monitoring/metrics.py`

---

### 7. Correção de Deprecation Warnings

**Status**: ⚠️ 21 warnings não-críticos pendentes.

**Tarefas:**
- [ ] **Pydantic V2**: Atualizar `src/utils/config.py` — trocar `env=` por `validation_alias=` em todos os `Field()`
- [ ] **python-json-logger**: Atualizar `src/utils/logger.py` — trocar `from pythonjsonlogger import jsonlogger` por `from pythonjsonlogger import json as jsonlogger`
- [ ] Verificar se `websockets` legacy warning foi resolvido

---

### 8. Inconsistência de Endereços de Contrato

**Status**: ✅ **RESOLVIDO**

- **Endereço Consolidado**: `0x0E8B23cb4Dcdd2AA3bc7a5db0070a2E9CB1c4252`
- **Arquivos Atualizados**: README.md, .env, e Documentação V2.
- **Ação**: O endereço antigo `0x5A...` (deploy falho/V1) foi descartado. O endereço `0x0E8B...` foi verificado como V2.

---

## 🟢 PENDÊNCIAS FUTURAS (Roadmap V2.2+)

### 9. Multi-Chain Support

- [ ] Adicionar suporte a Polygon (Mumbai testnet)
- [ ] Adapter para deploy multi-chain
- [ ] Configuração por rede no `.env`

### 10. IPFS Integration

- [ ] Implementar backup descentralizado de previsões via IPFS
- [ ] Armazenar modelos ML no IPFS
- [ ] Dependência já no `requirements.txt` (`ipfshttpclient==0.8.0a2`)

### 11. Advanced ML Models

- [ ] Implementar modelo LSTM para previsões mais precisas
- [ ] Implementar modelo Transformer
- [ ] Comparar com baseline (Linear Regression atual)
- [ ] A/B testing de modelos

### 12. Chainlink Price Feeds (On-Chain)

- [ ] Integrar Chainlink como 4ª fonte no `data_aggregator.py`
- [ ] Confidence: 99% (fonte on-chain, mais confiável)
- [ ] Placeholder já existe na arquitetura

### 13. Governança (DAO)

- [ ] Implementar contrato de governança
- [ ] Permitir votação em parâmetros do protocolo
- [ ] Token de governança (futuro)

### 14. WebSocket para Dados em Tempo Real

- [ ] Adicionar WebSocket stream (Binance WebSocket API)
- [ ] Atualizar dashboard com dados em tempo real
- [ ] Reduzir latência de atualização

---

## 🧹 LIMPEZA DE DOCUMENTAÇÃO

### Documentos Redundantes para Remover/Arquivar

O projeto tem **74 arquivos .md**, sendo que muitos são versões antigas, rascunhos ou duplicatas. Recomenda-se manter apenas os essenciais e mover o resto para `docs/archive/`. Os 2 novos documentos (`STATUS_COMPLETO.md` e `PENDENCIAS.md`) substituem a maioria.

#### Documentos que podem ser removidos/movidos para archive:
| Documento | Motivo |
|-----------|--------|
| `docs/EXECUTIVE_SUMMARY.md` | Substituído por `STATUS_COMPLETO.md` |
| `docs/PROGRESS_CHECKLIST.md` | Substituído por este documento |
| `docs/INDEX.md` | Desatualizado, referencia docs inexistentes |
| `docs/planning/v2/FINAL_REPORT.md` | Consolidado em `STATUS_COMPLETO.md` |
| `docs/planning/v2/PROGRESS_REPORT.md` | Consolidado em `STATUS_COMPLETO.md` |
| `docs/planning/v2/SESSION_SUMMARY.md` | Informação consolidada |
| `docs/planning/v2/IMPLEMENTATION_STATUS.md` | Consolidado em `STATUS_COMPLETO.md` |
| `docs/planning/v2/EXECUTION_GUIDE.md` | Informação no QUICKSTART |
| `docs/planning/EXECUTIVE_SUMMARY_V2.md` | Consolidado |
| `docs/planning/INDEX.md` | Desatualizado |
| `docs/planning/README.md` | Desatualizado |
| `docs/planning/QUICK_START.md` | Duplicata do QUICKSTART.md raiz |
| `docs/planning/EXECUTION_PLAN_V2.md` | Consolidado |
| `docs/planning/UPDATE_RESILIENT_ARCHITECTURE.md` | Consolidado no V2 |
| `docs/planning/VISUAL_DIAGRAM.md` | Diagramas já no STATUS_COMPLETO |

#### Documentos ESSENCIAIS para MANTER:
| Documento | Razão |
|-----------|-------|
| `README.md` | Principal — público no GitHub |
| `QUICKSTART.md` | Guia rápido para novos devs |
| `CONTRIBUTING.md` | Guia de contribuição |
| `CHANGELOG_V2.md` | Histórico de mudanças |
| `LICENSE` | Licença MIT |
| `.env.example` | Template de configuração |
| `docs/STATUS_COMPLETO.md` | ← **NOVO** — O que temos |
| `docs/PENDENCIAS.md` | ← **NOVO** — O que falta |
| `docs/DEPLOY_GUIDE.md` | Guia de deploy |
| `docs/ENV_SETUP_GUIDE.md` | Guia de ambiente |
| `docs/DEPLOYMENT_LOG.md` | Registro de deploys |
| `docs/TEST_ANALYSIS_REPORT.md` | Análise dos testes |
| `docs/security/AUDIT_V2.md` | Auditoria de segurança |
| `docs/planning/v2/IMPLEMENTATION_PLAN.md` | Plano original (referência) |
| `docs/planning/v2/RESILIENT_ARCHITECTURE.md` | Arquitetura V2 (referência) |
| `docs/planning/v2/DEVELOPMENT_PLAN_V2.1.md` | Próximas fases |
| `docs/planning/v2/AI_AGENT_TASKS.md` | Tasks para V2.2+ |
| `docs/planning/ROADMAP_V2.md` | Roadmap de longo prazo |

---

## 🎯 PRIORIDADE DE EXECUÇÃO

### 🔴 Fazer AGORA (1-2h)
1. **Re-deploy contrato V2** no Sepolia
2. **Atualizar `.env`** com novo endereço
3. **Executar testes E2E** com novo contrato
4. **Corrigir endereço** no README.md

### 🟡 Fazer ESTA SEMANA (3-4h)
5. **Dockerizar** a API (Dockerfile + docker-compose) ✅
6. **Deploy do backend** em Railway/Render ✅
7. **Deploy do dashboard** no Streamlit Cloud
8. **Configurar Redis** para produção

### 🟢 Fazer NO PRÓXIMO CICLO (V2.1 — 1 semana)
9. Auditoria Slither
10. Cobertura de testes > 80%
11. Correção de deprecation warnings
12. Limpeza final de documentação

### 🔵 Backlog (V2.2+)
13. Chainlink Price Feeds
14. IPFS integration
15. Advanced ML (LSTM/Transformer)
16. Multi-chain (Polygon)
17. Governança (DAO)
18. WebSocket streaming

---

**Este documento substitui**: `PROGRESS_CHECKLIST.md`, `IMPLEMENTATION_STATUS.md`, e todas as listas de "próximos passos" fragmentadas nos documentos V2 anteriores.
