# ===========================================
# SISTEMA DE GESTIÓN DE AUTOMOTORES
# ===========================================

import datetime
import json
import os

# Lista global para almacenar propietarios
propietarios = []
DATA_FILE = "datos_automotores.json"

def load_data():
    """Carga los datos desde el archivo JSON si existe."""
    global propietarios
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                propietarios = json.load(f)
        except Exception as e:
            print(f"⚠️ No se pudo cargar el archivo de datos: {e}")
            propietarios = []
    else:
        propietarios = []

def save_data():
    """Guarda los datos actuales en el archivo JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(propietarios, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ No se pudo guardar el archivo de datos: {e}")

def mostrar_menu():
    """Muestra el menú principal del sistema"""
    print("\n" + "="*50)
    print("    🚗 SISTEMA DE GESTIÓN DE AUTOMOTORES 🚗")
    print("="*50)
    print("1. 📝 Registrar propietario")
    print("2. 🚙 Agregar vehículo")
    print("3. 📋 Listar propietarios")
    print("4. 🔧 Crear historial de mantenimiento")
    print("5. 🚪 Salir del programa")
    print("="*50)

def registrar_propietario():
    """Registra un nuevo propietario en el sistema"""
    print("\n--- REGISTRAR NUEVO PROPIETARIO ---")
    
    try:
        nombre = input("Ingrese el nombre del propietario: ").strip()
        apellido = input("Ingrese el apellido del propietario: ").strip()
        rut = input("Ingrese el RUT del propietario: ").strip()
        
        # Validar que no estén vacíos
        if not nombre or not apellido or not rut:
            print("❌ Error: Todos los campos son obligatorios.")
            return
        
        # Verificar si el RUT ya existe
        for propietario in propietarios:
            if propietario["rut"] == rut:
                print(f"❌ Error: Ya existe un propietario con el RUT {rut}")
                return
        
        # Crear el propietario
        propietario = {
            "nombre": nombre, 
            "apellido": apellido, 
            "rut": rut, 
            "vehiculos": [],
            "historial_mantenimiento": []
        }
        propietarios.append(propietario)
        save_data()
        print(f"✅ Propietario {nombre} {apellido} registrado exitosamente.")
        
    except Exception as e:
        print(f"❌ Error al registrar propietario: {e}")

def agregar_vehiculo():
    """Agrega un vehículo a un propietario existente"""
    print("\n--- AGREGAR VEHÍCULO ---")
    
    if not propietarios:
        print("❌ No hay propietarios registrados. Primero registre un propietario.")
        return
    
    try:
        rut = input("Ingrese el RUT del propietario: ").strip()
        
        # Buscar el propietario
        propietario_encontrado = None
        for propietario in propietarios:
            if propietario["rut"] == rut:
                propietario_encontrado = propietario
                break
        
        if not propietario_encontrado:
            print("❌ No se encontró el propietario con ese RUT.")
            return
        
        marca = input("Ingrese la marca del vehículo: ").strip()
        modelo = input("Ingrese el modelo del vehículo: ").strip()
        kilometraje = input("Ingrese el kilometraje actual: ").strip()
        
        if not marca or not modelo or not kilometraje:
            print("❌ Error: Todos los campos son obligatorios.")
            return
        
        # Validar que el kilometraje sea un número
        try:
            kilometraje = int(kilometraje)
            if kilometraje < 0:
                print("❌ Error: El kilometraje no puede ser negativo.")
                return
        except ValueError:
            print("❌ Error: El kilometraje debe ser un número válido.")
            return
        
        # Crear el vehículo
        vehiculo = {
            "marca": marca, 
            "modelo": modelo,
            "kilometraje": kilometraje,
            "fecha_registro": datetime.datetime.now().strftime("%d/%m/%Y")
        }
        
        propietario_encontrado["vehiculos"].append(vehiculo)
        save_data()
        print(f"✅ Vehículo '{marca} {modelo}' (Kilometraje: {kilometraje:,} km) agregado exitosamente a {propietario_encontrado['nombre']} {propietario_encontrado['apellido']}.")
        
    except Exception as e:
        print(f"❌ Error al agregar vehículo: {e}")

def listar_propietarios():
    """Lista todos los propietarios y sus vehículos"""
    print("\n--- LISTADO DE PROPIETARIOS ---")
    
    if not propietarios:
        print("📭 No hay propietarios registrados.")
        return
    
    for i, propietario in enumerate(propietarios, 1):
        print(f"\n👤 Propietario {i}:")
        print(f"   Nombre: {propietario['nombre']} {propietario['apellido']}")
        print(f"   RUT: {propietario['rut']}")
        
        if propietario['vehiculos']:
            print(f"   🚗 Vehículos ({len(propietario['vehiculos'])}):")
            for j, vehiculo in enumerate(propietario['vehiculos'], 1):
                print(f"      {j}. {vehiculo['marca']} {vehiculo['modelo']} - {vehiculo['kilometraje']:,} km (Registrado: {vehiculo['fecha_registro']})")
        else:
            print("   🚗 Sin vehículos registrados")
        
        if propietario['historial_mantenimiento']:
            print(f"   🔧 Mantenimientos registrados: {len(propietario['historial_mantenimiento'])}")
        else:
            print("   🔧 Sin mantenimientos registrados")

def crear_historial_mantenimiento():
    """Crea un historial de mantenimiento para un vehículo"""
    print("\n--- CREAR HISTORIAL DE MANTENIMIENTO ---")
    
    if not propietarios:
        print("❌ No hay propietarios registrados.")
        return
    
    try:
        rut = input("Ingrese el RUT del propietario: ").strip()
        
        # Buscar el propietario
        propietario_encontrado = None
        for propietario in propietarios:
            if propietario["rut"] == rut:
                propietario_encontrado = propietario
                break
        
        if not propietario_encontrado:
            print("❌ No se encontró el propietario con ese RUT.")
            return
        
        if not propietario_encontrado['vehiculos']:
            print("❌ Este propietario no tiene vehículos registrados.")
            return
        
        # Mostrar vehículos del propietario
        print(f"\nVehículos de {propietario_encontrado['nombre']} {propietario_encontrado['apellido']}:")
        for i, vehiculo in enumerate(propietario_encontrado['vehiculos'], 1):
            print(f"   {i}. {vehiculo['marca']} {vehiculo['modelo']} - {vehiculo['kilometraje']:,} km")
        
        # Seleccionar vehículo
        try:
            opcion_vehiculo = int(input("\nSeleccione el número del vehículo: ")) - 1
            if opcion_vehiculo < 0 or opcion_vehiculo >= len(propietario_encontrado['vehiculos']):
                print("❌ Opción inválida.")
                return
        except ValueError:
            print("❌ Por favor ingrese un número válido.")
            return
        
        vehiculo_seleccionado = propietario_encontrado['vehiculos'][opcion_vehiculo]
        
        # Obtener información del mantenimiento
        fecha_mantenimiento = input("Ingrese la fecha del mantenimiento (DD/MM/AAAA) o presione Enter para hoy: ").strip()
        if not fecha_mantenimiento:
            fecha_mantenimiento = datetime.datetime.now().strftime("%d/%m/%Y")
        
        tipo_mantenimiento = input("Ingrese el tipo de mantenimiento (ej: Cambio de aceite, Revisión general, etc.): ").strip()
        kilometraje_actual = input(f"Ingrese el kilometraje actual (actual: {vehiculo_seleccionado['kilometraje']:,} km): ").strip()
        
        # Validar kilometraje
        try:
            kilometraje_actual = int(kilometraje_actual)
            if kilometraje_actual < vehiculo_seleccionado['kilometraje']:
                print("❌ Error: El kilometraje actual no puede ser menor al registrado anteriormente.")
                return
        except ValueError:
            print("❌ Error: El kilometraje debe ser un número válido.")
            return
        
        descripcion = input("Ingrese la descripción del trabajo realizado: ").strip()
        costo = input("Ingrese el costo del mantenimiento (opcional): ").strip()
        
        # Crear el historial de mantenimiento
        mantenimiento = {
            "fecha": fecha_mantenimiento,
            "vehiculo": f"{vehiculo_seleccionado['marca']} {vehiculo_seleccionado['modelo']}",
            "kilometraje_anterior": vehiculo_seleccionado['kilometraje'],
            "kilometraje_actual": kilometraje_actual,
            "tipo_mantenimiento": tipo_mantenimiento,
            "descripcion": descripcion,
            "costo": costo if costo else "No especificado"
        }
        
        # Actualizar el kilometraje del vehículo
        vehiculo_seleccionado['kilometraje'] = kilometraje_actual
        
        propietario_encontrado['historial_mantenimiento'].append(mantenimiento)
        save_data()
        
        print(f"\n✅ Historial de mantenimiento creado exitosamente:")
        print(f"   📅 Fecha: {fecha_mantenimiento}")
        print(f"   🚗 Vehículo: {vehiculo_seleccionado['marca']} {vehiculo_seleccionado['modelo']}")
        print(f"   📊 Kilometraje: {vehiculo_seleccionado['kilometraje']:,} km → {kilometraje_actual:,} km")
        print(f"   🔧 Tipo: {tipo_mantenimiento}")
        print(f"   📝 Descripción: {descripcion}")
        print(f"   💰 Costo: {costo if costo else 'No especificado'}")
        
    except Exception as e:
        print(f"❌ Error al crear historial de mantenimiento: {e}")
    
def main():
    """Función principal que maneja el menú del sistema"""
    load_data()
    print("¡Bienvenido al Sistema de Gestión de Automotores! 🚗")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\nSeleccione una opción (1-5): ").strip()
            
            if opcion == "1":
                registrar_propietario()
            elif opcion == "2":
                agregar_vehiculo()
            elif opcion == "3":
                listar_propietarios()
            elif opcion == "4":
                crear_historial_mantenimiento()
            elif opcion == "5":
                print("\n👋 ¡Gracias por usar el Sistema de Gestión de Automotores!")
                print("¡Hasta luego! 🚗")
                break
            else:
                print("❌ Opción inválida. Por favor seleccione una opción del 1 al 5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido por el usuario.")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
