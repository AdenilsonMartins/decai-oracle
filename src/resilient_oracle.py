"""
DecAI Oracle - Exemplo de Integração Completa
Versão 2.0

Fluxo completo resiliente:
1. Buscar dados de múltiplas fontes
2. Validar consenso
3. Gerar previsão ML
4. Armazenar on-chain
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

from data_aggregator import MultiSourceAggregator
from contract_manager_v2 import ContractManager


class ResilientOracleSystem:
    """Sistema completo de oráculo com múltiplas fontes"""
    
    def __init__(self):
        self.aggregator = MultiSourceAggregator()
        self.contract_manager = ContractManager()
        self.predictions_count = 0
    
    async def generate_prediction(self, symbol: str) -> Dict[str, Any]:
        """
        Gera previsão baseada em dados de múltiplas fontes
        
        Flow:
        1. Busca preço atual (multi-source)
        2. Valida consenso
        3. Aplica modelo ML (simulado aqui)
        4. Retorna previsão
        """
        print(f"\n{'='*60}")
        print(f"🔮 Gerando previsão para {symbol}")
        print("="*60)
        
        # STEP 1: Obter preço atual com agregação
        print("\n📊 STEP 1: Buscando dados de múltiplas fontes...")
        current_price_data = await self.aggregator.get_price(
            symbol=symbol,
            min_sources=2,  # Requer pelo menos 2 fontes
            max_deviation=5.0  # Máximo 5% de diferença entre fontes
        )
        
        if not current_price_data:
            print("❌ Falha ao obter dados confiáveis!")
            return None
        
        print(f"✅ Preço atual: ${current_price_data.price:,.2f}")
        print(f"✅ Fontes usadas: {current_price_data.metadata['sources_used']}")
        print(f"✅ Confiança dos dados: {current_price_data.confidence:.1f}%")
        
        # STEP 2: Simular modelo ML
        print("\n🤖 STEP 2: Aplicando modelo de Machine Learning...")
        
        # Aqui você integraria seu modelo real
        # Por enquanto, simulação simples baseada em tendência
        predicted_price = current_price_data.price * 1.02  # Simulação: +2%
        prediction_confidence = current_price_data.confidence * 0.95  # Ajustar por incerteza do modelo
        
        prediction_data = {
            'symbol': symbol,
            'current_price': current_price_data.price,
            'predicted_price': predicted_price,
            'predicted_change_pct': 2.0,
            'time_horizon': '24h',
            'prediction_confidence': prediction_confidence,
            'model_version': 'v2.0-resilient',
            'data_sources': current_price_data.metadata['sources_used'],
            'data_quality': {
                'num_sources': current_price_data.metadata['num_sources'],
                'price_deviation_pct': current_price_data.metadata['price_deviation_pct'],
                'data_confidence': current_price_data.confidence
            },
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"✅ Previsão: ${predicted_price:,.2f} (+2.0%)")
        print(f"✅ Confiança da previsão: {prediction_confidence:.1f}%")
        print(f"✅ Qualidade dos dados: {current_price_data.metadata['num_sources']} fontes")
        
        return prediction_data
    
    async def store_prediction_on_chain(self, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Armazena previsão no blockchain
        
        Args:
            prediction: Dados da previsão
        
        Returns:
            Resultado da transação
        """
        print("\n⛓️  STEP 3: Armazenando previsão on-chain...")
        
        self.predictions_count += 1
        prediction_id = f"pred_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self.predictions_count}"
        
        try:
            result = self.contract_manager.store_prediction(
                prediction_id=prediction_id,
                model_id=prediction['model_version'],
                prediction=json.dumps(prediction),
                confidence=prediction['prediction_confidence']
            )
            
            if result['success']:
                print(f"✅ Previsão armazenada on-chain!")
                print(f"📤 TX: {result['tx_hash']}")
                print(f"🔍 Etherscan: https://sepolia.etherscan.io/tx/{result['tx_hash']}")
                
                # Adicionar metadados de blockchain
                prediction['blockchain'] = {
                    'tx_hash': result['tx_hash'],
                    'block_number': result['block_number'],
                    'prediction_id': prediction_id
                }
            
            return result
            
        except Exception as e:
            print(f"❌ Erro ao armazenar on-chain: {str(e)}")
            return None
    
    async def run_prediction_cycle(self, symbols: list):
        """
        Executa ciclo completo de previsões para múltiplos símbolos
        
        Args:
            symbols: Lista de símbolos para prever
        """
        print("\n" + "="*60)
        print("🚀 DECAI ORACLE - PREDICTION CYCLE")
        print("="*60)
        print(f"Símbolos: {symbols}")
        print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        results = []
        
        for symbol in symbols:
            # Gerar previsão
            prediction = await self.generate_prediction(symbol)
            
            if prediction:
                # Armazenar on-chain
                tx_result = await self.store_prediction_on_chain(prediction)
                
                results.append({
                    'symbol': symbol,
                    'prediction': prediction,
                    'blockchain_result': tx_result,
                    'success': tx_result is not None and tx_result.get('success', False)
                })
            else:
                results.append({
                    'symbol': symbol,
                    'prediction': None,
                    'blockchain_result': None,
                    'success': False
                })
            
            # Pequeno delay entre previsões
            await asyncio.sleep(2)
        
        # Relatório final
        self.print_cycle_summary(results)
        
        return results
    
    def print_cycle_summary(self, results: list):
        """Imprime resumo do ciclo de previsões"""
        print("\n" + "="*60)
        print("📊 CYCLE SUMMARY")
        print("="*60)
        
        successful = sum(1 for r in results if r['success'])
        total = len(results)
        
        for result in results:
            emoji = "✅" if result['success'] else "❌"
            print(f"{emoji} {result['symbol']}: {'SUCCESS' if result['success'] else 'FAILED'}")
            
            if result['success']:
                pred = result['prediction']
                print(f"   Predicted: ${pred['predicted_price']:,.2f} ({pred['predicted_change_pct']:+.1f}%)")
                print(f"   Sources: {len(pred['data_sources'])}")
                print(f"   TX: {result['blockchain_result']['tx_hash'][:16]}...")
        
        print("\n" + "─"*60)
        print(f"Total: {successful}/{total} predictions successful ({successful/total*100:.0f}%)")
        
        # Health report
        print("\n" + "─"*60)
        print("🏥 DATA SOURCES HEALTH")
        print("─"*60)
        
        health = self.aggregator.get_health_report()
        print(f"Healthy sources: {health['healthy_sources']}/{health['total_sources']}")
        
        for source in health['sources']:
            status_emoji = {'healthy': '✅', 'degraded': '⚠️', 'down': '❌'}
            emoji = status_emoji.get(source['status'], '❓')
            print(f"{emoji} {source['name']}: {source['success_rate']} success rate")
        
        print("="*60)


async def main():
    """Exemplo de uso completo"""
    
    # Criar sistema
    oracle = ResilientOracleSystem()
    
    # Executar ciclo de previsões
    symbols = ['BTC/USD', 'ETH/USD']
    
    results = await oracle.run_prediction_cycle(symbols)
    
    print("\n✅ Ciclo completo finalizado!")
    print(f"📊 {len(results)} previsões processadas")


if __name__ == "__main__":
    asyncio.run(main())
