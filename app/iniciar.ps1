param([ValidateRange(1024,65535)][int]$Port = 8766)
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $personaPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $personaPython)) {
        $personaBasePython = (Get-Command python -ErrorAction Stop).Source
        & $personaBasePython -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Não foi possível preparar o ambiente.' }
        & $personaPython -m pip install -r requirements.lock.txt
        if ($LASTEXITCODE -ne 0) { throw 'Não foi possível instalar as dependências.' }
    }
    if (-not (Test-Path -LiteralPath 'dist/index.html')) {
        & npm.cmd ci
        if ($LASTEXITCODE -ne 0) { throw 'Não foi possível preparar a interface.' }
        & npm.cmd run build
        if ($LASTEXITCODE -ne 0) { throw 'Não foi possível montar a interface.' }
    }
    try { $personaHealth = Invoke-RestMethod "http://127.0.0.1:$Port/api/health" -TimeoutSec 2 } catch { $personaHealth = $null }
    if ($personaHealth -and $personaHealth.version -eq '5.0' -and $personaHealth.cards -eq 141) {
        Write-Output "Persona Cards já está disponível em http://127.0.0.1:$Port"
        return
    }
    New-Item -ItemType Directory -Force .runtime | Out-Null
    $personaProcess = Start-Process -FilePath $personaPython -ArgumentList '-m','uvicorn','server:app','--host','127.0.0.1','--port',"$Port" -WorkingDirectory $PSScriptRoot -WindowStyle Hidden -PassThru -RedirectStandardOutput .runtime/server.log -RedirectStandardError .runtime/server-error.log
    $personaProcess.Id | Set-Content .runtime/server.pid
    $personaReady = $false
    for ($personaAttempt = 0; $personaAttempt -lt 20; $personaAttempt++) {
        try {
            $personaHealth = Invoke-RestMethod "http://127.0.0.1:$Port/api/health" -TimeoutSec 1
            if ($personaHealth.version -eq '5.0' -and $personaHealth.cards -eq 141) { $personaReady = $true; break }
        } catch { }
        if ($personaProcess.HasExited) { break }
        Start-Sleep -Milliseconds 250
    }
    if (-not $personaReady) { throw 'O servidor não iniciou. Consulte .runtime/server-error.log; a porta pode estar ocupada.' }
    Write-Output "Persona Cards disponível em http://127.0.0.1:$Port"
} finally { Pop-Location }
