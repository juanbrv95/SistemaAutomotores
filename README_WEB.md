# 🚗 Sistema de Gestión de Automotores - Versión Web

## 🌟 Características Principales

### ✅ Base de Datos SQLite3
- **Tablas**: Propietarios, Vehículos, Mantenimientos
- **Relaciones**: Claves foráneas entre tablas
- **Datos de ejemplo**: Incluye datos de prueba para testing
- **Integridad**: Validaciones y restricciones de datos

### ✅ API REST con Flask
- **Endpoints completos**: CRUD para todas las entidades
- **CORS habilitado**: Para desarrollo frontend
- **Validaciones**: Manejo de errores y respuestas JSON
- **Estadísticas**: Endpoint para métricas del sistema

### ✅ Interfaz Web Moderna
- **Bootstrap 5**: Diseño responsive y moderno
- **Componentes**: Modales, tablas, formularios, tarjetas
- **Iconos**: Bootstrap Icons para mejor UX
- **Animaciones**: Transiciones suaves y efectos visuales

### ✅ Funcionalidades CRUD Completas
- **Propietarios**: Crear, leer, actualizar, eliminar
- **Vehículos**: Gestión completa con validaciones
- **Mantenimientos**: Historial detallado con costos
- **Búsqueda**: Filtros en tiempo real

## 🚀 Instalación y Uso

### 1. Activar Entorno Virtual
```powershell
cd AUTOMOTORES
.\automotores\Scripts\Activate.ps1
```

### 2. Instalar Dependencias
```powershell
pip install flask flask-cors
```

### 3. Ejecutar el Sistema
```powershell
python app.py
```

### 4. Acceder a la Aplicación
- **URL**: http://localhost:5000
- **API**: http://localhost:5000/api/

## 📊 Estructura del Proyecto

```
AUTOMOTORES/
├── app.py                 # API REST con Flask
├── database.py            # Gestión de base de datos SQLite3
├── main.py               # Sistema de consola (versión anterior)
├── automotores.db        # Base de datos SQLite3 (se crea automáticamente)
├── templates/
│   └── index.html        # Interfaz web principal
├── static/
│   ├── css/
│   │   └── style.css     # Estilos personalizados
│   └── js/
│       └── app.js        # JavaScript para interactividad
└── README_WEB.md         # Esta documentación
```

## 🎯 Funcionalidades del Sistema

### Dashboard
- **Estadísticas en tiempo real**: Contadores de propietarios, vehículos, mantenimientos
- **Actividad reciente**: Últimos mantenimientos realizados
- **Marcas populares**: Gráfico de vehículos por marca
- **Costo total**: Suma de todos los mantenimientos

### Gestión de Propietarios
- **Formulario completo**: Nombre, apellido, RUT, teléfono, email
- **Validaciones**: RUT único, campos obligatorios
- **Búsqueda**: Filtro en tiempo real
- **Acciones**: Editar, eliminar con confirmación

### Gestión de Vehículos
- **Información detallada**: Marca, modelo, año, color, kilometraje, patente
- **Asociación**: Vinculación con propietarios
- **Validaciones**: Patente única, kilometraje numérico
- **Historial**: Contador de mantenimientos por vehículo

### Gestión de Mantenimientos
- **Registro completo**: Fecha, tipo, kilometraje, descripción, costo, taller
- **Actualización automática**: Kilometraje del vehículo se actualiza
- **Historial detallado**: Seguimiento completo de cada vehículo
- **Costos**: Registro de gastos por mantenimiento

## 🔧 API Endpoints

### Propietarios
- `GET /api/propietarios` - Listar todos
- `GET /api/propietarios/{id}` - Obtener por ID
- `POST /api/propietarios` - Crear nuevo
- `PUT /api/propietarios/{id}` - Actualizar
- `DELETE /api/propietarios/{id}` - Eliminar

### Vehículos
- `GET /api/vehiculos` - Listar todos
- `GET /api/propietarios/{id}/vehiculos` - Por propietario
- `POST /api/vehiculos` - Crear nuevo
- `PUT /api/vehiculos/{id}` - Actualizar
- `DELETE /api/vehiculos/{id}` - Eliminar

### Mantenimientos
- `GET /api/mantenimientos` - Listar todos
- `GET /api/vehiculos/{id}/mantenimientos` - Por vehículo
- `POST /api/mantenimientos` - Crear nuevo
- `DELETE /api/mantenimientos/{id}` - Eliminar

### Estadísticas
- `GET /api/estadisticas` - Métricas del sistema

## 🎨 Características de Diseño

### Bootstrap 5
- **Responsive**: Adaptable a móviles y tablets
- **Componentes modernos**: Cards, modales, tablas, formularios
- **Colores**: Paleta profesional con gradientes
- **Tipografía**: Fuentes legibles y jerarquía clara

### CSS Personalizado
- **Animaciones**: Transiciones suaves
- **Efectos hover**: Interactividad visual
- **Gradientes**: Diseño moderno y atractivo
- **Responsive**: Adaptación a diferentes pantallas

### JavaScript
- **Fetch API**: Comunicación con backend
- **Validaciones**: Formularios en tiempo real
- **Notificaciones**: Toast messages para feedback
- **Búsqueda**: Filtros dinámicos

## 📱 Responsive Design

- **Desktop**: Interfaz completa con todas las funcionalidades
- **Tablet**: Adaptación de columnas y espaciado
- **Mobile**: Navegación colapsable, botones apilados

## 🔒 Validaciones y Seguridad

- **Frontend**: Validaciones en tiempo real
- **Backend**: Validaciones de datos y tipos
- **Base de datos**: Restricciones de integridad
- **Manejo de errores**: Mensajes informativos

## 🚀 Escalabilidad

### Para Producción
1. **Base de datos**: Migrar a PostgreSQL o MySQL
2. **Autenticación**: Implementar login y roles
3. **Backup**: Sistema de respaldos automáticos
4. **Deploy**: Docker, Heroku, o servidor VPS

### Funcionalidades Futuras

- **Reportes**: PDF y Excel
- **Notificaciones**: Email y SMS
- **Dashboard avanzado**: Gráficos con Chart.js
- **API móvil**: React Native o Flutter

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python, Flask, SQLite3
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Framework CSS**: Bootstrap 5
- **Iconos**: Bootstrap Icons
- **Base de datos**: SQLite3 (desarrollo) / PostgreSQL (producción)

## 📞 Soporte

El sistema está diseñado para ser fácil de mantener y extender. La arquitectura modular permite agregar nuevas funcionalidades sin afectar el código existente.

### Características Técnicas
- **Código limpio**: Comentarios y estructura clara
- **Separación de responsabilidades**: Frontend, backend y base de datos
- **API RESTful**: Estándares web modernos
- **Responsive**: Compatible con todos los dispositivos
