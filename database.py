# ===========================================
# BASE DE DATOS SQLITE3 - SISTEMA AUTOMOTORES
# ===========================================

import sqlite3
import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_name: str = "automotores.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Obtiene una conexión a la base de datos"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Inicializa la base de datos y crea las tablas necesarias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Crear tabla de propietarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS propietarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                rut TEXT UNIQUE NOT NULL,
                tipo_personal TEXT,
                telefono TEXT,
                email TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Agregar columna tipo_personal si no existe (para bases de datos existentes)
        try:
            cursor.execute('ALTER TABLE propietarios ADD COLUMN tipo_personal TEXT')
        except sqlite3.OperationalError:
            # La columna ya existe, no hacer nada
            pass
        
        # Crear tabla de vehículos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                propietario_id INTEGER NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                año INTEGER,
                color TEXT,
                kilometraje INTEGER DEFAULT 0,
                patente TEXT UNIQUE,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (propietario_id) REFERENCES propietarios (id)
            )
        ''')
        
        # Crear tabla de mantenimientos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mantenimientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehiculo_id INTEGER NOT NULL,
                fecha_mantenimiento DATE NOT NULL,
                tipo_mantenimiento TEXT NOT NULL,
                kilometraje_anterior INTEGER,
                kilometraje_actual INTEGER,
                kilometros_recorridos INTEGER,
                descripcion TEXT,
                costo REAL,
                taller TEXT,
                foto_url TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos (id)
            )
        ''')

        # Agregar columna kilometros_recorridos si no existe (para bases existentes)
        try:
            cursor.execute('ALTER TABLE mantenimientos ADD COLUMN kilometros_recorridos INTEGER')
        except sqlite3.OperationalError:
            pass
        
        # Crear tabla de viajes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS viajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vehiculo_id INTEGER NOT NULL,
                propietario_id INTEGER NOT NULL,
                tipo_personal TEXT,
                destino TEXT NOT NULL,
                fecha_salida DATE NOT NULL,
                fecha_llegada DATE,
                kilometraje_salida INTEGER NOT NULL,
                kilometraje_llegada INTEGER,
                combustible_inicial REAL,
                combustible_final REAL,
                combustible_consumido REAL,
                costo_combustible REAL,
                observaciones TEXT,
                estado TEXT DEFAULT 'En curso',
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (vehiculo_id) REFERENCES vehiculos (id),
                FOREIGN KEY (propietario_id) REFERENCES propietarios (id)
            )
        ''')

        # Crear tabla de tickets de rendición
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                sistema TEXT NOT NULL CHECK (sistema IN ('viajes','mantenimientos')),
                referencia_id INTEGER,
                descripcion TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Agregar columna tipo_personal si no existe (para bases de datos existentes)
        try:
            cursor.execute('ALTER TABLE viajes ADD COLUMN tipo_personal TEXT')
        except sqlite3.OperationalError:
            # La columna ya existe, no hacer nada
            pass
        
        # Crear tabla de presupuesto
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS presupuesto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo_movimiento TEXT NOT NULL CHECK (tipo_movimiento IN ('ingreso', 'egreso')),
                categoria TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                monto REAL NOT NULL,
                fecha_movimiento DATE NOT NULL,
                metodo_pago TEXT,
                referencia TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla de información adicional de propietarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS propietarios_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                propietario_id INTEGER NOT NULL,
                direccion TEXT,
                fecha_nacimiento DATE,
                profesion TEXT,
                empresa TEXT,
                telefono_emergencia TEXT,
                contacto_emergencia TEXT,
                notas TEXT,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (propietario_id) REFERENCES propietarios (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insertar datos de ejemplo si las tablas están vacías
        self.insert_sample_data()
    
    def insert_sample_data(self):
        """Inserta datos de ejemplo si las tablas están vacías"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM propietarios")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Datos de ejemplo
        propietarios_ejemplo = [
            ("Carlos", "Pérez", "12345678-9", "987654321", "carlos.perez@email.com"),
            ("María", "González", "23456789-0", "876543210", "maria.gonzalez@email.com"),
            ("Luis", "Martínez", "34567890-1", "765432109", "luis.martinez@email.com"),
            ("Ana", "Rodríguez", "45678901-2", "654321098", "ana.rodriguez@email.com"),
            ("Pedro", "López", "56789012-3", "543210987", "pedro.lopez@email.com")
        ]
        
        cursor.executemany('''
            INSERT INTO propietarios (nombre, apellido, rut, telefono, email)
            VALUES (?, ?, ?, ?, ?)
        ''', propietarios_ejemplo)
        
        # Obtener IDs de propietarios para los vehículos
        cursor.execute("SELECT id FROM propietarios")
        propietario_ids = [row[0] for row in cursor.fetchall()]
        
        vehiculos_ejemplo = [
            (propietario_ids[0], "Toyota", "Corolla", 2020, "Blanco", 25000, "ABC123"),
            (propietario_ids[0], "Honda", "Civic", 2019, "Negro", 35000, "DEF456"),
            (propietario_ids[1], "Ford", "Focus", 2021, "Rojo", 15000, "GHI789"),
            (propietario_ids[2], "Chevrolet", "Cruze", 2018, "Azul", 45000, "JKL012"),
            (propietario_ids[3], "Nissan", "Sentra", 2022, "Gris", 8000, "MNO345")
        ]
        
        cursor.executemany('''
            INSERT INTO vehiculos (propietario_id, marca, modelo, año, color, kilometraje, patente)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', vehiculos_ejemplo)
        
        # Obtener IDs de vehículos para los mantenimientos
        cursor.execute("SELECT id FROM vehiculos")
        vehiculo_ids = [row[0] for row in cursor.fetchall()]
        
        mantenimientos_ejemplo = [
            (vehiculo_ids[0], "2024-01-15", "Cambio de aceite", 24000, 25000, "Cambio de aceite y filtro", 45000, "Taller Central"),
            (vehiculo_ids[1], "2024-02-20", "Revisión general", 33000, 35000, "Revisión completa del vehículo", 80000, "AutoService"),
            (vehiculo_ids[2], "2024-03-10", "Cambio de neumáticos", 14000, 15000, "Cambio de 4 neumáticos", 120000, "Neumáticos Plus"),
            (vehiculo_ids[3], "2024-01-25", "Mantenimiento preventivo", 43000, 45000, "Mantenimiento programado", 65000, "Taller Central"),
            (vehiculo_ids[4], "2024-04-05", "Primera revisión", 7000, 8000, "Primera revisión de garantía", 0, "Concesionario Nissan")
        ]
        
        cursor.executemany('''
            INSERT INTO mantenimientos (vehiculo_id, fecha_mantenimiento, tipo_mantenimiento, 
                                      kilometraje_anterior, kilometraje_actual, descripcion, costo, taller)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', mantenimientos_ejemplo)
        
        conn.commit()
        conn.close()
    
    # CRUD para Propietarios
    def create_propietario(self, nombre: str, apellido: str, rut: str, tipo_personal: str = None, telefono: str = None, email: str = None) -> int:
        """Crea un nuevo propietario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO propietarios (nombre, apellido, rut, tipo_personal, telefono, email)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, apellido, rut, tipo_personal, telefono, email))
            
            propietario_id = cursor.lastrowid
            conn.commit()
            return propietario_id
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe un propietario con ese RUT")
        finally:
            conn.close()
    
    def get_propietarios(self) -> List[Dict]:
        """Obtiene todos los propietarios"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT p.*, COUNT(v.id) as total_vehiculos
            FROM propietarios p
            LEFT JOIN vehiculos v ON p.id = v.propietario_id
            GROUP BY p.id
            ORDER BY p.nombre, p.apellido
        ''')
        
        columns = [description[0] for description in cursor.description]
        propietarios = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return propietarios
    
    def get_propietario_by_id(self, propietario_id: int) -> Optional[Dict]:
        """Obtiene un propietario por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM propietarios WHERE id = ?", (propietario_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            propietario = dict(zip(columns, row))
            conn.close()
            return propietario
        
        conn.close()
        return None
    
    def update_propietario(self, propietario_id: int, nombre: str, apellido: str, rut: str, tipo_personal: str = None, telefono: str = None, email: str = None) -> bool:
        """Actualiza un propietario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE propietarios 
                SET nombre = ?, apellido = ?, rut = ?, tipo_personal = ?, telefono = ?, email = ?
                WHERE id = ?
            ''', (nombre, apellido, rut, tipo_personal, telefono, email, propietario_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe un propietario con ese RUT")
        finally:
            conn.close()
    
    def delete_propietario(self, propietario_id: int) -> bool:
        """Elimina un propietario y todos sus vehículos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Eliminar mantenimientos de los vehículos del propietario
            cursor.execute('''
                DELETE FROM mantenimientos 
                WHERE vehiculo_id IN (
                    SELECT id FROM vehiculos WHERE propietario_id = ?
                )
            ''', (propietario_id,))
            
            # Eliminar vehículos del propietario
            cursor.execute("DELETE FROM vehiculos WHERE propietario_id = ?", (propietario_id,))
            
            # Eliminar el propietario
            cursor.execute("DELETE FROM propietarios WHERE id = ?", (propietario_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    # CRUD para Vehículos
    def create_vehiculo(self, propietario_id: int, marca: str, modelo: str, año: int = None, 
                       color: str = None, kilometraje: int = 0, patente: str = None) -> int:
        """Crea un nuevo vehículo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO vehiculos (propietario_id, marca, modelo, año, color, kilometraje, patente)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (propietario_id, marca, modelo, año, color, kilometraje, patente))
            
            vehiculo_id = cursor.lastrowid
            conn.commit()
            return vehiculo_id
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe un vehículo con esa patente")
        finally:
            conn.close()
    
    def get_vehiculos_by_propietario(self, propietario_id: int) -> List[Dict]:
        """Obtiene todos los vehículos de un propietario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.*, p.nombre || ' ' || p.apellido as propietario_nombre,
                   COUNT(m.id) as total_mantenimientos
            FROM vehiculos v
            JOIN propietarios p ON v.propietario_id = p.id
            LEFT JOIN mantenimientos m ON v.id = m.vehiculo_id
            WHERE v.propietario_id = ?
            GROUP BY v.id
            ORDER BY v.marca, v.modelo
        ''', (propietario_id,))
        
        columns = [description[0] for description in cursor.description]
        vehiculos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return vehiculos
    
    def get_all_vehiculos(self) -> List[Dict]:
        """Obtiene todos los vehículos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.*, p.nombre || ' ' || p.apellido as propietario_nombre,
                   COUNT(m.id) as total_mantenimientos
            FROM vehiculos v
            JOIN propietarios p ON v.propietario_id = p.id
            LEFT JOIN mantenimientos m ON v.id = m.vehiculo_id
            GROUP BY v.id
            ORDER BY p.nombre, v.marca, v.modelo
        ''')
        
        columns = [description[0] for description in cursor.description]
        vehiculos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return vehiculos
    
    def update_vehiculo(self, vehiculo_id: int, marca: str, modelo: str, año: int = None,
                       color: str = None, kilometraje: int = 0, patente: str = None) -> bool:
        """Actualiza un vehículo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE vehiculos 
                SET marca = ?, modelo = ?, año = ?, color = ?, kilometraje = ?, patente = ?
                WHERE id = ?
            ''', (marca, modelo, año, color, kilometraje, patente, vehiculo_id))
            
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe un vehículo con esa patente")
        finally:
            conn.close()
    
    def delete_vehiculo(self, vehiculo_id: int) -> bool:
        """Elimina un vehículo y todos sus mantenimientos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Eliminar mantenimientos del vehículo
            cursor.execute("DELETE FROM mantenimientos WHERE vehiculo_id = ?", (vehiculo_id,))
            
            # Eliminar el vehículo
            cursor.execute("DELETE FROM vehiculos WHERE id = ?", (vehiculo_id,))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    # CRUD para Mantenimientos
    def create_mantenimiento(self, vehiculo_id: int, fecha_mantenimiento: str, tipo_mantenimiento: str,
                           kilometros_recorridos: int, descripcion: str = None,
                           costo: float = None, taller: str = None) -> int:
        """Crea un nuevo mantenimiento"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO mantenimientos (vehiculo_id, fecha_mantenimiento, tipo_mantenimiento,
                                          kilometros_recorridos, descripcion, costo, taller)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (vehiculo_id, fecha_mantenimiento, tipo_mantenimiento,
                  kilometros_recorridos, descripcion, costo, taller))
            
            mantenimiento_id = cursor.lastrowid
            
            # Ya no se actualiza el kilometraje del vehículo desde mantenimiento personalizado
            
            conn.commit()
            return mantenimiento_id
        finally:
            conn.close()
    
    def get_mantenimiento_by_id(self, mantenimiento_id: int) -> Optional[Dict]:
        """Obtiene un mantenimiento por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, v.marca || ' ' || v.modelo as vehiculo_info,
                   p.nombre || ' ' || p.apellido as propietario_nombre
            FROM mantenimientos m
            JOIN vehiculos v ON m.vehiculo_id = v.id
            JOIN propietarios p ON v.propietario_id = p.id
            WHERE m.id = ?
        ''', (mantenimiento_id,))
        
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            mantenimiento = dict(zip(columns, row))
            conn.close()
            return mantenimiento
        
        conn.close()
        return None
    
    def get_mantenimientos_by_vehiculo(self, vehiculo_id: int) -> List[Dict]:
        """Obtiene todos los mantenimientos de un vehículo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, v.marca || ' ' || v.modelo as vehiculo_info
            FROM mantenimientos m
            JOIN vehiculos v ON m.vehiculo_id = v.id
            WHERE m.vehiculo_id = ?
            ORDER BY m.fecha_mantenimiento DESC
        ''', (vehiculo_id,))
        
        columns = [description[0] for description in cursor.description]
        mantenimientos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return mantenimientos
    # CRUD para Tickets de Rendición
    def create_ticket(self, fecha: str, sistema: str, referencia_id: int = None, descripcion: str = None) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO tickets (fecha, sistema, referencia_id, descripcion)
                VALUES (?, ?, ?, ?)
            ''', (fecha, sistema, referencia_id, descripcion))
            ticket_id = cursor.lastrowid
            conn.commit()
            return ticket_id
        finally:
            conn.close()

    def get_all_tickets(self) -> List[Dict]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM tickets ORDER BY fecha DESC, id DESC
        ''')
        columns = [d[0] for d in cursor.description]
        rows = cursor.fetchall()
        conn.close()
        return [dict(zip(columns, r)) for r in rows]
    
    def get_all_mantenimientos(self) -> List[Dict]:
        """Obtiene todos los mantenimientos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT m.*, v.marca || ' ' || v.modelo as vehiculo_info,
                   p.nombre || ' ' || p.apellido as propietario_nombre
            FROM mantenimientos m
            JOIN vehiculos v ON m.vehiculo_id = v.id
            JOIN propietarios p ON v.propietario_id = p.id
            ORDER BY m.fecha_mantenimiento DESC
        ''')
        
        columns = [description[0] for description in cursor.description]
        mantenimientos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return mantenimientos
    
    def update_mantenimiento(self, mantenimiento_id: int, vehiculo_id: int, fecha_mantenimiento: str,
                           tipo_mantenimiento: str, kilometros_recorridos: int,
                           descripcion: str = None, costo: float = None, taller: str = None) -> bool:
        """Actualiza un mantenimiento"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE mantenimientos 
                SET vehiculo_id = ?, fecha_mantenimiento = ?, tipo_mantenimiento = ?,
                    kilometros_recorridos = ?, descripcion = ?,
                    costo = ?, taller = ?
                WHERE id = ?
            ''', (vehiculo_id, fecha_mantenimiento, tipo_mantenimiento, kilometros_recorridos,
                  descripcion, costo, taller, mantenimiento_id))
            
            # Ya no se actualiza el kilometraje del vehículo desde mantenimiento personalizado
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    def delete_mantenimiento(self, mantenimiento_id: int) -> bool:
        """Elimina un mantenimiento"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM mantenimientos WHERE id = ?", (mantenimiento_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    # CRUD para Viajes
    def create_viaje(self, vehiculo_id: int, propietario_id: int, destino: str, 
                    fecha_salida: str, kilometraje_salida: int, tipo_personal: str = None,
                    combustible_inicial: float = None, observaciones: str = None) -> int:
        """Crea un nuevo viaje"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO viajes (vehiculo_id, propietario_id, tipo_personal, destino, fecha_salida, 
                                  kilometraje_salida, combustible_inicial, observaciones)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (vehiculo_id, propietario_id, tipo_personal, destino, fecha_salida, 
                  kilometraje_salida, combustible_inicial, observaciones))
            
            viaje_id = cursor.lastrowid
            conn.commit()
            return viaje_id
        finally:
            conn.close()
    
    def get_viajes_by_vehiculo(self, vehiculo_id: int) -> List[Dict]:
        """Obtiene todos los viajes de un vehículo"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.*, ve.marca || ' ' || ve.modelo as vehiculo_info,
                   p.nombre || ' ' || p.apellido as propietario_nombre
            FROM viajes v
            JOIN vehiculos ve ON v.vehiculo_id = ve.id
            JOIN propietarios p ON v.propietario_id = p.id
            WHERE v.vehiculo_id = ?
            ORDER BY v.fecha_salida DESC
        ''', (vehiculo_id,))
        
        columns = [description[0] for description in cursor.description]
        viajes = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return viajes
    
    def get_all_viajes(self) -> List[Dict]:
        """Obtiene todos los viajes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT v.*, ve.marca || ' ' || ve.modelo as vehiculo_info,
                   p.nombre || ' ' || p.apellido as propietario_nombre
            FROM viajes v
            JOIN vehiculos ve ON v.vehiculo_id = ve.id
            JOIN propietarios p ON v.propietario_id = p.id
            ORDER BY v.fecha_salida DESC
        ''')
        
        columns = [description[0] for description in cursor.description]
        viajes = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return viajes
    
    def update_viaje(self, viaje_id: int, fecha_llegada: str = None, 
                    kilometraje_llegada: int = None, combustible_final: float = None,
                    combustible_consumido: float = None, costo_combustible: float = None,
                    observaciones: str = None, estado: str = None, tipo_personal: str = None) -> bool:
        """Actualiza un viaje"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Construir la consulta dinámicamente
            updates = []
            params = []
            
            if fecha_llegada:
                updates.append("fecha_llegada = ?")
                params.append(fecha_llegada)
            if kilometraje_llegada:
                updates.append("kilometraje_llegada = ?")
                params.append(kilometraje_llegada)
            if combustible_final is not None:
                updates.append("combustible_final = ?")
                params.append(combustible_final)
            if combustible_consumido is not None:
                updates.append("combustible_consumido = ?")
                params.append(combustible_consumido)
            if costo_combustible is not None:
                updates.append("costo_combustible = ?")
                params.append(costo_combustible)
            if observaciones:
                updates.append("observaciones = ?")
                params.append(observaciones)
            if estado:
                updates.append("estado = ?")
                params.append(estado)
            if tipo_personal:
                updates.append("tipo_personal = ?")
                params.append(tipo_personal)
            
            if updates:
                params.append(viaje_id)
                query = f"UPDATE viajes SET {', '.join(updates)} WHERE id = ?"
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount > 0
            
            return False
        finally:
            conn.close()
    
    def delete_viaje(self, viaje_id: int) -> bool:
        """Elimina un viaje"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM viajes WHERE id = ?", (viaje_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    # CRUD para Presupuesto
    def create_movimiento_presupuesto(self, tipo_movimiento: str, categoria: str, 
                                    descripcion: str, monto: float, fecha_movimiento: str,
                                    metodo_pago: str = None, referencia: str = None) -> int:
        """Crea un nuevo movimiento de presupuesto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO presupuesto (tipo_movimiento, categoria, descripcion, monto, 
                                       fecha_movimiento, metodo_pago, referencia)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (tipo_movimiento, categoria, descripcion, monto, 
                  fecha_movimiento, metodo_pago, referencia))
            
            movimiento_id = cursor.lastrowid
            conn.commit()
            return movimiento_id
        finally:
            conn.close()
    
    def get_movimientos_presupuesto(self, tipo_movimiento: str = None) -> List[Dict]:
        """Obtiene movimientos de presupuesto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if tipo_movimiento:
            cursor.execute('''
                SELECT * FROM presupuesto 
                WHERE tipo_movimiento = ?
                ORDER BY fecha_movimiento DESC
            ''', (tipo_movimiento,))
        else:
            cursor.execute('''
                SELECT * FROM presupuesto 
                ORDER BY fecha_movimiento DESC
            ''')
        
        columns = [description[0] for description in cursor.description]
        movimientos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return movimientos
    
    def get_estadisticas_presupuesto(self) -> Dict:
        """Obtiene estadísticas del presupuesto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total ingresos
        cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM presupuesto WHERE tipo_movimiento = 'ingreso'")
        total_ingresos = cursor.fetchone()[0]
        
        # Total egresos
        cursor.execute("SELECT COALESCE(SUM(monto), 0) FROM presupuesto WHERE tipo_movimiento = 'egreso'")
        total_egresos = cursor.fetchone()[0]
        
        # Balance
        balance = total_ingresos - total_egresos
        
        # Ingresos por categoría
        cursor.execute('''
            SELECT categoria, SUM(monto) as total
            FROM presupuesto 
            WHERE tipo_movimiento = 'ingreso'
            GROUP BY categoria
            ORDER BY total DESC
        ''')
        ingresos_por_categoria = [dict(zip(['categoria', 'total'], row)) for row in cursor.fetchall()]
        
        # Egresos por categoría
        cursor.execute('''
            SELECT categoria, SUM(monto) as total
            FROM presupuesto 
            WHERE tipo_movimiento = 'egreso'
            GROUP BY categoria
            ORDER BY total DESC
        ''')
        egresos_por_categoria = [dict(zip(['categoria', 'total'], row)) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            'total_ingresos': total_ingresos,
            'total_egresos': total_egresos,
            'balance': balance,
            'ingresos_por_categoria': ingresos_por_categoria,
            'egresos_por_categoria': egresos_por_categoria
        }
    
    def delete_movimiento_presupuesto(self, movimiento_id: int) -> bool:
        """Elimina un movimiento de presupuesto"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM presupuesto WHERE id = ?", (movimiento_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
    
    # CRUD para Información Adicional de Propietarios
    def create_propietario_info(self, propietario_id: int, direccion: str = None,
                              fecha_nacimiento: str = None, profesion: str = None,
                              empresa: str = None, telefono_emergencia: str = None,
                              contacto_emergencia: str = None, notas: str = None) -> int:
        """Crea información adicional de un propietario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO propietarios_info (propietario_id, direccion, fecha_nacimiento,
                                             profesion, empresa, telefono_emergencia,
                                             contacto_emergencia, notas)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (propietario_id, direccion, fecha_nacimiento, profesion, empresa,
                  telefono_emergencia, contacto_emergencia, notas))
            
            info_id = cursor.lastrowid
            conn.commit()
            return info_id
        finally:
            conn.close()
    
    def get_propietario_info(self, propietario_id: int) -> Optional[Dict]:
        """Obtiene información adicional de un propietario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM propietarios_info WHERE propietario_id = ?", (propietario_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            info = dict(zip(columns, row))
            conn.close()
            return info
        
        conn.close()
        return None
    
    def update_propietario_info(self, propietario_id: int, direccion: str = None,
                              fecha_nacimiento: str = None, profesion: str = None,
                              empresa: str = None, telefono_emergencia: str = None,
                              contacto_emergencia: str = None, notas: str = None) -> bool:
        """Actualiza información adicional de un propietario"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Verificar si existe información
            cursor.execute("SELECT id FROM propietarios_info WHERE propietario_id = ?", (propietario_id,))
            if not cursor.fetchone():
                # Crear nueva información
                self.create_propietario_info(propietario_id, direccion, fecha_nacimiento,
                                           profesion, empresa, telefono_emergencia,
                                           contacto_emergencia, notas)
                return True
            
            # Actualizar información existente
            cursor.execute('''
                UPDATE propietarios_info 
                SET direccion = ?, fecha_nacimiento = ?, profesion = ?, empresa = ?,
                    telefono_emergencia = ?, contacto_emergencia = ?, notas = ?
                WHERE propietario_id = ?
            ''', (direccion, fecha_nacimiento, profesion, empresa,
                  telefono_emergencia, contacto_emergencia, notas, propietario_id))
            
            conn.commit()
            return cursor.rowcount > 0
        finally:
            conn.close()
