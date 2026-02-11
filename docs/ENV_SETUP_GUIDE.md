# 🔐 Guia de Configuração do .env - DecAI Oracle

**Data**: 07 de Fevereiro de 2026  
**Status**: 📋 GUIA DE REFERÊNCIA

---

## ⚠️ PROBLEMAS IDENTIFICADOS

Seu arquivo `.env` atual tem **2 problemas críticos** que impedem o deploy:

### ❌ Problema 1: Private Key Inválida
```env
# ATUAL (INCORRETO) - 32 caracteres
PRIVATE_KEY="b3d1db2e0c9a4a5eb6908a02bb93ea3d"

# NECESSÁRIO - 66 caracteres (0x + 64 hex)
PRIVATE_KEY="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
```

### ❌ Problema 2: Mesma String para API e Private Key
A string `b3d1db2e0c9a4a5eb6908a02bb93ea3d` está sendo usada incorretamente em dois lugares.

---

## 📋 PASSO A PASSO PARA CORREÇÃO

### Passo 1: Obter Private Key da MetaMask

#### 1.1 Abrir MetaMask
- Clique no ícone da extensão MetaMask no navegador

#### 1.2 Selecionar a Conta
- Certifique-se de estar na conta que você quer usar para o projeto
- **IMPORTANTE**: Use uma conta de TESTE, não sua conta principal com fundos reais

#### 1.3 Exportar Private Key
```
1. Clique nos 3 pontos (⋮) ao lado do nome da conta
2. Selecione "Account Details"
3. Clique em "Show Private Key"
4. Digite sua senha do MetaMask
5. Clique em "Confirm"
6. Copie a chave (começa com 0x)
```

#### 1.4 Verificação
- ✅ A chave deve ter **66 caracteres**
- ✅ Deve começar com `0x`
- ✅ Deve conter apenas caracteres hexadecimais (0-9, a-f)

**Exemplo de formato correto:**
```
0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b
```

---

### Passo 2: Verificar Infura API Key

#### 2.1 Acessar Dashboard do Infura
1. Ir para: https://app.infura.io/
2. Fazer login com sua conta

#### 2.2 Encontrar a API Key
```
1. Dashboard → API Keys
2. Selecionar seu projeto (ou criar um novo)
3. Copiar o "PROJECT ID" (não o "PROJECT SECRET")
```

#### 2.3 Verificação
- ✅ A API Key deve ter **32 caracteres**
- ✅ Deve conter apenas caracteres hexadecimais (0-9, a-f)

**Exemplo:**
```
a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
```

---

### Passo 3: Atualizar o Arquivo .env

#### 3.1 Template Correto
Copie este template e substitua pelos seus valores:

```env
# ============================================
# ENVIRONMENT CONFIGURATION
# ============================================
ENVIRONMENT=development
LOG_LEVEL=INFO

# ============================================
# BLOCKCHAIN CONFIGURATION (Sepolia Testnet)
# ============================================

# Infura RPC URL
# Substitua YOUR_INFURA_API_KEY pela sua API Key do Infura (32 chars)
SEPOLIA_RPC_URL="https://sepolia.infura.io/v3/YOUR_INFURA_API_KEY"

# Private Key da Carteira
# Substitua YOUR_PRIVATE_KEY pela chave da MetaMask (66 chars, começa com 0x)
# ⚠️ NUNCA compartilhe esta chave! Use apenas para testes!
PRIVATE_KEY="0xYOUR_PRIVATE_KEY_64_CHARACTERS_HERE"

# Habilitar integração blockchain
BLOCKCHAIN_ENABLED=true

# ============================================
# SMART CONTRACT ADDRESS
# ============================================

# Endereço do contrato (será atualizado após deploy na Sepolia)
# Atualmente aponta para localhost - será substituído
PREDICTION_ORACLE_ADDRESS="0x5fbdb2315678afecb367f032d93f642f64180aa3"

# ============================================
# DATA APIS
# ============================================

# CoinGecko API (gratuita, sem necessidade de key)
COINGECKO_BASE_URL="https://api.coingecko.com/api/v3"

# ============================================
# ML MODEL CONFIGURATION
# ============================================

# Intervalo de atualização do modelo (em segundos)
MODEL_UPDATE_INTERVAL=3600

# Threshold de confiança para previsões (0.0 a 1.0)
PREDICTION_CONFIDENCE_THRESHOLD=0.7

# Ativos suportados (separados por vírgula)
SUPPORTED_ASSETS="BTC,ETH,SOL"

# ============================================
# API SETTINGS
# ============================================

# Host e porta para API local
API_HOST="0.0.0.0"
API_PORT=8000

# ============================================
# OPTIONAL: ETHERSCAN API (para verificação de contratos)
# ============================================

# Obtenha em: https://etherscan.io/myapikey
# ETHERSCAN_API_KEY="YOUR_ETHERSCAN_API_KEY"

# ============================================
# OPTIONAL: TWITTER BOT (para automação social)
# ============================================

# Obtenha em: https://developer.twitter.com/
# TWITTER_API_KEY="your_api_key"
# TWITTER_API_SECRET="your_api_secret"
# TWITTER_ACCESS_TOKEN="your_access_token"
# TWITTER_ACCESS_SECRET="your_access_secret"
```

