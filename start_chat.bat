@echo off
chcp 65001 >nul
title Planificateur de Voyage

echo.
echo  Demarrage du Planificateur de Voyage...
echo  -----------------------------------------
echo.

:: Lancer le serveur unifie (API + Interface Web sur port 8080)
start "Serveur Travel Agent" cmd /k "cd /d %~dp0 && uv run python server.py"

:: Attendre que le serveur demarre
echo  En attente du demarrage du serveur (5 secondes)...
timeout /t 5 /nobreak >nul

:: Ouvrir l'interface dans le navigateur
echo  Ouverture de l'interface...
start "" "http://localhost:8080/"

echo.
echo  L'interface est ouverte !
echo  Pour arreter : fermez la fenetre "Serveur Travel Agent"
echo.
pause
