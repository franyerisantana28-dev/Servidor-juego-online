@echo off
title Servidor Multijugador Isla Salvaje - Santana Studio
color 0A
echo ========================================================
echo       ISLA SALVAJE - SERVIDOR MULTIJUGADOR PERSISTENTE
echo               Santana Studio (c) 2026
echo ========================================================
echo.
echo Inicializando Base de Datos SQLite WAL...
python "%~dp0database.py"
echo.
echo Iniciando Servidor REST y Sincronizacion de Jugadores en puerto 8080...
echo [Presione Ctrl+C para detener el servidor]
echo.
python "%~dp0server.py"
pause
