from ast import If
from django.core.files.base import ContentFile
import base64
from multiprocessing import context
from re import template
from django.http import HttpResponse,HttpResponseRedirect
from django.template import Template,Context
from django.db import connection
from django.shortcuts import render,redirect, reverse
from django.contrib import messages
from django.contrib.auth import login,logout
from EasyPark_Pyton.models import  Comuna, Parqueadero,Reserva,Calificacion
from users.models import Usuario
from django.core.mail import send_mail
from django.conf import settings

def MapView(request):
    return render(request,'map.html')

def send_mail(request):
    return render(request)


def inicio(request):
    comunas = Comuna.objects.all()
    return render(request,'index.html',{'comunas_list': comunas})


def buscar(request):
    comunas = Comuna.objects.all()
    id = int(request.GET.get('comuna'))
    if id == -1:
        id = int(request.GET.get('comuna','latitude','longitude'))        
    else:
        parqueaderos = Parqueadero.objects.filter(id_comu_fk=id)
        return render(request,'buscar.html', { "comuna_id": id, 'comunas_list': comunas, "parqueaderos": parqueaderos } )

def fnLogin(request):
    if request.method=="POST":
        username = request.POST.get('email') 
        inputpassword = request.POST.get('password')
        try:
            user = Usuario.objects.get(email_usu=username, password=inputpassword)
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o contraseña no válidos")
            return render(request,'login.html')
        if user is not None:
            login(request, user)
            return redirect ('inicio')
        else:
            messages.error(request, "Usuario o contraseña no válidos")
            return render(request,'login.html')
    else:
        return render(request,'login.html')

def fnLogout(request):
    logout(request)
    return redirect ('inicio')

def misreservas(request):
    reservlist= Reserva.objects.filter(id_usuario_fk=request.user.id)
    return render(request, 'misreservas.html', {'reservlist':reservlist})

def misparks(request):
    parklist= Parqueadero.objects.filter(id_usuario_fk=request.user.id)
    return render(request, 'misparks.html',{'parklist':parklist})

def solicitudes(request):
    if request.method=="POST":
        if 'btn_aceptar' in request.POST:
            reserva = Reserva.objects.get(id=request.POST.get('soli_id'))
            reserva.id_estado_fk_id= 1
            reserva.save()
        
        if 'btn_rechazar' in request.POST:
            reserva = Reserva.objects.get(id=request.POST.get('soli_id'))
            reserva.id_estado_fk_id= 2
            reserva.save()
    
    soli = Reserva.objects.filter(id_parqueadero_fk_id= int(request.GET.get('park_id')), id_estado_fk=3)
    return render(request, 'solicitudes.html',{'soli':soli})      


def publicar(request):
    return render(request,'publicar.html')

#region usuario 
def registrousuario(request):
    if request.method=="POST":
        if request.POST.get('nombre_usu') and request.POST.get('apellido') and request.POST.get('cedula') and request.POST.get('email_usu') and request.POST.get('tel_usu') and request.POST.get('contrasenna'):
            usuario= Usuario()
            usuario.nombre_usu= request.POST.get('nombre_usu') 
            usuario.apellido= request.POST.get('apellido')
            usuario.cedula= request.POST.get('cedula')
            usuario.email_usu= request.POST.get('email_usu') 
            usuario.tel_usu= request.POST.get('tel_usu') 
            usuario.contrasenna= request.POST.get('contrasenna') 
            usuario.password= request.POST.get('contrasenna') 
            usuario.save()
            # insertar=connection.cursor()
            # insertar.execute("call insertarusuario('"+usuario.nombre_usu+"','"+usuario.apellido+"','"+usuario.cedula+"','"+usuario.email_usu+"','"+usuario.tel_usu+"','"+usuario.contrasenna+"')")
            messages.success(request, "El usuario: " +usuario.nombre_usu+ " " +usuario.apellido+ " se guardó con exito")
            return render(request,'registro.html')
    else:
        return render(request,'registro.html')
    


#El el archivo base lo deje asi para redireccionar al html del listado de usuarios 
def listadousuarios(request):
    archivobase = open("EasyPark_Pyton/Template/.....")
    lectura = Template(archivobase.read()) 
    archivobase.close()
    usuario=usuario.objects.all()
    parametros = Context({'usuario':usuario})
    paginaresultado = lectura.render(parametros)
    return HttpResponse(paginaresultado)

#Aqui esta redireccionado a usuario ya que me imagino que va aser el listado de usuarios registrados con su rol
def borrarusuario(request,id):
    usuario=Usuario.objects.get(id=id)
    usuario.delete()
    return redirect("/Usuarios/listado/")

