# ===========================================
# API REST - SISTEMA AUTOMOTORES
# ===========================================

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import DatabaseManager
import datetime

app = Flask(__name__)
CORS(app)

# Inicializar la base de datos
db = DatabaseManager()

# ===========================================
# RUTAS PARA PROPIETARIOS
# ===========================================

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/vehiculos-viajes')
def vehiculos_viajes_page():
    """Página de sistema de viajes para vehículos"""
    return render_template('vehiculos_viajes.html')


@app.route('/presupuesto')
def presupuesto_page():
    """Página de gestión de presupuesto"""
    return render_template('presupuesto.html')

# ===========================================
# RUTAS - RENDICIÓN DE TICKETS
# ===========================================

@app.route('/tickets')
def tickets_page():
    """Página de gestión de tickets"""
    return render_template('tickets.html')

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    try:
        tickets = db.get_all_tickets()
        return jsonify({'success': True, 'data': tickets})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    try:
        data = request.get_json()
        required = ['fecha', 'sistema']  # sistema: 'viajes' | 'mantenimientos'
        for f in required:
            if not data.get(f):
                return jsonify({'success': False, 'error': f'El campo {f} es obligatorio'}), 400

        ticket_id = db.create_ticket(
            fecha=data['fecha'],
            sistema=data['sistema'],
            referencia_id=data.get('referencia_id'),
            descripcion=data.get('descripcion')
        )
        return jsonify({'success': True, 'message': 'Ticket creado', 'data': {'id': ticket_id}}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/propietarios', methods=['GET'])
def get_propietarios():
    """Obtiene todos los propietarios"""
    try:
        propietarios = db.get_propietarios()
        return jsonify({
            'success': True,
            'data': propietarios,
            'count': len(propietarios)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/propietarios/<int:propietario_id>', methods=['GET'])
def get_propietario(propietario_id):
    """Obtiene un propietario por ID"""
    try:
        propietario = db.get_propietario_by_id(propietario_id)
        if propietario:
            return jsonify({
                'success': True,
                'data': propietario
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Propietario no encontrado'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/propietarios', methods=['POST'])
def create_propietario():
    """Crea un nuevo propietario"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombre', 'apellido', 'rut']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        propietario_id = db.create_propietario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            rut=data['rut'],
            tipo_personal=data.get('tipo_personal'),
            telefono=data.get('telefono'),
            email=data.get('email')
        )
        
        return jsonify({
            'success': True,
            'message': 'Propietario creado exitosamente',
            'data': {'id': propietario_id}
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/propietarios/<int:propietario_id>', methods=['PUT'])
def update_propietario(propietario_id):
    """Actualiza un propietario"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['nombre', 'apellido', 'rut']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        success = db.update_propietario(
            propietario_id=propietario_id,
            nombre=data['nombre'],
            apellido=data['apellido'],
            rut=data['rut'],
            tipo_personal=data.get('tipo_personal'),
            telefono=data.get('telefono'),
            email=data.get('email')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Propietario actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Propietario no encontrado'
            }), 404
            
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/propietarios/<int:propietario_id>', methods=['DELETE'])
def delete_propietario(propietario_id):
    """Elimina un propietario"""
    try:
        success = db.delete_propietario(propietario_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Propietario eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Propietario no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===========================================
# RUTAS PARA VEHÍCULOS
# ===========================================

@app.route('/api/vehiculos', methods=['GET'])
def get_vehiculos():
    """Obtiene todos los vehículos"""
    try:
        vehiculos = db.get_all_vehiculos()
        return jsonify({
            'success': True,
            'data': vehiculos,
            'count': len(vehiculos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/propietarios/<int:propietario_id>/vehiculos', methods=['GET'])
def get_vehiculos_by_propietario(propietario_id):
    """Obtiene vehículos de un propietario"""
    try:
        vehiculos = db.get_vehiculos_by_propietario(propietario_id)
        return jsonify({
            'success': True,
            'data': vehiculos,
            'count': len(vehiculos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/vehiculos', methods=['POST'])
def create_vehiculo():
    """Crea un nuevo vehículo"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['propietario_id', 'marca', 'modelo']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        vehiculo_id = db.create_vehiculo(
            propietario_id=data['propietario_id'],
            marca=data['marca'],
            modelo=data['modelo'],
            año=data.get('año'),
            color=data.get('color'),
            kilometraje=data.get('kilometraje', 0),
            patente=data.get('patente')
        )
        
        return jsonify({
            'success': True,
            'message': 'Vehículo creado exitosamente',
            'data': {'id': vehiculo_id}
        }), 201
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/vehiculos/<int:vehiculo_id>', methods=['PUT'])
def update_vehiculo(vehiculo_id):
    """Actualiza un vehículo"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['marca', 'modelo']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        success = db.update_vehiculo(
            vehiculo_id=vehiculo_id,
            marca=data['marca'],
            modelo=data['modelo'],
            año=data.get('año'),
            color=data.get('color'),
            kilometraje=data.get('kilometraje', 0),
            patente=data.get('patente')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Vehículo actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Vehículo no encontrado'
            }), 404
            
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/vehiculos/<int:vehiculo_id>', methods=['DELETE'])
def delete_vehiculo(vehiculo_id):
    """Elimina un vehículo"""
    try:
        success = db.delete_vehiculo(vehiculo_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Vehículo eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Vehículo no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===========================================
# RUTAS PARA MANTENIMIENTOS
# ===========================================

@app.route('/api/mantenimientos', methods=['GET'])
def get_mantenimientos():
    """Obtiene todos los mantenimientos"""
    try:
        mantenimientos = db.get_all_mantenimientos()
        return jsonify({
            'success': True,
            'data': mantenimientos,
            'count': len(mantenimientos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/vehiculos/<int:vehiculo_id>/mantenimientos', methods=['GET'])
def get_mantenimientos_by_vehiculo(vehiculo_id):
    """Obtiene mantenimientos de un vehículo"""
    try:
        mantenimientos = db.get_mantenimientos_by_vehiculo(vehiculo_id)
        return jsonify({
            'success': True,
            'data': mantenimientos,
            'count': len(mantenimientos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mantenimientos', methods=['POST'])
def create_mantenimiento():
    """Crea un nuevo mantenimiento"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['vehiculo_id', 'fecha_mantenimiento', 'tipo_mantenimiento', 'kilometros_recorridos']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        mantenimiento_id = db.create_mantenimiento(
            vehiculo_id=data['vehiculo_id'],
            fecha_mantenimiento=data['fecha_mantenimiento'],
            tipo_mantenimiento=data['tipo_mantenimiento'],
            kilometros_recorridos=data['kilometros_recorridos'],
            descripcion=data.get('descripcion'),
            costo=data.get('costo'),
            taller=data.get('taller')
        )
        
        return jsonify({
            'success': True,
            'message': 'Mantenimiento creado exitosamente',
            'data': {'id': mantenimiento_id}
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mantenimientos/<int:mantenimiento_id>', methods=['PUT'])
def update_mantenimiento(mantenimiento_id):
    """Actualiza un mantenimiento"""
    try:
        data = request.get_json()
        
        # Validar que el mantenimiento existe
        mantenimiento = db.get_mantenimiento_by_id(mantenimiento_id)
        if not mantenimiento:
            return jsonify({
                'success': False,
                'error': 'Mantenimiento no encontrado'
            }), 404
        
        # Validar datos requeridos
        required_fields = ['vehiculo_id', 'fecha_mantenimiento', 'tipo_mantenimiento', 'kilometros_recorridos']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        success = db.update_mantenimiento(
            mantenimiento_id=mantenimiento_id,
            vehiculo_id=data['vehiculo_id'],
            fecha_mantenimiento=data['fecha_mantenimiento'],
            tipo_mantenimiento=data['tipo_mantenimiento'],
            kilometros_recorridos=data['kilometros_recorridos'],
            descripcion=data.get('descripcion'),
            costo=data.get('costo'),
            taller=data.get('taller')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Mantenimiento actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Error al actualizar el mantenimiento'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mantenimientos/<int:mantenimiento_id>', methods=['DELETE'])
def delete_mantenimiento(mantenimiento_id):
    """Elimina un mantenimiento"""
    try:
        success = db.delete_mantenimiento(mantenimiento_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Mantenimiento eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Mantenimiento no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===========================================
# RUTAS DE ESTADÍSTICAS
# ===========================================

@app.route('/api/estadisticas', methods=['GET'])
def get_estadisticas():
    """Obtiene estadísticas generales del sistema"""
    try:
        propietarios = db.get_propietarios()
        vehiculos = db.get_all_vehiculos()
        mantenimientos = db.get_all_mantenimientos()
        
        # Calcular estadísticas
        total_propietarios = len(propietarios)
        total_vehiculos = len(vehiculos)
        total_mantenimientos = len(mantenimientos)
        
        # Marca más común
        marcas = {}
        for vehiculo in vehiculos:
            marca = vehiculo['marca']
            marcas[marca] = marcas.get(marca, 0) + 1
        
        marca_mas_comun = max(marcas.items(), key=lambda x: x[1]) if marcas else ('N/A', 0)
        
        # Costo total de mantenimientos
        costo_total = sum(m['costo'] or 0 for m in mantenimientos)
        
        return jsonify({
            'success': True,
            'data': {
                'total_propietarios': total_propietarios,
                'total_vehiculos': total_vehiculos,
                'total_mantenimientos': total_mantenimientos,
                'marca_mas_comun': marca_mas_comun[0],
                'vehiculos_por_marca': marca_mas_comun[1],
                'costo_total_mantenimientos': costo_total
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===========================================
# RUTAS PARA VIAJES
# ===========================================

@app.route('/api/viajes', methods=['GET'])
def get_viajes():
    """Obtiene todos los viajes"""
    try:
        viajes = db.get_all_viajes()
        return jsonify({
            'success': True,
            'data': viajes,
            'count': len(viajes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/vehiculos/<int:vehiculo_id>/viajes', methods=['GET'])
def get_viajes_by_vehiculo(vehiculo_id):
    """Obtiene viajes de un vehículo"""
    try:
        viajes = db.get_viajes_by_vehiculo(vehiculo_id)
        return jsonify({
            'success': True,
            'data': viajes,
            'count': len(viajes)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/viajes', methods=['POST'])
def create_viaje():
    """Crea un nuevo viaje"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['vehiculo_id', 'propietario_id', 'destino', 'fecha_salida', 'kilometraje_salida']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        viaje_id = db.create_viaje(
            vehiculo_id=data['vehiculo_id'],
            propietario_id=data['propietario_id'],
            destino=data['destino'],
            fecha_salida=data['fecha_salida'],
            kilometraje_salida=data['kilometraje_salida'],
            tipo_personal=data.get('tipo_personal'),
            combustible_inicial=data.get('combustible_inicial'),
            observaciones=data.get('observaciones')
        )
        
        return jsonify({
            'success': True,
            'message': 'Viaje creado exitosamente',
            'data': {'id': viaje_id}
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/viajes/<int:viaje_id>', methods=['PUT'])
def update_viaje(viaje_id):
    """Actualiza un viaje"""
    try:
        data = request.get_json()
        
        success = db.update_viaje(
            viaje_id=viaje_id,
            fecha_llegada=data.get('fecha_llegada'),
            kilometraje_llegada=data.get('kilometraje_llegada'),
            combustible_final=data.get('combustible_final'),
            combustible_consumido=data.get('combustible_consumido'),
            costo_combustible=data.get('costo_combustible'),
            observaciones=data.get('observaciones'),
            estado=data.get('estado'),
            tipo_personal=data.get('tipo_personal')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Viaje actualizado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Viaje no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/viajes/<int:viaje_id>', methods=['DELETE'])
def delete_viaje(viaje_id):
    """Elimina un viaje"""
    try:
        success = db.delete_viaje(viaje_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Viaje eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Viaje no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===========================================
# RUTAS PARA PRESUPUESTO
# ===========================================

@app.route('/api/presupuesto', methods=['GET'])
def get_movimientos_presupuesto():
    """Obtiene movimientos de presupuesto"""
    try:
        tipo_movimiento = request.args.get('tipo')
        movimientos = db.get_movimientos_presupuesto(tipo_movimiento)
        return jsonify({
            'success': True,
            'data': movimientos,
            'count': len(movimientos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/presupuesto/estadisticas', methods=['GET'])
def get_estadisticas_presupuesto():
    """Obtiene estadísticas del presupuesto"""
    try:
        estadisticas = db.get_estadisticas_presupuesto()
        return jsonify({
            'success': True,
            'data': estadisticas
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/presupuesto', methods=['POST'])
def create_movimiento_presupuesto():
    """Crea un nuevo movimiento de presupuesto"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['tipo_movimiento', 'categoria', 'descripcion', 'monto', 'fecha_movimiento']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'El campo {field} es obligatorio'
                }), 400
        
        movimiento_id = db.create_movimiento_presupuesto(
            tipo_movimiento=data['tipo_movimiento'],
            categoria=data['categoria'],
            descripcion=data['descripcion'],
            monto=data['monto'],
            fecha_movimiento=data['fecha_movimiento'],
            metodo_pago=data.get('metodo_pago'),
            referencia=data.get('referencia')
        )
        
        return jsonify({
            'success': True,
            'message': 'Movimiento creado exitosamente',
            'data': {'id': movimiento_id}
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/presupuesto/<int:movimiento_id>', methods=['DELETE'])
def delete_movimiento_presupuesto(movimiento_id):
    """Elimina un movimiento de presupuesto"""
    try:
        success = db.delete_movimiento_presupuesto(movimiento_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Movimiento eliminado exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Movimiento no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ===========================================
# RUTAS PARA INFORMACIÓN ADICIONAL DE PROPIETARIOS
# ===========================================

@app.route('/api/propietarios/<int:propietario_id>/info', methods=['GET'])
def get_propietario_info(propietario_id):
    """Obtiene información adicional de un propietario"""
    try:
        info = db.get_propietario_info(propietario_id)
        return jsonify({
            'success': True,
            'data': info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/propietarios/<int:propietario_id>/info', methods=['POST'])
def create_propietario_info(propietario_id):
    """Crea información adicional de un propietario"""
    try:
        data = request.get_json()
        
        info_id = db.create_propietario_info(
            propietario_id=propietario_id,
            direccion=data.get('direccion'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            profesion=data.get('profesion'),
            empresa=data.get('empresa'),
            telefono_emergencia=data.get('telefono_emergencia'),
            contacto_emergencia=data.get('contacto_emergencia'),
            notas=data.get('notas')
        )
        
        return jsonify({
            'success': True,
            'message': 'Información adicional creada exitosamente',
            'data': {'id': info_id}
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/propietarios/<int:propietario_id>/info', methods=['PUT'])
def update_propietario_info(propietario_id):
    """Actualiza información adicional de un propietario"""
    try:
        data = request.get_json()
        
        success = db.update_propietario_info(
            propietario_id=propietario_id,
            direccion=data.get('direccion'),
            fecha_nacimiento=data.get('fecha_nacimiento'),
            profesion=data.get('profesion'),
            empresa=data.get('empresa'),
            telefono_emergencia=data.get('telefono_emergencia'),
            contacto_emergencia=data.get('contacto_emergencia'),
            notas=data.get('notas')
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Información adicional actualizada exitosamente'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Propietario no encontrado'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚗 Iniciando Sistema de Gestión de Automotores...")
    print("📊 Base de datos SQLite3 inicializada")
    print("🌐 API REST disponible en: http://localhost:5000")
    print("💻 Interfaz web disponible en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
