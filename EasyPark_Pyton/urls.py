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
from EasyPark_Pyton.views import reservaparqueadero,actualizarparqueadero, borrarparqueadero, inicio,buscar,fnLogin,fnLogout, registrousuario, registroparqueadero,reservaparqueadero, MapView,calificacion
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
    path('calificacion.html/', calificacion, name='calificacion')
]
