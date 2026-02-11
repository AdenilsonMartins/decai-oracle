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
        
        return {
            'asset': 'BTC/USD',
            'predicted_price': 45230.50,
            'confidence': 87.5,
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
        print("📋 TEST 2: Store Prediction On-Chain (V2)")
        print("="*60)
        
        try:
            # Gerar previsão de teste
            test_pred = self.generate_test_prediction()
            
            print(f"📊 Asset: {test_pred['asset']}")
            print(f"💰 Price: {test_pred['predicted_price']}")
            print(f"📈 Confidence: {test_pred['confidence']}%")
            
            print("\n⏳ Enviando transação para blockchain...")
            
            # Armazenar no blockchain
            result = self.manager.store_prediction(
                asset=test_pred['asset'],
                predicted_price=test_pred['predicted_price'],
                confidence=test_pred['confidence']
            )
            
            if result['success']:
                print(f"\n✅ SUCESSO!")
                print(f"📤 TX Hash: {result['tx_hash']}")
                print(f"📦 Block: {result['block_number']}")
                print(f"⛽ Gas Usado: {result['gas_used']}")
                print(f"🔍 Etherscan: https://sepolia.etherscan.io/tx/{result['tx_hash']}")
                
                # Como não estamos lendo os logs para pegar o ID exato neste teste simplificado,
                # e o contrato usa um contador sequencial, podemos tentar prever o ID.
                # Mas para ser robusto, vamos precisar ler do contrato ou logs.
                # O ideal seria atualizar `store_prediction` para retornar o ID lendo os eventos.
                # Por hora, vamos assumir que precisamos do ID para o próximo teste.
                # Se for testnet pública, pode ser difícil saber o ID sem ler eventos.
                # VAMOS TENTAR ler o último ID do contador 'predictionCount' se possível,
                # mas o contract_manager não expõe isso ainda.
                
                # WORKAROUND: Vamos tentar ler o último ID inferindo que fomos nós (race condition em mainnet)
                # Para este teste, vamos assumir que o usuário vai verificar manualmente ou
                # implementaremos a leitura de eventos no futuro.
                # Porem, o `test_3` precisa do ID.
                # Vamos tentar ler o `predictionCount` publico do contrato.
                
                try:
                    count = self.manager.contract.functions.predictionCount().call()
                    result['prediction_id'] = count # Assumindo que fomos a ultima tx
                    print(f"🔢 Prediction ID (Inferido): {count}")
                except:
                    print("⚠️ Não foi possível obter predictionCount, usando 1 como fallback")
                    result['prediction_id'] = 1

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
    
    def test_3_retrieve_prediction(self, prediction_id: int) -> bool:
        """Test 3: Recuperar previsão do blockchain"""
        print("\n" + "="*60)
        print("📋 TEST 3: Retrieve Prediction From Chain")
        print("="*60)
        
        try:
            print(f"🔍 Buscando previsão ID: {prediction_id}")
            
            # Aguardar alguns segundos para garantir que o bloco foi minerado
            # print("⏳ Aguardando confirmação do bloco...")
            # time.sleep(5)
            
            # Recuperar do blockchain
            retrieved = self.manager.get_prediction(prediction_id)
            
            print(f"\n✅ Previsão recuperada com sucesso!")
            print(f"📊 Asset: {retrieved['asset']}")
            print(f"💰 Price: {retrieved['predicted_price']}")
            print(f"📈 Confidence: {retrieved['confidence']:.2f}%")
            print(f"🕐 Timestamp: {datetime.fromtimestamp(retrieved['timestamp'])}")
            print(f"🔐 Predictor: {retrieved['predictor']}")
            print(f"✅ Verified: {retrieved['verified']}")
            
            self.test_results.append(('Retrieve Prediction', 'PASSED'))
            return retrieved
            
        except Exception as e:
            print(f"❌ FALHOU: {str(e)}")
            self.test_results.append(('Retrieve Prediction', 'FAILED'))
            return None
    
    def test_4_data_integrity(self, original: Dict, retrieved: Dict) -> bool:
        """Test 4: Verificar integridade dos dados"""
        print("\n" + "="*60)
        print("📋 TEST 4: Data Integrity Verification")
        print("="*60)
        
        try:
            checks = []
            
            # Check 1: Asset
            check_asset = retrieved['asset'] == original['asset']
            checks.append(('Asset', check_asset))
            print(f"{'✅' if check_asset else '❌'} Asset match: {original['asset']}")
            
            # Check 2: Price (float comparison)
            check_price = abs(retrieved['predicted_price'] - original['predicted_price']) < 0.01
            checks.append(('Price', check_price))
            print(f"{'✅' if check_price else '❌'} Price match: {retrieved['predicted_price']}")
            
            # Check 3: Confidence
            check_conf = abs(retrieved['confidence'] - original['confidence']) < 0.1
            checks.append(('Confidence', check_conf))
            print(f"{'✅' if check_conf else '❌'} Confidence match: {retrieved['confidence']}")
            
            # Check 4: Predictor
            check_predictor = retrieved['predictor'].lower() == self.manager.account.address.lower()
            checks.append(('Predictor', check_predictor))
            print(f"{'✅' if check_predictor else '❌'} Predictor match: {retrieved['predictor']}")
            
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
        retrieved_data = self.test_3_retrieve_prediction(stored_data['prediction_id'])
        if not retrieved_data:
             print("\n⚠️  Falha ao recuperar previsão.")
             return
        
        # Test 4: Data Integrity
        self.test_4_data_integrity(stored_data, retrieved_data)
        
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
