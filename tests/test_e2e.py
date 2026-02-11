"""
DecAI Oracle - End-to-End Test Suite
Versão 1.0

Testa o fluxo completo:
1. Gerar previsão ML
2. Armazenar no blockchain
3. Recuperar e validar dados
4. Verificar no Etherscan
"""

import json
import time
import hashlib
from datetime import datetime
from typing import Dict, Any
import sys
from pathlib import Path

# Adicionar path do projeto
# Adicionar a pasta raiz ao sys.path
sys.path.append(str(Path(__file__).parent.parent))
from src.blockchain.contract_manager import ContractManager


class EndToEndTester:
    """Suite de testes end-to-end para DecAI Oracle"""
    
    def __init__(self):
        self.manager = ContractManager()
        self.test_results = []
    
    def generate_test_prediction(self) -> Dict[str, Any]:
        """Gera uma previsão de teste simulada"""
        timestamp = datetime.now().isoformat()
        
        # Simular dados de uma previsão real
        prediction_data = {
            'symbol': 'BTC/USD',
            'predicted_price': 45230.50,
            'predicted_trend': 'bullish',
            'time_horizon': '24h',
            'features_used': ['price', 'volume', 'sentiment'],
            'model_version': 'v1.2.3'
        }
        
        # Gerar ID único
        prediction_id = hashlib.sha256(
            f"{timestamp}{json.dumps(prediction_data)}".encode()
        ).hexdigest()[:16]
        
        return {
            'prediction_id': prediction_id,
            'model_id': 'btc_price_predictor_v1',
            'prediction': json.dumps(prediction_data),
            'confidence': 87.5,  # 87.5%
            'timestamp': timestamp
        }
    
    def test_1_connection(self) -> bool:
        """Test 1: Verificar conexão com a rede"""
        print("\n" + "="*60)
        print("📋 TEST 1: Network Connection")
        print("="*60)
        
        try:
            info = self.manager.get_network_info()
            
            print(f"✅ Conectado à rede: {info['network']}")
            print(f"✅ Chain ID: {info['chain_id']}")
            print(f"✅ Último bloco: {info['latest_block']}")
            print(f"✅ Saldo da carteira: {info['wallet_balance_eth']:.4f} ETH")
            
            # Verificar se tem saldo suficiente
            if info['wallet_balance_eth'] < 0.001:
                print("⚠️  AVISO: Saldo baixo! Pode não ter ETH suficiente para transações.")
                return False
            
            self.test_results.append(('Connection Test', 'PASSED'))
            return True
            
        except Exception as e:
            print(f"❌ FALHOU: {str(e)}")
            self.test_results.append(('Connection Test', 'FAILED'))
            return False
    
    def test_2_store_prediction(self) -> Dict[str, Any]:
        """Test 2: Armazenar previsão no blockchain"""
        print("\n" + "="*60)
        print("📋 TEST 2: Store Prediction On-Chain")
        print("="*60)
        
        try:
            # Gerar previsão de teste
            test_pred = self.generate_test_prediction()
            
            print(f"📊 Prediction ID: {test_pred['prediction_id']}")
            print(f"🤖 Model ID: {test_pred['model_id']}")
            print(f"📈 Confidence: {test_pred['confidence']}%")
            print(f"📝 Data: {test_pred['prediction'][:100]}...")
            
            print("\n⏳ Enviando transação para blockchain...")
            
            # Armazenar no blockchain
            result = self.manager.store_prediction(
                prediction_id=test_pred['prediction_id'],
                model_id=test_pred['model_id'],
                prediction=test_pred['prediction'],
                confidence=test_pred['confidence']
            )
            
            if result['success']:
                print(f"\n✅ SUCESSO!")
                print(f"📤 TX Hash: {result['tx_hash']}")
                print(f"📦 Block: {result['block_number']}")
                print(f"⛽ Gas Usado: {result['gas_used']}")
                print(f"🔍 Etherscan: https://sepolia.etherscan.io/tx/{result['tx_hash']}")
                
                self.test_results.append(('Store Prediction', 'PASSED'))
                return {**test_pred, **result}
            else:
                print("❌ Transação falhou!")
                self.test_results.append(('Store Prediction', 'FAILED'))
                return None
                
        except Exception as e:
            print(f"❌ FALHOU: {str(e)}")
            self.test_results.append(('Store Prediction', 'FAILED'))
            return None
    
    def test_3_retrieve_prediction(self, prediction_id: str) -> bool:
        """Test 3: Recuperar previsão do blockchain"""
        print("\n" + "="*60)
        print("📋 TEST 3: Retrieve Prediction From Chain")
        print("="*60)
        
        try:
            print(f"🔍 Buscando previsão: {prediction_id}")
            
            # Aguardar alguns segundos para garantir que o bloco foi minerado
            print("⏳ Aguardando confirmação do bloco...")
            time.sleep(5)
            
            # Recuperar do blockchain
            retrieved = self.manager.get_prediction(prediction_id)
            
            print(f"\n✅ Previsão recuperada com sucesso!")
            print(f"📊 Prediction ID: {retrieved['prediction_id']}")
            print(f"🤖 Model ID: {retrieved['model_id']}")
            print(f"📈 Confidence: {retrieved['confidence']:.2f}%")
            print(f"🕐 Timestamp: {datetime.fromtimestamp(retrieved['timestamp'])}")
            print(f"🔐 Oracle: {retrieved['oracle_address']}")
            print(f"📝 Prediction Data:")
            
            # Parse e mostrar dados da previsão
            pred_data = json.loads(retrieved['prediction'])
            for key, value in pred_data.items():
                print(f"   - {key}: {value}")
            
            self.test_results.append(('Retrieve Prediction', 'PASSED'))
            return True
            
        except Exception as e:
            print(f"❌ FALHOU: {str(e)}")
            self.test_results.append(('Retrieve Prediction', 'FAILED'))
            return False
    
    def test_4_data_integrity(self, original: Dict, prediction_id: str) -> bool:
        """Test 4: Verificar integridade dos dados"""
        print("\n" + "="*60)
        print("📋 TEST 4: Data Integrity Verification")
        print("="*60)
        
        try:
            # Recuperar dados
            retrieved = self.manager.get_prediction(prediction_id)
            
            # Verificações
            checks = []
            
            # Check 1: Prediction ID
            check_id = retrieved['prediction_id'] == prediction_id
            checks.append(('Prediction ID', check_id))
            print(f"{'✅' if check_id else '❌'} Prediction ID: {check_id}")
            
            # Check 2: Model ID
            check_model = retrieved['model_id'] == original['model_id']
            checks.append(('Model ID', check_model))
            print(f"{'✅' if check_model else '❌'} Model ID: {check_model}")
            
            # Check 3: Prediction Data
            check_data = retrieved['prediction'] == original['prediction']
            checks.append(('Prediction Data', check_data))
            print(f"{'✅' if check_data else '❌'} Prediction Data: {check_data}")
            
            # Check 4: Confidence (com margem de erro)
            check_conf = abs(retrieved['confidence'] - original['confidence']) < 0.1
            checks.append(('Confidence', check_conf))
            print(f"{'✅' if check_conf else '❌'} Confidence: {check_conf}")
            
            # Check 5: Oracle Address
            check_oracle = retrieved['oracle_address'].lower() == self.manager.account.address.lower()
            checks.append(('Oracle Address', check_oracle))
            print(f"{'✅' if check_oracle else '❌'} Oracle Address: {check_oracle}")
            
            all_passed = all(check[1] for check in checks)
            
            if all_passed:
                print("\n✅ INTEGRIDADE DOS DADOS VERIFICADA!")
                self.test_results.append(('Data Integrity', 'PASSED'))
            else:
                print("\n⚠️  ALGUNS CHECKS FALHARAM!")
                self.test_results.append(('Data Integrity', 'FAILED'))
            
            return all_passed
            
        except Exception as e:
            print(f"❌ FALHOU: {str(e)}")
            self.test_results.append(('Data Integrity', 'FAILED'))
            return False
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for _, status in self.test_results if status == 'PASSED')
        total = len(self.test_results)
        
        for test_name, status in self.test_results:
            emoji = "✅" if status == "PASSED" else "❌"
            print(f"{emoji} {test_name}: {status}")
        
        print("\n" + "-"*60)
        print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
        print("="*60)
        
        if passed == total:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("✅ Sistema está funcionando corretamente!")
        else:
            print("\n⚠️  ALGUNS TESTES FALHARAM!")
            print("❌ Revisar logs acima para detalhes")
    
    def run_all_tests(self):
        """Executa todos os testes em sequência"""
        print("\n" + "="*60)
        print("🚀 DECAI ORACLE - END-TO-END TEST SUITE")
        print("="*60)
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Network: Sepolia Testnet")
        print(f"Contract: {self.manager.contract.address}")
        print("="*60)
        
        # Test 1: Connection
        if not self.test_1_connection():
            print("\n❌ Teste de conexão falhou. Abortando suite.")
            return
        
        # Test 2: Store Prediction
        stored_data = self.test_2_store_prediction()
        if not stored_data:
            print("\n❌ Falha ao armazenar previsão. Abortando suite.")
            return
        
        # Test 3: Retrieve Prediction
        if not self.test_3_retrieve_prediction(stored_data['prediction_id']):
            print("\n⚠️  Falha ao recuperar previsão.")
        
        # Test 4: Data Integrity
        self.test_4_data_integrity(stored_data, stored_data['prediction_id'])
        
        # Summary
        self.print_summary()


def main():
    """Função principal"""
    try:
        tester = EndToEndTester()
        tester.run_all_tests()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal: {str(e)}")
        raise


if __name__ == "__main__":
    main()
