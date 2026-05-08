@echo off
REM Script para configurar rápidamente el Sistema de Facturación (Windows)

echo.
echo ======================================================
echo CONFIGURACION RAPIDA - SISTEMA DE FACTURACION
echo ======================================================
echo.

REM 1. Crear entorno virtual
echo 1. Creando entorno virtual...
python -m venv venv

REM 2. Activar entorno virtual
echo 2. Activando entorno virtual...
call venv\Scripts\activate.bat

REM 3. Instalar dependencias
echo 3. Instalando dependencias...
pip install -r requirements.txt

REM 4. Crear directorios necesarios
echo 4. Creando directorios...
if not exist instance mkdir instance
if not exist data mkdir data
if not exist logs mkdir logs

REM 5. Inicializar base de datos
echo 5. Inicializando base de datos...
python manage_db.py init

REM 6. Cargar datos de prueba
echo 6. Cargando datos de prueba...
python manage_db.py seed

REM 7. Ver información
echo.
echo 7. Informacion de la Base de Datos:
python manage_db.py info

echo.
echo ======================================================
echo CONFIGURACION COMPLETADA
echo ======================================================
echo.
echo Proximos pasos:
echo 1. Ejecutar servidor: python run.py
echo 2. Acceder a API: http://localhost:5000/api/customers
echo 3. Ver logs SQL: Configurado en SQLALCHEMY_ECHO
echo.
echo Presiona cualquier tecla para continuar...
pause > nul
