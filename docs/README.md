# 📚 DecAI Oracle - Documentação

**Versão:** 2.0  
**Última Atualização:** 09/02/2026

---

## 🎯 Visão Geral

DecAI Oracle é um oráculo descentralizado que combina Machine Learning com blockchain para fornecer previsões de preços de criptomoedas on-chain.

---

## 📖 Índice de Documentação

### 🚀 Início Rápido
- [ENV_SETUP_GUIDE.md](ENV_SETUP_GUIDE.md) - Configuração do ambiente
- [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) - Guia de deploy

### 📋 Planejamento V2
- [planning/](planning/) - Documentação completa do planejamento V2
  - [EXECUTION_PLAN_V2.md](planning/EXECUTION_PLAN_V2.md) - Plano de execução detalhado
  - [EXECUTIVE_SUMMARY_V2.md](planning/EXECUTIVE_SUMMARY_V2.md) - Resumo executivo
  - [ROADMAP_V2.md](planning/ROADMAP_V2.md) - Roadmap visual
  - [v2/](planning/v2/) - Documentos técnicos detalhados
    - [IMPLEMENTATION_PLAN.md](planning/v2/IMPLEMENTATION_PLAN.md) - Plano de implementação
    - [ARCHITECTURE.md](planning/v2/ARCHITECTURE.md) - Arquitetura do sistema
    - [SECURITY_PLAN.md](planning/v2/SECURITY_PLAN.md) - Plano de segurança

### 📊 Progresso e Status
- [PROGRESS_CHECKLIST.md](PROGRESS_CHECKLIST.md) - Checklist de progresso
- [DEPLOYMENT_LOG.md](DEPLOYMENT_LOG.md) - Log de deployments
- [TEST_ANALYSIS_REPORT.md](TEST_ANALYSIS_REPORT.md) - Relatório de testes

### 🗂️ Outros Documentos
- [FEATURES.md](FEATURES.md) - Features do sistema
- [INDEX.md](INDEX.md) - Índice geral
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Estrutura do projeto
- [REPOSITORY_ORGANIZATION.md](REPOSITORY_ORGANIZATION.md) - Organização do repositório

### 📦 Arquivo (V1)
- [archive/v1/](archive/v1/) - Documentação da versão 1 (arquivada)

---

## 🏗️ Estrutura do Projeto

```
decai-oracle/
├── src/                    # Código fonte
│   ├── ml/                # Machine Learning
│   ├── blockchain/        # Integração blockchain
│   └── data/              # Coleta e processamento de dados
├── contracts/             # Smart contracts Solidity
├── dashboard/             # Dashboard Streamlit
├── tests/                 # Testes automatizados
├── scripts/               # Scripts de utilidade
└── docs/                  # Documentação (você está aqui)
    ├── planning/          # Planejamento V2
    │   └── v2/           # Documentos técnicos
    └── archive/           # Documentação arquivada
```

---

## 🚀 Quick Start

### 1. Configurar Ambiente
```bash
# Ver guia completo
cat docs/ENV_SETUP_GUIDE.md

# Setup rápido
python scripts/setup.py
```

### 2. Executar Testes
```bash
# Testes end-to-end
python tests/test_e2e.py

# Testes unitários
pytest tests/ -v --cov
```

### 3. Deploy
```bash
# Ver guia completo
cat docs/DEPLOY_GUIDE.md

# Deploy em testnet
cd contracts
npx hardhat run scripts/deploy.js --network sepolia
```

---

## 📊 Status Atual

### ✅ Completado
- Contrato deployado em Sepolia: `0x5A1788fBDBB9868C2D89A01ee5C6B692cb57fAFA`
- Infraestrutura base funcionando
- Testes E2E passando
- Documentação V2 completa

### 🔄 Em Progresso
- Implementação de features avançadas (V2)
- Testes automatizados completos
- Sistema de monitoring

### 📅 Planejado
- Multi-chain support (Polygon)
- Federated Learning
- DAO Governance

---

## 🔗 Links Úteis

### Blockchain
- **Contrato (Sepolia):** [Etherscan](https://sepolia.etherscan.io/address/0x5A1788fBDBB9868C2D89A01ee5C6B692cb57fAFA)
- **Wallet:** `0xcbc53e6265834A24090466Ac8442aA087b7de66f`

### Repositório
- **GitHub:** [AdenilsonMartins/decai-oracle](https://github.com/AdenilsonMartins/decai-oracle)
- **Issues:** [GitHub Issues](https://github.com/AdenilsonMartins/decai-oracle/issues)

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação relevante acima
2. Abra uma issue no GitHub
3. Entre em contato via Discord (em breve)

---

## 📝 Convenções de Documentação

### Emojis
- 🎯 Objetivos e metas
- ✅ Completado
- 🔄 Em progresso
- 📅 Planejado
- 🚨 Crítico/Urgente
- 📊 Métricas e dados
- 🔒 Segurança
- 🚀 Deploy e produção

### Estrutura de Arquivos
- `*.md` - Documentação em Markdown
- `planning/` - Planejamento e roadmaps
- `archive/` - Documentação obsoleta (mantida para referência)

---

**Última Atualização:** 09/02/2026  
**Versão:** 2.0  
**Mantenedor:** @AdenilsonMartins
