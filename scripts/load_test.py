import asyncio
import aiohttp
import time
import statistics
from datetime import datetime

API_URL = "http://localhost:8000/api/v2/predict"
CONCURRENT_REQUESTS = 5
TOTAL_REQUESTS = 20

async def make_request(session, request_id):
    start = time.time()
    payload = {"asset_id": "bitcoin", "days_back": 30}
    try:
        async with session.post(API_URL, json=payload) as response:
            status = response.status
            data = await response.json()
            duration = time.time() - start
            return {
                "id": request_id,
                "status": status,
                "duration": duration,
                "cached": "cache hit" in str(data).lower() or duration < 0.1 # Simplificação para detecção de cache
            }
    except Exception as e:
        return {"id": request_id, "status": "error", "duration": time.time() - start, "error": str(e)}

async def run_load_test():
    print(f"🚀 Iniciando Teste de Carga: {TOTAL_REQUESTS} requisições...")
    print(f"🔗 URL: {API_URL}")
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(TOTAL_REQUESTS):
            tasks.append(make_request(session, i))
            if len(tasks) >= CONCURRENT_REQUESTS:
                # Controlar concorrência básica
                results = await asyncio.gather(*tasks)
                tasks = []
                # Pequena pausa entre batches
                time.sleep(0.5)
    
    # Analisar resultados
    durations = [r['duration'] for r in results if r['status'] == 200]
    errors = [r for r in results if r['status'] != 200]
    
    print("\n" + "="*40)
    print("📊 RESULTADOS DO TESTE DE CARGA")
    print("="*40)
    print(f"Total: {TOTAL_REQUESTS}")
    print(f"Sucesso: {len(durations)}")
    print(f"Erros/Rate Limits: {len(errors)}")
    
    if durations:
        print(f"Latência Média: {statistics.mean(durations):.3f}s")
        print(f"Latência Mínima: {min(durations):.3f}s (Provável Cache)")
        print(f"Latência Máxima: {max(durations):.3f}s")
    
    if errors:
        print("\nExemplos de Erros:")
        for e in errors[:3]:
            print(f"  - Status {e['status']}: {e.get('error', 'Rate Limited?')}")
    
    print("="*40)

if __name__ == "__main__":
    # Nota: A API deve estar rodando para este teste funcionar
    try:
        asyncio.run(run_load_test())
    except ConnectionError:
        print("❌ Erro: API não está rodando. Inicie com 'python src/api/main.py' primeiro.")
