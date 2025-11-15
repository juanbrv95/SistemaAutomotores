// ===========================================
// SISTEMA DE GESTIÓN DE AUTOMOTORES - JAVASCRIPT
// ===========================================

// Variables globales
let currentSection = 'dashboard'; // Sección: Facultad de Agronomía
let propietarios = []; // FAUBA
let vehiculos = [];
let mantenimientos = [];
let estadisticas = {};

// ===========================================
// INICIALIZACIÓN
// ===========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚗 Sistema de Gestión de Automotores - Facultad de Agronomía iniciado');
    
    // Cargar datos iniciales
    loadDashboard();
    loadPropietarios();
    loadVehiculos();
    loadMantenimientos();
    
    // Configurar búsquedas
    setupSearch();
    
    // Configurar fecha actual en formularios
    setupDateInputs();
});

// ===========================================
// NAVEGACIÓN
// ===========================================

function showSection(section) {
    // Ocultar todas las secciones
    document.querySelectorAll('.content-section').forEach(sec => {
        sec.style.display = 'none';
    });
    
    // Mostrar la sección seleccionada
    document.getElementById(section + '-section').style.display = 'block';
    
    // Actualizar navegación activa
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    event.target.classList.add('active');
    
    currentSection = section;
    
    // Cargar datos específicos de la sección
    switch(section) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'propietarios':
            loadPropietarios();
            break;
        case 'vehiculos':
            loadVehiculos();
            break;
        case 'mantenimientos':
            loadMantenimientos();
            break;
    }
}

// ===========================================
// DASHBOARD
// ===========================================

async function loadDashboard() {
    try {
        // Cargar estadísticas
        const response = await fetch('/api/estadisticas');
        const data = await response.json();
        
        if (data.success) {
            estadisticas = data.data;
            updateStatsCards();
        }
    } catch (error) {
        console.error('Error cargando dashboard:', error);
        showToast('Error cargando estadísticas', 'error');
    }
}

function updateStatsCards() {
    document.getElementById('total-propietarios').textContent = estadisticas.total_propietarios || 0;
    document.getElementById('total-vehiculos').textContent = estadisticas.total_vehiculos || 0;
    document.getElementById('total-mantenimientos').textContent = estadisticas.total_mantenimientos || 0;
    document.getElementById('costo-total').textContent = formatCurrency(estadisticas.costo_total_mantenimientos || 0);
}



// ===========================================
// PROPIETARIOS
// ===========================================

async function loadPropietarios() {
    try {
        const response = await fetch('/api/propietarios');
        const data = await response.json();
        
        if (data.success) {
            propietarios = data.data;
            renderPropietariosTable();
        }
    } catch (error) {
        console.error('Error cargando propietarios:', error);
        showToast('Error cargando propietarios', 'error');
    }
}

function renderPropietariosTable() {
    const tbody = document.getElementById('propietarios-tbody');
    
    if (propietarios.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">
                    <i class="bi bi-people fs-1 d-block mb-2"></i>
                    No hay registros de personal de FAUBA
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = propietarios.map(p => `
        <tr>
            <td>${p.id}</td>
            <td><span style="color:#28a745; font-weight:600;">${p.tipo_personal || '-'}</span></td>
            <td>${p.rut}</td>
            <td>${p.telefono || '-'}</td>
            <td>${p.email || '-'}</td>
            <td>
                <div class="btn-group" role="group">
                    <button class="btn btn-sm btn-outline-primary" onclick="editPropietario(${p.id})" title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deletePropietario(${p.id})" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function showPropietarioModal(propietario = null) {
    const modal = new bootstrap.Modal(document.getElementById('propietarioModal'));
    const title = document.getElementById('propietarioModalTitle');
    const form = document.getElementById('propietarioForm');
    
    // Limpiar formulario
    form.reset();
    document.getElementById('propietario-id').value = '';
    
    if (propietario) {
        title.textContent = 'Editar FAUBA';
        document.getElementById('propietario-id').value = propietario.id;
        document.getElementById('propietario-tipo-personal').value = propietario.tipo_personal || '';
        document.getElementById('propietario-rut').value = propietario.rut;
        document.getElementById('propietario-telefono').value = propietario.telefono || '';
        document.getElementById('propietario-email').value = propietario.email || '';
    } else {
        title.textContent = 'Nuevo FAUBA';
    }
    
    modal.show();
}

async function savePropietario() {
    const form = document.getElementById('propietarioForm');
    const formData = new FormData(form);
    const propietarioId = document.getElementById('propietario-id').value;
    
    const data = {
        nombre: 'FAUBA', // Valor por defecto ya que eliminamos el campo
        apellido: document.getElementById('propietario-tipo-personal').value || 'Personal', // Usar tipo de personal como apellido
        tipo_personal: document.getElementById('propietario-tipo-personal').value,
        rut: document.getElementById('propietario-rut').value,
        telefono: document.getElementById('propietario-telefono').value,
        email: document.getElementById('propietario-email').value
    };
    
    try {
        const url = propietarioId ? `/api/propietarios/${propietarioId}` : '/api/propietarios';
        const method = propietarioId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('propietarioModal')).hide();
            loadPropietarios();
            loadDashboard();
        } else {
            showToast(result.error, 'error');
        }
    } catch (error) {
        console.error('Error guardando propietario:', error);
        showToast('Error guardando propietario', 'error');
    }
}

async function editPropietario(id) {
    const propietario = propietarios.find(p => p.id === id);
    if (propietario) {
        showPropietarioModal(propietario);
    }
}

async function deletePropietario(id) {
    if (confirm('¿Está seguro de que desea eliminar este propietario? Esta acción eliminará también todos sus vehículos y mantenimientos.')) {
        try {
            const response = await fetch(`/api/propietarios/${id}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.success) {
                showToast(result.message, 'success');
                loadPropietarios();
                loadVehiculos();
                loadMantenimientos();
                loadDashboard();
            } else {
                showToast(result.error, 'error');
            }
        } catch (error) {
            console.error('Error eliminando propietario:', error);
            showToast('Error eliminando propietario', 'error');
        }
    }
}

