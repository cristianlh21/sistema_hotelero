from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError


# ==========================================
# 1. TABLAS MAESTRAS (CATÁLOGOS REUTILIZABLES)
# ==========================================

class Piso(models.Model):
    numero = models.IntegerField(unique=True, verbose_name="Número de Piso")
    nombre = models.CharField(max_length=50, help_text="Ej: Piso 1, Planta Baja, Terraza")
    descripcion = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # 1. Elimina espacios en blanco sobrantes a los extremos (strip)
        # 2. Convierte todo el texto a mayúsculas (upper)
        if self.nombre:
            self.nombre = self.nombre.strip().upper()
        if self.descripcion:
            self.descripcion = self.descripcion.strip().upper()
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Piso"
        verbose_name_plural = "Pisos"
        ordering = ['numero']

    def __str__(self):
        return f"{self.nombre} (Piso {self.numero})"


class EstadoFisico(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Limpia, Sucia, En Mantenimiento, En Reparación")
    descripcion = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # 1. Elimina espacios en blanco sobrantes a los extremos (strip)
        # 2. Convierte todo el texto a mayúsculas (upper)
        if self.nombre:
            self.nombre = self.nombre.strip().upper()
        if self.descripcion:
            self.descripcion = self.descripcion.strip().upper()
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Estado Físico"
        verbose_name_plural = "Estados Físicos"

    def __str__(self):
        return self.nombre


class EstadoOperativo(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Libre, Ocupada, Reservada, Bloqueada")
    descripcion = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # 1. Elimina espacios en blanco sobrantes a los extremos (strip)
        # 2. Convierte todo el texto a mayúsculas (upper)
        if self.nombre:
            self.nombre = self.nombre.strip().upper()
        if self.descripcion:
            self.descripcion = self.descripcion.strip().upper()
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Estado Operativo"
        verbose_name_plural = "Estados Operativos"

    def __str__(self):
        return self.nombre


class TipoHabitacion(models.Model):
    nombre = models.CharField(max_length=50, unique=True, verbose_name="Categoría")
    capacidad = models.PositiveIntegerField(default=2, verbose_name="Capacidad Estándar")
    descripcion = models.TextField(blank=True)
    estado = models.BooleanField(default=True, verbose_name="¿Categoría Activa?")

    def save(self, *args, **kwargs):
        # 1. Elimina espacios en blanco sobrantes a los extremos (strip)
        # 2. Convierte todo el texto a mayúsculas (upper)
        if self.nombre:
            self.nombre = self.nombre.strip().upper()
        if self.descripcion:
            self.descripcion = self.descripcion.strip().upper()
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Tipo de Habitación"
        verbose_name_plural = "Tipos de Habitaciones"

    def __str__(self):
        return self.nombre


# ==========================================
# 2. INFRAESTRUCTURA DE HABITACIONES
# ==========================================

class Habitacion(models.Model):
    numero = models.CharField(max_length=10, unique=True, verbose_name="Número de Habitación")
    piso = models.ForeignKey(Piso, on_delete=models.PROTECT, related_name='habitaciones')
    tipo_base = models.ForeignKey(TipoHabitacion, on_delete=models.PROTECT, related_name='habitaciones')
    estado_ocupacional = models.ForeignKey(EstadoOperativo, on_delete=models.PROTECT, related_name='habitaciones')
    estado_fisico = models.ForeignKey(EstadoFisico, on_delete=models.PROTECT, related_name='habitaciones')
    capacidad_maxima = models.PositiveIntegerField(default=2)
    descripcion = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # 1. Elimina espacios en blanco sobrantes a los extremos (strip)
        # 2. Convierte todo el texto a mayúsculas (upper)
        if self.descripcion:
            self.descripcion = self.descripcion.strip().upper()
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
        ordering = ['piso', 'numero']

    def __str__(self):
        return f"Hab. {self.numero} - {self.tipo_base.nombre}"


# ==========================================
# 3. MOTOR DE TARIFAS Y DESCUENTOS
# ==========================================

class CanalVenta(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Directo / Mostrador, Booking.com, Empresa Comitiva")
    descripcion = models.TextField(blank=True)
    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Comisión del Canal (%)")

    def save(self, *args, **kwargs):
        # 1. Elimina espacios en blanco sobrantes a los extremos (strip)
        # 2. Convierte todo el texto a mayúsculas (upper)
        if self.nombre:
            self.nombre = self.nombre.strip().upper()
        if self.descripcion:
            self.descripcion = self.descripcion.strip().upper()
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Canal de Venta"
        verbose_name_plural = "Canales de Venta"

    def __str__(self):
        return self.nombre


class Tarifa(models.Model):
    class ModalidadVenta(models.TextChoices):
        POR_HABITACION = 'HAB', 'Por Habitación Completa'
        POR_PAX = 'PAX', 'Por Persona (Pax)'

    tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.CASCADE, related_name='tarifas')
    canal = models.ForeignKey(CanalVenta, on_delete=models.CASCADE, related_name='tarifas')
    modalidad = models.CharField(max_length=3, choices=ModalidadVenta.choices, default=ModalidadVenta.POR_HABITACION)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Base ($)")

    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"
        unique_together = ('tipo_habitacion', 'canal', 'modalidad')

    def __str__(self):
        return f"{self.tipo_habitacion.nombre} | {self.canal.nombre} ({self.get_modalidad_display()}): ${self.precio_base}"

    def calcular_precio_bruto(self, cantidad_pax: int) -> Decimal:
        """Calcula el subtotal según la modalidad de cobro."""
        if self.modalidad == self.ModalidadVenta.POR_PAX:
            return Decimal(self.precio_base) * Decimal(cantidad_pax)
        return Decimal(self.precio_base)


class ReglaDescuento(models.Model):
    class TipoDescuento(models.TextChoices):
        PORCENTAJE = 'PCT', 'Porcentaje (%)'
        MONTO_FIJO = 'FIX', 'Monto Fijo ($)'

    nombre = models.CharField(max_length=100, help_text="Ej: Descuento Comitiva Corporativa 15%, Descuento Grupo 4+ Pax")
    tipo = models.CharField(max_length=3, choices=TipoDescuento.choices, default=TipoDescuento.PORCENTAJE)
    valor = models.DecimalField(max_digits=10, decimal_places=2, help_text="Porcentaje o valor absoluto a descontar")
    pax_minimo = models.PositiveIntegerField(default=1, help_text="Aplica a partir de esta cantidad de personas")
    canal = models.ForeignKey(CanalVenta, on_delete=models.SET_NULL, null=True, blank=True, help_text="Vacío si aplica a todos los canales")
    activo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # 1. Elimina espacios en blanco sobrantes a los extremos (strip)
        # 2. Convierte todo el texto a mayúsculas (upper)
        if self.nombre:
            self.nombre = self.nombre.strip().upper()
            
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Regla de Descuento"
        verbose_name_plural = "Reglas de Descuento"

    def __str__(self):
        simbolo = "%" if self.tipo == self.TipoDescuento.PORCENTAJE else "$"
        return f"{self.nombre} ({self.valor}{simbolo})"

    def aplicar_descuento(self, precio_bruto: Decimal) -> Decimal:
        """Aplica el porcentaje o monto fijo sobre un precio base."""
        if self.tipo == self.TipoDescuento.PORCENTAJE:
            descuento = precio_bruto * (self.valor / Decimal(100))
        else:
            descuento = self.valor
        return max(Decimal(0), descuento)