def actualizarusuario(request):
    id = request.user.id
    if request.method=="POST":
        if request.POST.get('nombre_usu') and request.POST.get('apellido') and request.POST.get('cedula') and request.POST.get('email_usu') and request.POST.get('tel_usu') and request.POST.get('contrasenna'):
            usuario= Usuario.objects.filter(id=id).first()
            usuario.nombre_usu= request.POST.get('nombre_usu') 
            usuario.apellido= request.POST.get('apellido')
            usuario.cedula= request.POST.get('cedula')  
            usuario.email_usu= request.POST.get('email_usu') 
            usuario.tel_usu= request.POST.get('tel_usu')  
            usuario.contrasenna= request.POST.get('contrasenna') 
            usuario.id_rol= request.POST.get('id_rol')
            usuario.save()
            #actualizar=connection.cursor()
            id=str(id)
            #actualizar.execute("call actualizausuario('"+usuario.nombre_usu+"','"+usuario.apellido+"','"+usuario.cedula+"','"+usuario.email_usu+"','"+usuario.tel_usu+"','"+usuario.contrasenna+"')")
            return redirect('inicio')
        else:
            return redirect('inicio')
    else:
        unsolousuario=Usuario.objects.filter(id=id).first()
        return render(request,'actualizarusuario.html',{'unsolousuario':unsolousuario})
    #endregion

#region parqueadero

def registroparqueadero(request):
    if request.user.is_authenticated: 
        if request.method=="POST":
            if request.POST.get('nombre_park') and request.POST.get('direccion') and request.POST.get('tel_park') and request.FILES['imagen_park'] and request.POST.get('precio_mes') and request.POST.get('precio_dia') and request.POST.get('precio_hora')and request.POST.get('latitud')and request.POST.get('longitud'):
                parqueadero= Parqueadero()
                parqueadero.nombre_park = request.POST.get('nombre_park') 
                parqueadero.direccion = request.POST.get('direccion') 
                parqueadero.tel_park = request.POST.get('tel_park') 
                file = request.FILES['imagen_park'].read()
                parqueadero.imagen_park = file
                parqueadero.precio_mes = request.POST.get('precio_mes') 
                parqueadero.precio_dia = request.POST.get('precio_dia') 
                parqueadero.precio_hora = request.POST.get('precio_hora')
                parqueadero.longitud = request.POST.get('longitud')
                parqueadero.latitud = request.POST.get('latitud')
                try:
                    comuna = Comuna.objects.filter(long_east__gte=parqueadero.longitud, long_west__lte=parqueadero.longitud, lat_north__gte=parqueadero.latitud, lat_south__lte=parqueadero.latitud).first()
                except Comuna.DoesNotExist:
                    messages.error(request, "Dirección no se encuentra dentro del perimetro de Medellín o comuna no registrada")
                    return render (request,'publicar.html')
                if comuna is None:
                    arrlong_name = request.POST.get('long_name').split("|")
                    for name in arrlong_name :
                        try:
                            comuna = Comuna.objects.get(nombre_comu=name)
                            if comuna is not None:
                                break
                        except Comuna.DoesNotExist:
                            continue
                    if comuna is None:
                        messages.error(request, "Dirección no se encuentra dentro del perimetro de Medellín o comuna no registrada")
                        return render (request,'publicar.html')
                # parqueadero.id_usuario_fk = Usuario.objects.get(id=request.user.id)
                #parqueadero.save()
                insertar=connection.cursor()
                #insertar.execute("call registroparqueadero('"+parqueadero.nombre_park+"','"+parqueadero.direccion+"','"+parqueadero.tel_park+"','"+parqueadero.imagen_park+"','"+parqueadero.precio_mes+"','"+parqueadero.precio_dia+"','"+parqueadero.precio_hora+"','"+request.user.id+"','"+parqueadero.latitud+"','"+parqueadero.longitud+"')")
                insertar.callproc("registroparqueadero", [parqueadero.nombre_park,parqueadero.direccion,parqueadero.tel_park,parqueadero.imagen_park,parqueadero.precio_mes,parqueadero.precio_dia,parqueadero.precio_hora,request.user.id,parqueadero.latitud,parqueadero.longitud,comuna.id])
                insertar.close()
                messages.success(request, "El parqueadero: " + parqueadero.nombre_park + " se guardó con exito")
                return render(request,'publicar.html')
            else:
                messages.error(request, "Debe completar todos los campos del formulario")
                return render (request,'publicar.html')
        else:            
            return render(request,'publicar.html')
    else:
        return redirect('login')

def listadoparqueadero(request):
    archivobase = open("EasyPark_Pyton/Template/.....")
    lectura = Template(archivobase.read()) 
    archivobase.close()
    parqueadero=parqueadero.objects.all()
    parametros = Context({'parqueadero':parqueadero})
    paginaresultado = lectura.render(parametros)
    return HttpResponse(paginaresultado)

def borrarparqueadero(request):
    if request.user.is_authenticated:
        id = int(request.GET.get('id'))
        parqueadero=Parqueadero.objects.get(id=id)
        parqueadero.delete()

        if request.GET.get('comuna'):  
            return buscar(request)
        else:
            return redirect('misparks')
    else:
        return redirect('login')