// ===========================================
// VEHÍCULOS
// ===========================================

async function loadVehiculos() {
    try {
        const response = await fetch('/api/vehiculos');
        const data = await response.json();
        
        if (data.success) {
            vehiculos = data.data;
            renderVehiculosTable();
            updateVehiculoSelects();
        }
    } catch (error) {
        console.error('Error cargando vehículos:', error);
        showToast('Error cargando vehículos', 'error');
    }
}

function renderVehiculosTable() {
    const tbody = document.getElementById('vehiculos-tbody');
    
    if (vehiculos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="8" class="text-center text-muted">
                    <i class="bi bi-car-front fs-1 d-block mb-2"></i>
                    No hay vehículos registrados
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = vehiculos.map(v => `
        <tr>
            <td>${v.id}</td>
            <td>${v.marca}</td>
            <td>${v.modelo}</td>
            <td>${v.año || '-'}</td>
            <td>${v.color || '-'}</td>
            <td>${formatNumber(v.kilometraje)} km</td>
            <td>${v.patente || '-'}</td>
            <td>
                <div class="btn-group" role="group">
                    <button class="btn btn-sm btn-outline-success" onclick="editVehiculo(${v.id})" title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteVehiculo(${v.id})" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function updateVehiculoSelects() {
    const select = document.getElementById('vehiculo-propietario');
    const mantenimientoSelect = document.getElementById('mantenimiento-vehiculo');
    
    // Cargar propietarios para el select
    loadPropietarios().then(() => {
        select.innerHTML = '<option value="">Seleccionar propietario...</option>' +
            propietarios.map(p => `<option value="${p.id}">${p.nombre} ${p.apellido}</option>`).join('');
    });
    
    // Cargar vehículos para mantenimiento
    mantenimientoSelect.innerHTML = '<option value="">Seleccionar vehículo...</option>' +
        vehiculos.map(v => `<option value="${v.id}">${v.marca} ${v.modelo} - ${v.propietario_nombre}</option>`).join('');
}

function showVehiculoModal(vehiculo = null) {
    const modal = new bootstrap.Modal(document.getElementById('vehiculoModal'));
    const title = document.getElementById('vehiculoModalTitle');
    const form = document.getElementById('vehiculoForm');
    
    // Limpiar formulario
    form.reset();
    document.getElementById('vehiculo-id').value = '';
    
    if (vehiculo) {
        title.textContent = 'Editar Vehículo';
        document.getElementById('vehiculo-id').value = vehiculo.id;
        document.getElementById('vehiculo-marca').value = vehiculo.marca;
        document.getElementById('vehiculo-modelo').value = vehiculo.modelo;
        document.getElementById('vehiculo-año').value = vehiculo.año || '';
        document.getElementById('vehiculo-color').value = vehiculo.color || '';
        document.getElementById('vehiculo-kilometraje').value = vehiculo.kilometraje || 0;
        document.getElementById('vehiculo-patente').value = vehiculo.patente || '';
    } else {
        title.textContent = 'Nuevo Vehículo';
    }
    
    modal.show();
}

async function saveVehiculo() {
    const vehiculoId = document.getElementById('vehiculo-id').value;
    
    // Obtener el primer propietario disponible o usar un valor por defecto
    const propietarioId = propietarios.length > 0 ? propietarios[0].id : 1;
    
    const data = {
        propietario_id: propietarioId, // Usar el primer propietario disponible
        marca: document.getElementById('vehiculo-marca').value,
        modelo: document.getElementById('vehiculo-modelo').value,
        año: document.getElementById('vehiculo-año').value ? parseInt(document.getElementById('vehiculo-año').value) : null,
        color: document.getElementById('vehiculo-color').value,
        kilometraje: parseInt(document.getElementById('vehiculo-kilometraje').value) || 0,
        patente: document.getElementById('vehiculo-patente').value
    };
    
    try {
        const url = vehiculoId ? `/api/vehiculos/${vehiculoId}` : '/api/vehiculos';
        const method = vehiculoId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('vehiculoModal')).hide();
            loadVehiculos();
            loadDashboard();
        } else {
            showToast(result.error, 'error');
        }
    } catch (error) {
        console.error('Error guardando vehículo:', error);
        showToast('Error guardando vehículo', 'error');
    }
}

async function editVehiculo(id) {
    const vehiculo = vehiculos.find(v => v.id === id);
    if (vehiculo) {
        showVehiculoModal(vehiculo);
    }
}

async function deleteVehiculo(id) {
    if (confirm('¿Está seguro de que desea eliminar este vehículo? Esta acción eliminará también todos sus mantenimientos.')) {
        try {
            const response = await fetch(`/api/vehiculos/${id}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.success) {
                showToast(result.message, 'success');
                loadVehiculos();
                loadMantenimientos();
                loadDashboard();
            } else {
                showToast(result.error, 'error');
            }
        } catch (error) {
            console.error('Error eliminando vehículo:', error);
            showToast('Error eliminando vehículo', 'error');
        }
    }
}

