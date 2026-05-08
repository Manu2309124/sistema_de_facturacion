#!/bin/bash
# Script para configurar rápidamente el Sistema de Facturación

echo "======================================================"
echo "CONFIGURACIÓN RÁPIDA - SISTEMA DE FACTURACIÓN"
echo "======================================================"
echo ""

# 1. Crear entorno virtual
echo "📦 Creando entorno virtual..."
python -m venv venv

# 2. Activar entorno virtual
echo "✓ Activando entorno virtual..."
source venv/Scripts/activate  # Windows
# source venv/bin/activate    # Mac/Linux

# 3. Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# 4. Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p instance
mkdir -p data
mkdir -p logs

# 5. Inicializar base de datos
echo "🗄️ Inicializando base de datos..."
python manage_db.py init

# 6. Cargar datos de prueba
echo "🌱 Cargando datos de prueba..."
python manage_db.py seed

# 7. Ver información
echo ""
echo "📊 Información de la Base de Datos:"
python manage_db.py info

echo ""
echo "======================================================"
echo "✅ CONFIGURACIÓN COMPLETADA"
echo "======================================================"
echo ""
echo "Próximos pasos:"
echo "1. Ejecutar servidor: python run.py"
echo "2. Acceder a API: http://localhost:5000/api/customers"
echo "3. Ver logs SQL: Configurado en SQLALCHEMY_ECHO"
echo ""
