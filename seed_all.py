#!/usr/bin/env python
"""
Script maestro para cargar todos los datos de prueba consistentes.
Carga usuarios y pacientes con datos fijos.

Ejecutar: python seed_all.py
"""

import os
import subprocess
import sys

def run_script(script_name, description):
    """Ejecuta un script de seed"""
    print(f"\n{'='*70}")
    print(f"📌 {description}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            cwd=os.path.dirname(os.path.abspath(__file__)),
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando {script_name}: {e}")
        return False

def main():
    """Ejecuta todos los scripts de seed"""
    print("\n" + "="*70)
    print("🚀 INICIANDO CARGA DE DATOS DE PRUEBA CONSISTENTES")
    print("="*70)
    
    # Paso 1: Cargar usuarios
    if not run_script('seed_users.py', 'PASO 1: Cargando Usuarios'):
        print("❌ Error en carga de usuarios")
        sys.exit(1)
    
    # Paso 2: Cargar pacientes
    if not run_script('seed_patients.py', 'PASO 2: Cargando Pacientes'):
        print("❌ Error en carga de pacientes")
        sys.exit(1)
    
    # Resumen final
    print("\n" + "="*70)
    print("✅ TODOS LOS DATOS DE PRUEBA HAN SIDO CARGADOS EXITOSAMENTE")
    print("="*70)
    print("\n📝 RESUMEN DE USUARIOS Y CONTRASEÑAS:")
    print("-" * 70)
    print("Contraseña universal para todos: Test1234!")
    print("\nUsuarios disponibles:")
    print("  1. Carlos García (Médico Radiólogo) - medico1@hospital.com")
    print("  2. María Rodríguez (Médica Radiólogo) - medico2@hospital.com")
    print("  3. Juan Pérez (Técnico Salud) - tecnico1@hospital.com")
    print("  4. Ana López (Técnica Salud) - tecnico2@hospital.com")
    print("  5. Pedro Martínez (Administrador) - admin@hospital.com")
    print("\n💡 PRÓXIMOS PASOS:")
    print("  1. Iniciar servidor: python manage.py runserver")
    print("  2. Acceder a: http://127.0.0.1:8000")
    print("  3. Usar cualquiera de los emails/contraseñas listados arriba")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
