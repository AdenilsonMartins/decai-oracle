"""
🚀 Script de Deploy Automatizado - DecAI Oracle
Deploy do contrato na Sepolia com verificação automática
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account

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

def run_command(cmd, cwd=None):
    """Executa comando e retorna output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_prerequisites():
    """Verifica pré-requisitos"""
    print_header("1. Verificando Pré-requisitos")
    
    # Verificar Node.js
    success, stdout, _ = run_command("node --version")
    if success:
        print_success(f"Node.js instalado: {stdout.strip()}")
    else:
        print_error("Node.js não encontrado!")
        return False
    
    # Verificar npm
    success, stdout, _ = run_command("npm --version")
    if success:
        print_success(f"npm instalado: {stdout.strip()}")
    else:
        print_error("npm não encontrado!")
        return False
    
    # Verificar Hardhat
    contracts_dir = Path("contracts")
    if not contracts_dir.exists():
        print_error("Diretório 'contracts' não encontrado!")
        return False
    
    package_json = contracts_dir / "package.json"
    if not package_json.exists():
        print_error("package.json não encontrado em contracts/")
        return False
    
    print_success("Hardhat configurado")
    
    return True

def check_balance():
    """Verifica saldo da carteira"""
    print_header("2. Verificando Saldo da Carteira")
    
    try:
        rpc_url = os.getenv('SEPOLIA_RPC_URL', '')
        private_key = os.getenv('PRIVATE_KEY', '')
        
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = Account.from_key(private_key)
        
        balance_wei = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance_wei, 'ether')
        
        print_info(f"Endereço: {account.address}")
        print_info(f"Saldo: {balance_eth} SepoliaETH")
        
        if balance_eth < 0.05:
            print_warning("Saldo baixo! Recomendado: >0.05 ETH")
            print_info("Obtenha mais em: https://sepoliafaucet.com/")
            
            response = input("\nContinuar mesmo assim? (s/n): ")
            if response.lower() != 's':
                return False
        else:
            print_success("Saldo suficiente para deploy")
        
        return True
        
    except Exception as e:
        print_error(f"Erro ao verificar saldo: {str(e)}")
        return False

def compile_contracts():
    """Compila os contratos"""
    print_header("3. Compilando Contratos")
    
    print_info("Executando: npx hardhat compile")
    
    success, stdout, stderr = run_command(
        "npx hardhat compile",
        cwd="contracts"
    )
    
    if success:
        print_success("Contratos compilados com sucesso!")
        return True
    else:
        print_error("Erro na compilação:")
        print(stderr)
        return False

def deploy_to_sepolia():
    """Faz deploy na Sepolia"""
    print_header("4. Fazendo Deploy na Sepolia")
    
    print_info("Executando: npx hardhat run scripts/deploy.js --network sepolia")
    print_warning("Isso pode levar alguns minutos...")
    
    success, stdout, stderr = run_command(
        "npx hardhat run scripts/deploy.js --network sepolia",
        cwd="contracts"
    )
    
    if success:
        print_success("Deploy concluído!")
        print("\n" + stdout)
        
        # Tentar extrair endereço do contrato
        for line in stdout.split('\n'):
            if 'deployed to' in line.lower() or 'address' in line.lower():
                print_info(line)
        
        return True, stdout
    else:
        print_error("Erro no deploy:")
        print(stderr)
        return False, stderr

def extract_contract_address(deploy_output):
    """Extrai endereço do contrato do output"""
    # Procurar por padrão de endereço Ethereum
    import re
    pattern = r'0x[a-fA-F0-9]{40}'
    matches = re.findall(pattern, deploy_output)
    
    if matches:
        # Retornar o último endereço encontrado (geralmente é o do contrato)
        return matches[-1]
    
    return None