#### 3.2 Exemplo Preenchido (com valores fictícios)
```env
ENVIRONMENT=development
LOG_LEVEL=INFO

# Blockchain (Sepolia Testnet)
SEPOLIA_RPC_URL="https://sepolia.infura.io/v3/a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
PRIVATE_KEY="0x1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b"
BLOCKCHAIN_ENABLED=true

# Contract Address
PREDICTION_ORACLE_ADDRESS="0x5fbdb2315678afecb367f032d93f642f64180aa3"

# Data APIs
COINGECKO_BASE_URL="https://api.coingecko.com/api/v3"
MODEL_UPDATE_INTERVAL=3600
PREDICTION_CONFIDENCE_THRESHOLD=0.7
SUPPORTED_ASSETS="BTC,ETH,SOL"

# API Settings
API_HOST="0.0.0.0"
API_PORT=8000
```

---

### Passo 4: Obter Sepolia ETH (Testnet)

Você precisa de ETH de teste para pagar as taxas de gas no deploy.

#### 4.1 Faucets Recomendados

**Opção 1: Alchemy Sepolia Faucet** (Mais Fácil)
```
URL: https://sepoliafaucet.com/
Requisitos: Conta Alchemy (gratuita)
Quantidade: 0.5 SepoliaETH/dia
```

**Passos:**
1. Criar conta em https://www.alchemy.com/
2. Acessar https://sepoliafaucet.com/
3. Fazer login com Alchemy
4. Colar endereço da sua carteira MetaMask
5. Clicar em "Send Me ETH"
6. Aguardar 1-2 minutos

**Opção 2: Infura Sepolia Faucet**
```
URL: https://www.infura.io/faucet/sepolia
Requisitos: Conta Infura (você já tem!)
Quantidade: 0.5 SepoliaETH/dia
```

**Opção 3: QuickNode Faucet**
```
URL: https://faucet.quicknode.com/ethereum/sepolia
Requisitos: Conta QuickNode (gratuita)
Quantidade: 0.1 SepoliaETH/dia
```

#### 4.2 Verificar Saldo
1. Abrir MetaMask
2. Trocar rede para "Sepolia Test Network"
3. Verificar se aparece o saldo (ex: 0.5 ETH)

**Se não aparecer a rede Sepolia:**
```
1. MetaMask → Settings → Advanced
2. Ativar "Show test networks"
3. Voltar e selecionar "Sepolia Test Network"
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Antes de prosseguir, verifique:

### Arquivo .env
- [ ] `SEPOLIA_RPC_URL` contém sua Infura API Key (32 chars)
- [ ] `PRIVATE_KEY` tem 66 caracteres e começa com 0x
- [ ] `PRIVATE_KEY` é diferente da Infura API Key
- [ ] Arquivo `.env` está no `.gitignore` (segurança)

### Carteira MetaMask
- [ ] Rede trocada para "Sepolia Test Network"
- [ ] Saldo > 0.1 SepoliaETH
- [ ] Endereço da carteira anotado

### Infura
- [ ] Conta criada e verificada
- [ ] Projeto criado
- [ ] API Key copiada

---

## 🔒 SEGURANÇA - IMPORTANTE!

### ⚠️ NUNCA faça isso:
- ❌ Compartilhar sua Private Key com ninguém
- ❌ Commitar o arquivo `.env` no Git
- ❌ Usar conta principal com fundos reais para testes
- ❌ Postar Private Key em fóruns/Discord/Telegram

### ✅ SEMPRE faça isso:
- ✅ Usar conta de teste separada
- ✅ Manter `.env` no `.gitignore`
- ✅ Usar `.env.example` para templates públicos
- ✅ Rotacionar chaves periodicamente

---

## 🧪 TESTE DE CONFIGURAÇÃO

Após configurar o `.env`, teste se está tudo correto:

```bash
# Navegar para a pasta do projeto
cd c:\Users\Valentim\Desktop\web3

# Testar conexão com Infura
python -c "from web3 import Web3; w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/SUA_API_KEY')); print('✅ Conectado!' if w3.is_connected() else '❌ Erro de conexão')"

# Testar Private Key
python -c "from eth_account import Account; Account.from_key('0xSUA_PRIVATE_KEY'); print('✅ Private Key válida!')"

# Verificar saldo
python -c "from web3 import Web3; w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/SUA_API_KEY')); balance = w3.eth.get_balance('SEU_ENDERECO'); print(f'Saldo: {w3.from_wei(balance, \"ether\")} ETH')"
```

---

## 📞 PRECISA DE AJUDA?

### Erros Comuns

**Erro: "Invalid private key"**
- Verificar se tem 66 caracteres
- Verificar se começa com 0x
- Verificar se não tem espaços extras

**Erro: "Insufficient funds"**
- Obter mais SepoliaETH nos faucets
- Verificar se está na rede Sepolia

**Erro: "Network timeout"**
- Verificar Infura API Key
- Verificar conexão com internet
- Tentar outro RPC endpoint

---

## 🚀 PRÓXIMOS PASSOS

Após configurar o `.env` corretamente:

1. ✅ Testar configuração (comandos acima)
2. ✅ Compilar contratos: `cd contracts && npx hardhat compile`
3. ✅ Deploy na Sepolia: `npx hardhat run scripts/deploy.js --network sepolia`
4. ✅ Atualizar `PREDICTION_ORACLE_ADDRESS` no `.env`
5. ✅ Testar dashboard: `streamlit run dashboard/app.py`

---

**Última Atualização**: 2026-02-07 21:18  
**Próximo Documento**: [DEPLOYMENT_PLAN.md](./DEPLOYMENT_PLAN.md)