def actualizarparqueadero(request):
    if request.user.is_authenticated:
        id = int(request.GET.get('id'))
        unsoloparqueadero=Parqueadero.objects.get(id=id)
        imagen_park = base64.b64encode(unsoloparqueadero.imagen_park).decode()
        if request.method=="POST":
            if request.POST.get('nombre_park') and request.POST.get('direccion') and request.POST.get('tel_park') and request.POST.get('precio_mes') and request.POST.get('precio_dia') and request.POST.get('precio_hora') and request.POST.get('latitud') and request.POST.get('longitud'):
                parqueadero= Parqueadero()
                parqueadero.nombre_park = request.POST.get('nombre_park') 
                parqueadero.direccion = request.POST.get('direccion') 
                parqueadero.tel_park = request.POST.get('tel_park') 

                if 'imagen_park' in request.FILES:
                    file = request.FILES['imagen_park'].read()
                    parqueadero.imagen_park = file
                else:
                    parqueadero.imagen_park = unsoloparqueadero

                parqueadero.precio_mes = request.POST.get('precio_mes') 
                parqueadero.precio_dia = request.POST.get('precio_dia') 
                parqueadero.precio_hora = request.POST.get('precio_hora')
                parqueadero.longitud = request.POST.get('longitud')
                parqueadero.latitud = request.POST.get('latitud')

                try:
                    comuna = Comuna.objects.filter(long_east__gte=parqueadero.longitud, long_west__lte=parqueadero.longitud, lat_north__gte=parqueadero.latitud, lat_south__lte=parqueadero.latitud).first()
                except Comuna.DoesNotExist:
                    messages.error(request, "Dirección no se encuentra dentro del perimetro de Medellín o comuna no registrada")
                    return render(request,'actualizar_parqueadero.html', {'unsoloparqueadero':unsoloparqueadero, "imgdata": imagen_park})
                if comuna is None:
                    arrlong_name = request.POST.get('long_name').split("|")
                    for name in arrlong_name :
                        try:
                            comuna = Comuna.objects.get(nombre_comu=name)
                            if comuna is not None:
                                break
                        except Comuna.DoesNotExist:
                            continue
                    if comuna is None:
                        messages.error(request, "Dirección no se encuentra dentro del perimetro de Medellín o comuna no registrada")
                        return render(request,'actualizar_parqueadero.html', {'unsoloparqueadero':unsoloparqueadero, "imgdata": imagen_park})
                insertar=connection.cursor()
                insertar.callproc("actualizarparqueadero", [parqueadero.nombre_park,parqueadero.direccion,parqueadero.tel_park,parqueadero.imagen_park,parqueadero.precio_mes,parqueadero.precio_dia,parqueadero.precio_hora,request.user.id,parqueadero.latitud,parqueadero.longitud,comuna.id,unsoloparqueadero.id])
                insertar.close()
                messages.success(request, "El parqueadero: " + parqueadero.nombre_park + " se guardó con exito")
                return redirect('buscar.html' + "?comuna=" + str(comuna.id))
            else:
                messages.error(request, "Por favor complete todos los campos")
                return render(request,'actualizar_parqueadero.html', {'unsoloparqueadero':unsoloparqueadero, "imgdata": imagen_park})
        else:
            return render(request,'actualizar_parqueadero.html', {'unsoloparqueadero':unsoloparqueadero, "imgdata": imagen_park})
    else:
        redirect('login')

#endregion

#regionreserva

def reservaparqueadero(request):
    id_parqueadero = int(request.GET.get('id'))
    if request.method=="POST":
         if request.POST.get('tipo_reserva') and request.POST.get('placa_veh') and request.POST.get('cantidad_reserva'):
            reservas=Reserva()
            reservas.tipo_reserva=request.POST.get('tipo_reserva')
            reservas.placa_veh=request.POST.get('placa_veh')
            reservas.cantidad_reserva=request.POST.get('cantidad_reserva')
            #reservas.save()
            insertar=connection.cursor()
            insertar.callproc("reservarparqueadero", [reservas.tipo_reserva,reservas.placa_veh,reservas.cantidad_reserva,request.user.id,id_parqueadero])
            insertar.close()
            messages.success(request, "Has hecho la reserva con exito")
            return redirect('../misreservas.html')
    
    else:
        return render(request,'reserva.html')
    
def terminarreserva(request):
    id_reserva=int(request.GET.get('id'))
    reserva = Reserva.objects.get(id=id_reserva)
    reserva.id_estado_fk_id=4
    reserva.save()

    return redirect('../misreservas.html')

#regioncalificacion
def calificacion(request):
    if request.method=="POST":
         if request.POST.get('estrellas') and request.POST.get('comentarios'):
            calificacion=Calificacion()
            calificacion.estrellas=request.POST.get('estrellas')
            calificacion.comentarios=request.POST.get('comentarios')
            #calificacion.save()
            insertar=connection.cursor()
            insertar.callproc("insertarcalificacion", [calificacion.estrellas,calificacion.comentarios,request.user.id])
            insertar.close()
            messages.success(request, "Has hecho la calificacion")
            return render(request,'calificacion.html')
    
    else: 
        return render(request,'calificacion.html')