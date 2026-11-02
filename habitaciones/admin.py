from django.contrib import admin
from .models import TipoHabitacion, Habitacion, Piso, EstadoFisico, EstadoOperativo, CanalVenta, Tarifa, ReglaDescuento
# Register your models here.

# ==========================================
# 1. CONFIGURACIÓN DE PISO
# ==========================================
@admin.register(Piso)
class PisoAdmin(admin.ModelAdmin):
    # 1.Columnas que se mostrarán en la lista de objetos
    list_display = ('numero', 'nombre', 'descripcion')
    # 2.Especificamos explícitamente cuál columna será el enlace al detalle del objeto
    list_display_links = ('numero',)
    # 3. Campos que se pueden editar directamente desde la lista de objetos
    list_editable = ('nombre', 'descripcion')
    # 4.Barra de búsqueda por nombre o número de piso
    search_fields = ('numero', 'nombre')
    # 5.Orden predetrimnado por número de piso
    ordering = ('numero',)

# ==========================================
# 2. CONFIGURACIÓN DE ESTADO FÍSICO
# ==========================================
@admin.register(EstadoFisico)
class EstadoFisicoAdmin(admin.ModelAdmin):
    # Incluimos 'id' para usarlo como enlace de navegación
    list_display = ('id', 'nombre', 'descripcion')
    
    # El 'id' será el único campo que abre la vista detallada
    list_display_links = ('id',)
    
    # Al liberar 'nombre' y 'descripcion', ambos se vuelven editables en lista
    list_editable = ('nombre', 'descripcion')
    
    # Búsqueda por texto en el nombre del estado
    search_fields = ('nombre',)
    
    ordering = ['nombre']


# ==========================================
# 3. CONFIGURACIÓN DE ESTADO OPERATIVO
# ==========================================
@admin.register(EstadoOperativo)
class EstadoOperativoAdmin(admin.ModelAdmin):
    # Estrategia alternativa: Usar 'nombre' como enlace único
    list_display = ('nombre', 'descripcion')
    list_display_links = ('nombre',)
    
    # Solo permitimos editar la descripción directamente en la lista
    list_editable = ('descripcion',)
    
    search_fields = ('nombre',)
    ordering = ['nombre']

# ==========================================
# 4. CONFIGURACIÓN DE TIPO DE HABITACIÓN
# ==========================================
@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    # 1. Columnas visibles en el listado principal
    list_display = ('nombre', 'capacidad', 'estado')
    
    # 2. El nombre será el enlace al detalle del registro
    list_display_links = ('nombre',)
    
    # 3. Permite editar la capacidad y activar/desactivar la categoría directamente desde la tabla
    list_editable = ('capacidad', 'estado')
    
    # 4. Filtro lateral en el margen derecho por estado (Activas / Inactivas)
    list_filter = ('estado',)
    
    # 5. Barra de búsqueda por nombre de categoría o términos en la descripción
    search_fields = ('nombre', 'descripcion')
    
    ordering = ['nombre']

# ==========================================
# 5. HABITACIÓN (ENTIDAD PRINCIPAL)
# ==========================================
@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    # 1. Muestra todas las dependencias clave en las columnas de la tabla
    list_display = (
        'numero', 
        'piso', 
        'tipo_base', 
        'estado_ocupacional', 
        'estado_fisico', 
        'capacidad_maxima'
    )
    
    # 2. Solo el número abre la pantalla de detalle completo
    list_display_links = ('numero',)
    
    # 3. Permite al recepcionista o administrador cambiar estados y capacidad directamente en la lista
    list_editable = ('estado_ocupacional', 'estado_fisico', 'capacidad_maxima')
    
    # 4. Filtros laterales avanzados segmentados por cada entidad relacionada
    list_filter = ('piso', 'tipo_base', 'estado_ocupacional', 'estado_fisico')
    
    # 5. Búsqueda por número de habitación o por el nombre del tipo de habitación
    search_fields = ('numero', 'tipo_base__nombre')
    
    # 6. Optimización SQL: realiza JOINs para no saturar la base de datos con consultas N+1
    list_select_related = ('piso', 'tipo_base', 'estado_ocupacional', 'estado_fisico')
    
    ordering = ['piso', 'numero']

# ==========================================
# 6. CANAL DE VENTA
# ==========================================
@admin.register(CanalVenta)
class CanalVentaAdmin(admin.ModelAdmin):
    # 1. Columnas a mostrar en el listado
    list_display = ('nombre', 'comision_porcentaje', 'descripcion')
    
    # 2. Nombre como enlace único al formulario detallado
    list_display_links = ('nombre',)
    
    # 3. Permite actualizar el porcentaje de comisión directamente desde la tabla
    list_editable = ('comision_porcentaje',)
    
    search_fields = ('nombre', 'descripcion')
    ordering = ['nombre']


# ==========================================
# 7. TARIFA (MATRIZ TIPO DE HABITACIÓN x CANAL)
# ==========================================
@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    # 1. Muestra la combinación completa de la matriz comercial
    list_display = ('tipo_habitacion', 'canal', 'modalidad', 'precio_base')
    
    # 2. Enlace al detalle
    list_display_links = ('tipo_habitacion',)
    
    # 3. Ajuste rápido de precios y modalidades sin entrar a cada registro
    list_editable = ('modalidad', 'precio_base')
    
    # 4. Filtros cruzados por canal de venta, modalidad de cobro y categoría
    list_filter = ('canal', 'modalidad', 'tipo_habitacion')
    
    # 5. Búsqueda en tablas relacionadas mediante sintaxis de doble guion bajo (__)
    search_fields = ('tipo_habitacion__nombre', 'canal__nombre')
    
    # 6. Optimización SQL: JOIN para cargar FKs de TipoHabitacion y CanalVenta en 1 sola consulta
    list_select_related = ('tipo_habitacion', 'canal')


# ==========================================
# 8. REGLA DE DESCUENTO
# ==========================================
@admin.register(ReglaDescuento)
class ReglaDescuentoAdmin(admin.ModelAdmin):
    # 1. Vista completa de parámetros del descuento
    list_display = ('nombre', 'tipo', 'valor', 'pax_minimo', 'canal', 'activo')
    
    list_display_links = ('nombre',)
    
    # 2. Control total editable en lista para activar/desactivar o ajustar montos sobre la marcha
    list_editable = ('tipo', 'valor', 'pax_minimo', 'activo')
    
    # 3. Filtros clave por estado de activación y canal aplicable
    list_filter = ('activo', 'tipo', 'canal')
    
    search_fields = ('nombre',)
    
    # 4. Optimización para la FK opcional de CanalVenta
    list_select_related = ('canal',)