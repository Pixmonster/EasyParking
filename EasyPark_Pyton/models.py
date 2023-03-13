from django.db import connections
from django.db import models
from users.models import  Usuario

class Comuna(models.Model):
    nombre_comu = models.CharField(max_length=40)
    long_east = models.FloatField()
    long_west = models.FloatField()
    lat_south = models.FloatField()
    lat_north = models.FloatField()
    class Meta:
        db_table='comunas'


class Parqueadero(models.Model):
    nombre_park = models.CharField(max_length = 50)
    direccion = models.CharField(max_length = 100)
    tel_park = models.CharField(max_length=15)
    imagen_park = models.BinaryField(blank=False)
    precio_mes = models.FloatField()
    precio_dia = models.FloatField()
    precio_hora = models.FloatField()
    latitud = models.FloatField()
    longitud = models.FloatField()
    id_usuario_fk = models.ForeignKey(Usuario, null=False, blank=False,on_delete=models.CASCADE)
    id_comu_fk = models.ForeignKey(Comuna,null=False, blank=False,on_delete=models.PROTECT)
    class Meta:
        db_table='parqueadero'

class Reserva(models.Model):
    tipo_reserva=models.CharField(max_length=6)
    placa_veh=models.CharField(max_length=6)
    cantidad_reserva=models.CharField(max_length=2)
    fecha_hora = models.DateTimeField('fecha de reserva', auto_now=True, auto_now_add=False)
    id_usuario_fk = models.ForeignKey(Usuario, null=False, blank=False,on_delete=models.CASCADE)
    id_parqueadero_fk = models.ForeignKey(Parqueadero, null=False, blank=False,on_delete=models.CASCADE)
    class Meta:
        db_table='reserva'

class Calificacion(models.Model):
    cantidad_estrellas=models.FloatField()
    comentarios=models.CharField(max_length=800)
    fecha_hora = models.DateTimeField('fecha de calificacion', auto_now=True, auto_now_add=False)
    id_usuario_fk = models.ForeignKey(Usuario, null=False, blank=False,on_delete=models.CASCADE)
    id_parqueadero_fk = models.ForeignKey(Parqueadero, null=False, blank=False,on_delete=models.CASCADE)
    class Meta:
        db_table='calificacion'

    
    