def update_env_file(contract_address):
    """Atualiza arquivo .env com novo endereço"""
    print_header("5. Atualizando Arquivo .env")
    
    env_path = Path('.env')
    
    if not env_path.exists():
        print_error("Arquivo .env não encontrado!")
        return False
    
    # Ler conteúdo atual
    with open(env_path, 'r') as f:
        lines = f.readlines()
    
    # Atualizar linha do contrato
    updated = False
    for i, line in enumerate(lines):
        if line.startswith('PREDICTION_ORACLE_ADDRESS='):
            lines[i] = f'PREDICTION_ORACLE_ADDRESS="{contract_address}"\n'
            updated = True
            break
    
    # Se não encontrou, adicionar
    if not updated:
        lines.append(f'\nPREDICTION_ORACLE_ADDRESS="{contract_address}"\n')
    
    # Salvar
    with open(env_path, 'w') as f:
        f.writelines(lines)
    
    print_success(f"Endereço atualizado: {contract_address}")
    return True

def verify_on_etherscan(contract_address):
    """Verifica contrato no Etherscan"""
    print_header("6. Verificando Contrato no Etherscan")
    
    etherscan_key = os.getenv('ETHERSCAN_API_KEY', '')
    
    if not etherscan_key:
        print_warning("ETHERSCAN_API_KEY não configurada")
        print_info("Pule a verificação ou configure a API Key")
        
        response = input("\nTentar verificar mesmo assim? (s/n): ")
        if response.lower() != 's':
            print_info("Verificação pulada")
            return True
    
    print_info(f"Verificando contrato: {contract_address}")
    
    success, stdout, stderr = run_command(
        f"npx hardhat verify --network sepolia {contract_address}",
        cwd="contracts"
    )
    
    if success:
        print_success("Contrato verificado no Etherscan!")
        print(stdout)
        return True
    else:
        print_warning("Erro na verificação (não crítico):")
        print(stderr)
        print_info("Você pode verificar manualmente depois")
        return True

def print_next_steps(contract_address):
    """Imprime próximos passos"""
    print_header("🎉 DEPLOY CONCLUÍDO COM SUCESSO!")
    
    print(f"\n{Colors.BOLD}Endereço do Contrato:{Colors.END}")
    print(f"{Colors.GREEN}{contract_address}{Colors.END}")
    
    print(f"\n{Colors.BOLD}Links Úteis:{Colors.END}")
    print(f"Etherscan: https://sepolia.etherscan.io/address/{contract_address}")
    print(f"Infura Dashboard: https://app.infura.io/")
    
    print(f"\n{Colors.BOLD}Próximos Passos:{Colors.END}")
    print("1. ✅ Testar integração com dashboard:")
    print("   streamlit run dashboard/app.py")
    print("\n2. ✅ Fazer previsão de teste:")
    print("   python src/main.py")
    print("\n3. ✅ Publicar dashboard no Streamlit Cloud")
    print("   Veja: docs/DEPLOYMENT_PLAN.md")
    print("\n4. ✅ Criar presença social (Twitter, Discord)")
    print("   Veja: docs/DEPLOYMENT_PLAN.md - Fase 4")

def main():
    """Função principal"""
    print_header("🚀 DEPLOY AUTOMATIZADO - DecAI Oracle")
    
    # Carregar .env
    load_dotenv()
    
    # Verificar pré-requisitos
    if not check_prerequisites():
        print_error("Pré-requisitos não atendidos!")
        sys.exit(1)
    
    # Verificar saldo
    if not check_balance():
        print_error("Saldo insuficiente ou verificação cancelada")
        sys.exit(1)
    
    # Compilar contratos
    if not compile_contracts():
        print_error("Falha na compilação")
        sys.exit(1)
    
    # Fazer deploy
    success, output = deploy_to_sepolia()
    if not success:
        print_error("Falha no deploy")
        sys.exit(1)
    
    # Extrair endereço do contrato
    contract_address = extract_contract_address(output)
    
    if contract_address:
        print_success(f"Contrato deployado em: {contract_address}")
        
        # Atualizar .env
        update_env_file(contract_address)
        
        # Verificar no Etherscan (opcional)
        verify_on_etherscan(contract_address)
        
        # Imprimir próximos passos
        print_next_steps(contract_address)
    else:
        print_warning("Não foi possível extrair endereço do contrato")
        print_info("Verifique o output acima e atualize manualmente o .env")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Deploy concluído com sucesso! 🎉{Colors.END}\n")

if __name__ == "__main__":
    main()