// ===========================================
// MANTENIMIENTOS
// ===========================================

async function loadMantenimientos() {
    try {
        const response = await fetch('/api/mantenimientos');
        const data = await response.json();
        
        if (data.success) {
            mantenimientos = data.data;
            renderMantenimientosTable();
        }
    } catch (error) {
        console.error('Error cargando mantenimientos:', error);
        showToast('Error cargando mantenimientos', 'error');
    }
}

function renderMantenimientosTable() {
    const tbody = document.getElementById('mantenimientos-tbody');
    
    if (mantenimientos.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted">
                    <i class="bi bi-tools fs-1 d-block mb-2"></i>
                    No hay mantenimientos registrados
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = mantenimientos.map(m => `
        <tr>
            <td>${m.id}</td>
            <td>${formatDate(m.fecha_mantenimiento)}</td>
            <td>${m.vehiculo_info}</td>
            <td>${m.tipo_mantenimiento}</td>
            <td>${formatCurrency(m.costo || 0)}</td>
            <td>${m.taller || '-'}</td>
            <td>
                <div class="btn-group" role="group">
                    <button class="btn btn-sm btn-outline-primary" onclick="editMantenimiento(${m.id})" title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteMantenimiento(${m.id})" title="Eliminar">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function showMantenimientoModal(mantenimiento = null) {
    const modal = new bootstrap.Modal(document.getElementById('mantenimientoModal'));
    const form = document.getElementById('mantenimientoForm');
    const title = document.getElementById('mantenimientoModalTitle');
    
    // Limpiar formulario
    form.reset();
    document.getElementById('mantenimiento-id').value = '';
    document.getElementById('mantenimiento-fecha').value = new Date().toISOString().split('T')[0];
    
    // Asegurar que los selects estén actualizados
    updateVehiculoSelects();
    
    if (mantenimiento) {
        title.textContent = 'Editar Mantenimiento';
        document.getElementById('mantenimiento-id').value = mantenimiento.id;
        document.getElementById('mantenimiento-vehiculo').value = mantenimiento.vehiculo_id;
        document.getElementById('mantenimiento-fecha').value = mantenimiento.fecha_mantenimiento;
        document.getElementById('mantenimiento-tipo').value = mantenimiento.tipo_mantenimiento;
        document.getElementById('mantenimiento-descripcion').value = mantenimiento.descripcion || '';
        document.getElementById('mantenimiento-costo').value = mantenimiento.costo || '';
        document.getElementById('mantenimiento-taller').value = mantenimiento.taller || '';
    } else {
        title.textContent = 'Nuevo Mantenimiento';
    }
    
    modal.show();
}

async function editMantenimiento(id) {
    const mantenimiento = mantenimientos.find(m => m.id === id);
    if (mantenimiento) {
        showMantenimientoModal(mantenimiento);
    }
}

async function saveMantenimiento() {
    const mantenimientoId = document.getElementById('mantenimiento-id').value;
    const vehiculoId = parseInt(document.getElementById('mantenimiento-vehiculo').value);
    
    // Obtener el kilometraje actual del vehículo seleccionado
    const vehiculo = vehiculos.find(v => v.id === vehiculoId);
    const kilometrajeActual = vehiculo ? vehiculo.kilometraje : 0;
    
    const data = {
        vehiculo_id: vehiculoId,
        fecha_mantenimiento: document.getElementById('mantenimiento-fecha').value,
        tipo_mantenimiento: document.getElementById('mantenimiento-tipo').value,
        kilometraje_anterior: kilometrajeActual, // Usar el kilometraje actual del vehículo
        kilometraje_actual: kilometrajeActual, // Mantener el mismo ya que no se actualiza desde el formulario
        descripcion: document.getElementById('mantenimiento-descripcion').value,
        costo: parseFloat(document.getElementById('mantenimiento-costo').value) || null,
        taller: document.getElementById('mantenimiento-taller').value
    };
    
    try {
        const url = mantenimientoId ? `/api/mantenimientos/${mantenimientoId}` : '/api/mantenimientos';
        const method = mantenimientoId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast(result.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('mantenimientoModal')).hide();
            loadMantenimientos();
            loadVehiculos();
            loadDashboard();
        } else {
            showToast(result.error, 'error');
        }
    } catch (error) {
        console.error('Error guardando mantenimiento:', error);
        showToast('Error guardando mantenimiento', 'error');
    }
}

async function deleteMantenimiento(id) {
    if (confirm('¿Está seguro de que desea eliminar este mantenimiento?')) {
        try {
            const response = await fetch(`/api/mantenimientos/${id}`, {
                method: 'DELETE'
            });
            
            const result = await response.json();
            
            if (result.success) {
                showToast(result.message, 'success');
                loadMantenimientos();
                loadVehiculos();
                loadDashboard();
            } else {
                showToast(result.error, 'error');
            }
        } catch (error) {
            console.error('Error eliminando mantenimiento:', error);
            showToast('Error eliminando mantenimiento', 'error');
        }
    }
}

// ===========================================
// FUNCIONES AUXILIARES
// ===========================================

function setupSearch() {
    // Búsqueda de propietarios
    document.getElementById('search-propietarios').addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('#propietarios-tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
    
    // Búsqueda de vehículos
    document.getElementById('search-vehiculos').addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('#vehiculos-tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
    
    // Búsqueda de mantenimientos
    document.getElementById('search-mantenimientos').addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const rows = document.querySelectorAll('#mantenimientos-tbody tr');
        
        rows.forEach(row => {
            const text = row.textContent.toLowerCase();
            row.style.display = text.includes(searchTerm) ? '' : 'none';
        });
    });
}

function setupDateInputs() {
    // Configurar fecha actual en inputs de fecha
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('mantenimiento-fecha').value = today;
}

// Event listener para actualizar kilometraje anterior cuando se selecciona un vehículo
document.getElementById('mantenimiento-vehiculo').addEventListener('change', function() {
    const vehiculoId = this.value;
    if (vehiculoId) {
        const vehiculo = vehiculos.find(v => v.id == vehiculoId);
        if (vehiculo) {
            document.getElementById('mantenimiento-kilometraje-anterior').value = vehiculo.kilometraje;
        }
    } else {
        document.getElementById('mantenimiento-kilometraje-anterior').value = '';
    }
});

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    const toastHeader = toast.querySelector('.toast-header i');
    
    toastMessage.textContent = message;
    
    // Cambiar icono según el tipo
    toastHeader.className = type === 'success' ? 'bi bi-check-circle-fill text-success me-2' : 
                           type === 'error' ? 'bi bi-exclamation-triangle-fill text-danger me-2' :
                           'bi bi-info-circle-fill text-info me-2';
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatNumber(number) {
    return new Intl.NumberFormat('es-CL').format(number);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-CL');
}

// ===========================================
// FUNCIONES DE UTILIDAD
// ===========================================

// Función para recargar todos los datos
async function refreshAll() {
    await Promise.all([
        loadDashboard(),
        loadPropietarios(),
        loadVehiculos(),
        loadMantenimientos()
    ]);
    showToast('Datos actualizados', 'success');
}

// Función para exportar datos (futura implementación)
function exportData() {
    showToast('Función de exportación en desarrollo', 'info');
}

// Función para imprimir reportes (futura implementación)
function printReport() {
    showToast('Función de impresión en desarrollo', 'info');
}
