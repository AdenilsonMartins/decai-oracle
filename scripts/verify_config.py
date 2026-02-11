"""
🔍 Script de Verificação de Configuração - DecAI Oracle
Verifica se o arquivo .env está configurado corretamente
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
import re

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_env_file():
    """Verifica se o arquivo .env existe"""
    print_header("1. Verificando Arquivo .env")
    
    env_path = Path('.env')
    if not env_path.exists():
        print_error("Arquivo .env não encontrado!")
        print_info("Copie .env.example para .env e configure as variáveis")
        return False
    
    print_success("Arquivo .env encontrado")
    return True

def check_private_key():
    """Verifica se a Private Key está configurada corretamente"""
    print_header("2. Verificando Private Key")
    
    private_key = os.getenv('PRIVATE_KEY', '')
    
    # Verificar se existe
    if not private_key:
        print_error("PRIVATE_KEY não configurada no .env")
        return False
    
    # Verificar formato
    if not private_key.startswith('0x'):
        print_error("PRIVATE_KEY deve começar com '0x'")
        return False
    
    # Verificar tamanho
    if len(private_key) != 66:
        print_error(f"PRIVATE_KEY deve ter 66 caracteres (tem {len(private_key)})")
        print_info("Formato: 0x + 64 caracteres hexadecimais")
        return False
    
    # Verificar se é hexadecimal
    if not re.match(r'^0x[0-9a-fA-F]{64}$', private_key):
        print_error("PRIVATE_KEY contém caracteres inválidos")
        print_info("Use apenas 0-9 e a-f após o '0x'")
        return False
    
    # Tentar criar conta
    try:
        account = Account.from_key(private_key)
        print_success("Private Key válida!")
        print_info(f"Endereço da carteira: {account.address}")
        return True
    except Exception as e:
        print_error(f"Private Key inválida: {str(e)}")
        return False

def check_infura_connection():
    """Verifica conexão com Infura"""
    print_header("3. Verificando Conexão Infura")
    
    rpc_url = os.getenv('SEPOLIA_RPC_URL', '')
    
    if not rpc_url:
        print_error("SEPOLIA_RPC_URL não configurada")
        return False
    
    # Verificar formato
    if 'infura.io' not in rpc_url:
        print_warning("URL não parece ser do Infura")
    
    # Tentar conectar
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not w3.is_connected():
            print_error("Não foi possível conectar ao Infura")
            print_info("Verifique sua API Key")
            return False
        
        print_success("Conectado ao Infura!")
        
        # Verificar rede
        chain_id = w3.eth.chain_id
        if chain_id == 11155111:
            print_success("Rede Sepolia confirmada (Chain ID: 11155111)")
        else:
            print_warning(f"Chain ID inesperado: {chain_id}")
        
        # Verificar bloco atual
        block = w3.eth.block_number
        print_info(f"Bloco atual: {block:,}")
        
        return True
        
    except Exception as e:
        print_error(f"Erro ao conectar: {str(e)}")
        return False

def check_wallet_balance():
    """Verifica saldo da carteira na Sepolia"""
    print_header("4. Verificando Saldo da Carteira")
    
    try:
        rpc_url = os.getenv('SEPOLIA_RPC_URL', '')
        private_key = os.getenv('PRIVATE_KEY', '')
        
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = Account.from_key(private_key)
        
        balance_wei = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        
        print_info(f"Endereço: {account.address}")
        print_info(f"Saldo: {balance_eth} SepoliaETH")
        
        # Verificar se tem saldo suficiente
        min_balance = 0.05  # 0.05 ETH mínimo recomendado
        
        if balance_eth == 0:
            print_error("Carteira sem saldo!")
            print_info("Obtenha SepoliaETH em: https://sepoliafaucet.com/")
            return False
        elif balance_eth < min_balance:
            print_warning(f"Saldo baixo (recomendado: >{min_balance} ETH)")
            print_info("Considere obter mais ETH nos faucets")
            return True
        else:
            print_success(f"Saldo suficiente para deploy!")
            return True
            
    except Exception as e:
        print_error(f"Erro ao verificar saldo: {str(e)}")
        return False

def check_contract_address():
    """Verifica endereço do contrato"""
    print_header("5. Verificando Endereço do Contrato")
    
    contract_address = os.getenv('PREDICTION_ORACLE_ADDRESS', '')
    
    if not contract_address:
        print_warning("PREDICTION_ORACLE_ADDRESS não configurado")
        print_info("Será configurado após o deploy")
        return True
    
    # Verificar formato
    if not contract_address.startswith('0x'):
        print_error("Endereço deve começar com '0x'")
        return False
    
    if len(contract_address) != 42:
        print_error(f"Endereço deve ter 42 caracteres (tem {len(contract_address)})")
        return False
    
    # Verificar se é endereço válido
    try:
        checksum_address = Web3.to_checksum_address(contract_address)
        print_success(f"Endereço válido: {checksum_address}")
        
        # Verificar se é localhost ou Sepolia
        if contract_address == "0x5fbdb2315678afecb367f032d93f642f64180aa3":
            print_warning("Usando endereço padrão do Hardhat (localhost)")
            print_info("Faça deploy na Sepolia para atualizar")
        
        return True
        
    except Exception as e:
        print_error(f"Endereço inválido: {str(e)}")
        return False

def check_other_configs():
    """Verifica outras configurações"""
    print_header("6. Verificando Outras Configurações")
    
    configs = {
        'COINGECKO_BASE_URL': 'https://api.coingecko.com/api/v3',
        'MODEL_UPDATE_INTERVAL': '3600',
        'PREDICTION_CONFIDENCE_THRESHOLD': '0.7',
        'SUPPORTED_ASSETS': 'BTC,ETH,SOL',
        'API_HOST': '0.0.0.0',
        'API_PORT': '8000',
    }
    
    all_ok = True
    
    for key, expected in configs.items():
        value = os.getenv(key, '')
        
        if not value:
            print_warning(f"{key} não configurado (usando padrão)")
            all_ok = False
        elif value == expected:
            print_success(f"{key} = {value}")
        else:
            print_info(f"{key} = {value} (customizado)")
    
    return all_ok

def check_gitignore():
    """Verifica se .env está no .gitignore"""
    print_header("7. Verificando Segurança (.gitignore)")
    
    gitignore_path = Path('.gitignore')
    
    if not gitignore_path.exists():
        print_warning(".gitignore não encontrado")
        return False
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    if '.env' in content:
        print_success(".env está no .gitignore (seguro)")
        return True
    else:
        print_error(".env NÃO está no .gitignore!")
        print_warning("PERIGO: Suas chaves podem ser expostas no Git!")
        print_info("Adicione '.env' ao arquivo .gitignore")
        return False

def print_summary(results):
    """Imprime resumo dos resultados"""
    print_header("📊 RESUMO DA VERIFICAÇÃO")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print(f"Total de verificações: {total}")
    print(f"{Colors.GREEN}Passou: {passed}{Colors.END}")
    print(f"{Colors.RED}Falhou: {failed}{Colors.END}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 TODAS AS VERIFICAÇÕES PASSARAM!{Colors.END}")
        print(f"{Colors.GREEN}Você está pronto para fazer deploy!{Colors.END}\n")
        print_info("Próximo passo: cd contracts && npx hardhat run scripts/deploy.js --network sepolia")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  ALGUMAS VERIFICAÇÕES FALHARAM{Colors.END}")
        print(f"{Colors.YELLOW}Corrija os problemas acima antes de prosseguir{Colors.END}\n")
        print_info("Consulte: docs/ENV_SETUP_GUIDE.md")

def main():
    """Função principal"""
    print_header("🔍 VERIFICAÇÃO DE CONFIGURAÇÃO - DecAI Oracle")
    
    # Carregar .env
    load_dotenv()
    
    # Executar verificações
    results = {
        'Arquivo .env': check_env_file(),
        'Private Key': check_private_key(),
        'Conexão Infura': check_infura_connection(),
        'Saldo da Carteira': check_wallet_balance(),
        'Endereço do Contrato': check_contract_address(),
        'Outras Configurações': check_other_configs(),
        'Segurança (.gitignore)': check_gitignore(),
    }
    
    # Imprimir resumo
    print_summary(results)
    
    # Retornar código de saída
    sys.exit(0 if all(results.values()) else 1)

if __name__ == "__main__":
    main()
