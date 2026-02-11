"""
DecAI Oracle - Smart Contract Manager
Versão 2.0 - Integração Real com Blockchain

Deploy Info:
- Network: Sepolia Testnet
- Contract: 0x5A1788fBDBB9868C2D89A01ee5C6B692cb57fAFA
- Deployed: 09/02/2026
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from eth_account import Account
from dotenv import load_dotenv

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()


class ContractManager:
    """Gerenciador de interações com o smart contract PredictionOracle"""
    
    def __init__(self):
        """Inicializa a conexão com o blockchain e carrega o contrato"""
        self.w3 = self._initialize_web3()
        self.account = self._load_account()
        self.contract = self._load_contract()
        
        logger.info("✅ ContractManager inicializado com sucesso")
        logger.info(f"📡 Conectado à rede: {os.getenv('NETWORK', 'sepolia')}")
        logger.info(f"📍 Contrato: {self.contract.address}")
        logger.info(f"💼 Wallet: {self.account.address}")
        logger.info(f"💰 Saldo: {self.get_wallet_balance()} ETH")
    
    def _initialize_web3(self) -> Web3:
        """Inicializa conexão Web3 com a rede Sepolia"""
        rpc_url = os.getenv('SEPOLIA_RPC_URL')
        
        if not rpc_url:
            raise ValueError("❌ SEPOLIA_RPC_URL não configurada no .env")
        
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Middleware para redes PoA (Proof of Authority) como Sepolia
        w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        
        if not w3.is_connected():
            raise ConnectionError("❌ Falha ao conectar na rede Sepolia")
        
        logger.info(f"✅ Conectado ao RPC: {rpc_url[:50]}...")
        logger.info(f"🔗 Chain ID: {w3.eth.chain_id}")
        logger.info(f"📦 Último bloco: {w3.eth.block_number}")
        
        return w3
    
    def _load_account(self) -> Account:
        """Carrega a conta a partir da private key"""
        private_key = os.getenv('PRIVATE_KEY')
        
        if not private_key:
            raise ValueError("❌ PRIVATE_KEY não configurada no .env")
        
        if not private_key.startswith('0x'):
            private_key = '0x' + private_key
        
        account = Account.from_key(private_key)
        logger.info(f"🔑 Conta carregada: {account.address}")
        
        return account
    
    def _load_contract(self):
        """Carrega o contrato a partir do ABI e endereço"""
        contract_address = os.getenv('PREDICTION_ORACLE_ADDRESS')
        
        if not contract_address:
            raise ValueError("❌ PREDICTION_ORACLE_ADDRESS não configurado no .env")
        
        # Verificar se o endereço é válido
        if not self.w3.is_address(contract_address):
            raise ValueError(f"❌ Endereço de contrato inválido: {contract_address}")
        
        # Carregar ABI do arquivo compilado do Hardhat
        abi = self._load_abi()
        
        # Criar instância do contrato
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(contract_address),
            abi=abi
        )
        
        logger.info(f"📜 Contrato carregado: {contract.address}")
        
        return contract
    
    def _load_abi(self) -> List[Dict]:
        """Carrega o ABI do contrato a partir do artifact do Hardhat"""
        # Possíveis caminhos para o artifact
        possible_paths = [
            Path("contracts/artifacts/src/PredictionOracle.sol/PredictionOracle.json"),
            Path("contracts/artifacts/contracts/PredictionOracle.sol/PredictionOracle.json"),
            Path("../contracts/artifacts/contracts/PredictionOracle.sol/PredictionOracle.json"),
            Path("artifacts/contracts/PredictionOracle.sol/PredictionOracle.json"),
        ]
        
        for artifact_path in possible_paths:
            if artifact_path.exists():
                with open(artifact_path, 'r') as f:
                    artifact = json.load(f)
                    logger.info(f"✅ ABI carregado de: {artifact_path}")
                    return artifact['abi']
        
        # Se não encontrou o artifact, usar ABI mínimo
        logger.warning("⚠️ Artifact não encontrado, usando ABI mínimo")
        return self._get_minimal_abi()
    
    def _get_minimal_abi(self) -> List[Dict]:
        """Retorna ABI mínimo para funções essenciais"""
        return [
            {
                "inputs": [
                    {"internalType": "string", "name": "_predictionId", "type": "string"},
                    {"internalType": "string", "name": "_modelId", "type": "string"},
                    {"internalType": "string", "name": "_prediction", "type": "string"},
                    {"internalType": "uint256", "name": "_confidence", "type": "uint256"}
                ],
                "name": "storePrediction",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [{"internalType": "string", "name": "_predictionId", "type": "string"}],
                "name": "getPrediction",
                "outputs": [
                    {"internalType": "string", "name": "modelId", "type": "string"},
                    {"internalType": "string", "name": "prediction", "type": "string"},
                    {"internalType": "uint256", "name": "confidence", "type": "uint256"},
                    {"internalType": "uint256", "name": "timestamp", "type": "uint256"},
                    {"internalType": "address", "name": "oracle", "type": "address"}
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
    
    def get_wallet_balance(self) -> float:
        """Retorna o saldo da carteira em ETH"""
        balance_wei = self.w3.eth.get_balance(self.account.address)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')
        return float(balance_eth)
    
    def estimate_gas_price(self) -> int:
        """Estima o preço do gas atual"""
        gas_price = self.w3.eth.gas_price
        max_gas = self.w3.to_wei(os.getenv('MAX_GAS_PRICE_GWEI', '50'), 'gwei')
        
        return min(gas_price, max_gas)
    
    def store_prediction(
        self,
        prediction_id: str,
        model_id: str,
        prediction: str,
        confidence: float
    ) -> Dict[str, Any]:
        """
        Armazena uma previsão no blockchain
        
        Args:
            prediction_id: ID único da previsão
            model_id: ID do modelo ML utilizado
            prediction: Resultado da previsão (JSON string)
            confidence: Confiança da previsão (0-100)
        
        Returns:
            Dict com transaction hash e receipt
        """
        try:
            # Converter confidence para uint256 (0-10000 = 0-100.00%)
            confidence_uint = int(confidence * 100)
            
            # Construir transação
            transaction = self.contract.functions.storePrediction(
                prediction_id,
                model_id,
                prediction,
                confidence_uint
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': int(os.getenv('GAS_LIMIT', '500000')),
                'gasPrice': self.estimate_gas_price(),
            })
            
            # Assinar transação
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=self.account.key
            )
            
            # Enviar transação
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            logger.info(f"📤 Transação enviada: {tx_hash.hex()}")
            logger.info(f"🔍 Etherscan: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
            
            # Aguardar confirmação
            logger.info("⏳ Aguardando confirmação...")
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if tx_receipt['status'] == 1:
                logger.info(f"✅ Previsão armazenada com sucesso!")
                logger.info(f"⛽ Gas usado: {tx_receipt['gasUsed']}")
            else:
                logger.error("❌ Transação falhou!")
            
            return {
                'success': tx_receipt['status'] == 1,
                'tx_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'gas_used': tx_receipt['gasUsed'],
                'prediction_id': prediction_id
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao armazenar previsão: {str(e)}")
            raise
    
    def get_prediction(self, prediction_id: str) -> Dict[str, Any]:
        """
        Recupera uma previsão do blockchain
        
        Args:
            prediction_id: ID da previsão
        
        Returns:
            Dict com os dados da previsão
        """
        try:
            result = self.contract.functions.getPrediction(prediction_id).call()
            
            prediction_data = {
                'prediction_id': prediction_id,
                'model_id': result[0],
                'prediction': result[1],
                'confidence': result[2] / 100,  # Converter de uint para float
                'timestamp': result[3],
                'oracle_address': result[4]
            }
            
            logger.info(f"✅ Previsão recuperada: {prediction_id}")
            
            return prediction_data
            
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar previsão: {str(e)}")
            raise
    
    def get_network_info(self) -> Dict[str, Any]:
        """Retorna informações da rede"""
        return {
            'network': os.getenv('NETWORK', 'sepolia'),
            'chain_id': self.w3.eth.chain_id,
            'latest_block': self.w3.eth.block_number,
            'gas_price_gwei': self.w3.from_wei(self.w3.eth.gas_price, 'gwei'),
            'wallet_address': self.account.address,
            'wallet_balance_eth': self.get_wallet_balance(),
            'contract_address': self.contract.address
        }


# Função auxiliar para testes rápidos
def main():
    """Teste rápido do ContractManager"""
    try:
        manager = ContractManager()
        
        print("\n" + "="*60)
        print("🔷 DECAI ORACLE - CONTRACT MANAGER TEST")
        print("="*60)
        
        # Informações da rede
        info = manager.get_network_info()
        print(f"\n📡 Network: {info['network']}")
        print(f"🔗 Chain ID: {info['chain_id']}")
        print(f"📦 Latest Block: {info['latest_block']}")
        print(f"⛽ Gas Price: {info['gas_price_gwei']:.2f} Gwei")
        print(f"💼 Wallet: {info['wallet_address']}")
        print(f"💰 Balance: {info['wallet_balance_eth']:.4f} ETH")
        print(f"📍 Contract: {info['contract_address']}")
        
        print("\n✅ ContractManager funcionando corretamente!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")
        raise


if __name__ == "__main__":
    main()
