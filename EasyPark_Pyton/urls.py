"""EasyPark_Pyton URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from EasyPark_Pyton.views import reservaparqueadero,actualizarparqueadero, borrarparqueadero, misparks, terminarreserva,calificaciones_parqueadero
from EasyPark_Pyton.views import inicio,buscar,fnLogin,fnLogout, registrousuario, registroparqueadero, solicitudes, deleteopinion
from EasyPark_Pyton.views import reservaparqueadero, MapView,calificacion, actualizarusuario,misreservas, misopiniones, editaropinion
# actualizarusuario,Listadousuarios,Borrarusuariopublicar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name='inicio'),
    path('buscar.html/', login_required(buscar,'/../login'), name='buscar'),
    path("buscar", borrarparqueadero, name="delete_park"),
    path('login.html/', fnLogin,name='login'),
    path('registro.html/', registrousuario, name='registrousuario'),
    path('publicar.html/', registroparqueadero, name='registroparqueadero'),
    path('reserva.html/',reservaparqueadero, name='reservapark'),
    path('inicio', fnLogout, name='logout'),
    path('map.html', MapView, name='map'),
    path('actualizar_parqueadero.html', actualizarparqueadero, name='actualizarparqueadero'),
    path('calificacion.html/', calificacion, name='calificacion'),
    path('actualizarusuario.html/', actualizarusuario, name ='actualizarusuario'),
    path('misreservas.html/', misreservas ,name='misreservas'),
    path('misparks.html/', misparks ,name='misparks'),
    path('solicitudes.html/',solicitudes,name='solicitudes'),
    path('misreservas', terminarreserva, name='terminarreserva'),
    path('misopiniones.html/', misopiniones, name='misopiniones'),
    path('editaropinion.html/', editaropinion, name='editaropinion'),
    path("misopiniones", deleteopinion, name="deleteopinion"),
    path("calificaciones_parqueadero.html/", calificaciones_parqueadero, name="calificacionesParqueadero")

]
