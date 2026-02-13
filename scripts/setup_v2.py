#!/usr/bin/env python3
"""
DecAI Oracle Network - Setup & Configuration Script
Versão 1.1
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


class SetupManager:
    """Gerenciador de setup do projeto"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.errors = []
        self.warnings = []
    
    def print_header(self):
        """Imprime cabeçalho"""
        print("\n" + "="*60)
        print("🔷 DECAI ORACLE NETWORK - SETUP & CONFIGURATION")
        print("="*60 + "\n")

    def check_python_version(self) -> bool:
        """Verifica versão do Python"""
        print("🐍 Verificando versão do Python...")
        
        version = sys.version_info
        required = (3, 8)
        
        if version >= required:
            print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
            return True
        else:
            print(f"   ❌ Python {version.major}.{version.minor} detectado")
            print(f"   ⚠️  Requer Python >= {required[0]}.{required[1]}")
            self.errors.append("Python version too old")
            return False
    
    def check_virtual_env(self) -> bool:
        """Verifica se está em virtual environment"""
        print("\n📦 Verificando virtual environment...")
        
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            print("   ✅ Virtual environment ativo")
            return True
        else:
            print("   ⚠️  Virtual environment não detectado")
            print("   💡 Recomendado: python -m venv venv")
            self.warnings.append("No virtual environment")
            return False
    
    def install_dependencies(self) -> bool:
        """Instala dependências do requirements.txt"""
        print("\n📥 Instalando dependências...")
        
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("   ❌ requirements.txt não encontrado!")
            self.errors.append("Missing requirements.txt")
            return False
        
        try:
            print("   ⏳ Instalando pacotes (isso pode demorar)...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True,
                check=True
            )
            print("   ✅ Dependências instaladas com sucesso!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro ao instalar dependências: {e}")
            self.errors.append("Dependency installation failed")
            return False
    
    def verify_packages(self) -> Dict[str, bool]:
        """Verifica se pacotes críticos estão instalados"""
        print("\n🔍 Verificando pacotes críticos...")
        
        critical_packages = {
            'web3': 'Web3.py',
            'eth_account': 'eth-account',
            'dotenv': 'python-dotenv'
        }
        
        results = {}
        
        for package, display_name in critical_packages.items():
            try:
                __import__(package)
                print(f"   ✅ {display_name}")
                results[package] = True
            except ImportError:
                print(f"   ❌ {display_name} não encontrado!")
                self.errors.append(f"Missing package: {display_name}")
                results[package] = False
        
        return results
    
    def check_env_file(self) -> bool:
        """Verifica existência e completude do .env"""
        print("\n⚙️  Verificando arquivo .env...")
        
        env_file = self.project_root / ".env"
        
        if not env_file.exists():
            print("   ❌ Arquivo .env não encontrado!")
            print("   💡 Copie .env.example para .env e preencha as variáveis")
            self.errors.append("Missing .env file")
            return False
        
        print("   ✅ Arquivo .env encontrado")
        
        # Verificar variáveis críticas
        required_vars = [
            'PRIVATE_KEY',
            'SEPOLIA_RPC_URL',
            'PREDICTION_ORACLE_ADDRESS'
        ]
        
        from dotenv import dotenv_values
        env_vars = dotenv_values(env_file)
        
        missing_vars = []
        empty_vars = []
        
        for var in required_vars:
            if var not in env_vars:
                missing_vars.append(var)
                print(f"   ❌ {var} não encontrada")
            elif not env_vars[var] or env_vars[var].startswith('your_'):
                empty_vars.append(var)
                print(f"   ⚠️  {var} não configurada")
            else:
                print(f"   ✅ {var} configurada")
        
        if missing_vars:
            self.errors.append(f"Missing env vars: {', '.join(missing_vars)}")
        
        if empty_vars:
            self.warnings.append(f"Empty env vars: {', '.join(empty_vars)}")
        
        return len(missing_vars) == 0
    
    def test_blockchain_connection(self) -> bool:
        """Testa conexão com blockchain"""
        print("\n🔗 Testando conexão com blockchain...")
        
        try:
            # Adicionar src ao path
            sys.path.insert(0, str(self.project_root / 'src'))
            from blockchain.contract_manager import ContractManager
            
            manager = ContractManager()
            
            # Testar conexão básica
            w3 = manager.w3
            if not w3.is_connected():
                raise Exception("Não foi possível conectar ao RPC")
            
            chain_id = w3.eth.chain_id
            latest_block = w3.eth.block_number
            balance = w3.eth.get_balance(manager.account.address)
            balance_eth = w3.from_wei(balance, 'ether')
            
            print(f"   ✅ Conectado à rede Sepolia")
            print(f"   ✅ Chain ID: {chain_id}")
            print(f"   ✅ Último bloco: {latest_block}")
            print(f"   ✅ Wallet: {manager.account.address}")
            print(f"   ✅ Saldo: {balance_eth:.4f} ETH")
            
            if balance_eth < 0.001:
                print("   ⚠️  Saldo baixo! Adicione Sepolia ETH")
                self.warnings.append("Low wallet balance")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Falha na conexão: {str(e)}")
            self.errors.append("Blockchain connection failed")
            return False
    
    def create_directories(self) -> bool:
        """Cria estrutura de diretórios necessária"""
        print("\n📁 Criando estrutura de diretórios...")
        
        directories = [
            'data',
            'logs',
            'tests',
            'artifacts'
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ {directory}/")
        
        return True
    
    def print_summary(self):
        """Imprime resumo do setup"""
        print("\n" + "="*60)
        print("📊 SETUP SUMMARY")
        print("="*60)
        
        if self.errors:
            print("\n❌ ERROS CRÍTICOS:")
            for error in self.errors:
                print(f"   • {error}")
        
        if self.warnings:
            print("\n⚠️  AVISOS:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ SETUP COMPLETO SEM PROBLEMAS!")
            print("\n🚀 Próximos passos:")
            print("   1. Execute: python src/main.py")
            print("   2. Verifique o dashboard: streamlit run dashboard/app.py")
        elif not self.errors:
            print("\n✅ SETUP COMPLETO COM AVISOS")
            print("   Sistema funcional, mas revise os avisos acima")
        else:
            print("\n❌ SETUP INCOMPLETO")
            print("   Corrija os erros acima antes de continuar")
        
        print("="*60 + "\n")
    
    def run(self):
        """Executa setup completo"""
        self.print_header()
        
        # Checks
        self.check_python_version()
        self.check_virtual_env()
        self.check_env_file()
        
        # Instalação
        install = input("\n❓ Instalar/atualizar dependências? (y/N): ")
        if install.lower() == 'y':
            self.install_dependencies()
        
        # Verificações pós-instalação
        self.verify_packages()
        self.create_directories()
        
        # Teste de conexão
        test_connection = input("\n❓ Testar conexão com blockchain? (y/N): ")
        if test_connection.lower() == 'y':
            self.test_blockchain_connection()
        
        # Resumo
        self.print_summary()


def main():
    """Função principal"""
    try:
        setup = SetupManager()
        setup.run()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {str(e)}")
        raise


if __name__ == "__main__":
    main()
