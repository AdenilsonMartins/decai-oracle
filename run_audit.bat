@echo off
echo ========================================================
echo 🛡️  INICIANDO AUDITORIA DE SEGURANCA (DecAI Oracle)
echo ========================================================
echo.
echo [1/2] Construindo imagem de auditoria (Isso pode demorar na primeira vez)...
docker build -t decai-audit -f Dockerfile.audit .

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Falha ao construir a imagem Docker. Verifique se o Docker Desktop esta aberto.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Executando analise de seguranca...
docker run --rm decai-audit

echo.
echo ========================================================
echo ✅ Auditoria concluida! Verifique os logs acima.
echo ========================================================
pause
