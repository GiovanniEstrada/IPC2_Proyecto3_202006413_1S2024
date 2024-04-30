from django.shortcuts import render, HttpResponse
from xml.dom import minidom
from .clases.Cliente import Cliente
import requests
from django.shortcuts import render
import xml.etree.ElementTree as ET


xml_input = ""
estado_datos = "Datos Sin Limpiar"

def index(request):
    
    return render(request, "base.html")


def response(request):
    response = requests.get("http://localhost:5000/clientes/get")
    print(response.text)
    context = {"xml": response.text}
    return render(request, "response.html", context)


def clientes(request):
    response = requests.get("http://localhost:5000/clientes/get")

    xml = minidom.parseString(response.text)
    clientes = xml.documentElement
    clientes_lista = clientes.getElementsByTagName("item")

    lista_clientes = []
    for cliente in clientes_lista:
        nombre = cliente.getElementsByTagName("nombre")[0].childNodes[0].data.strip()
        apellido = cliente.getElementsByTagName("apellido")[0].childNodes[0].data.strip()
        edad = cliente.getElementsByTagName("edad")[0].childNodes[0].data.strip()
        lista_clientes.append(Cliente(nombre, apellido, edad))

    context = {"clientes": lista_clientes}
    return render(request, "clientes.html", context)

def limpiar(request):
    global estado_datos
    response = requests.get("http://localhost:5000/clientes/limpiar")
    estado_datos = response.text
    context = {"response": estado_datos}
    return render(request, "limpiar.html", context)

def delete(request):
    response = requests.delete("http://localhost:1000/Reset")
    context = {"response": "¡Se han limpiado los registros!"}
    return render(request, "base.html", context)

def setConfig(request):
    global xml
    xml_input = request.GET.get("xml")
    if (xml_input is not "" and xml_input is not None):
        response = requests.post('http://localhost:1000/SaveConfig', data=xml_input)
        print(response)
    context = {"xml": xml_input}
    return render(request, "setConfig.html")

def setTrx(request):
    global xml
    xml_input = request.GET.get("xml")
    if (xml_input is not "" and xml_input is not None):
        response = requests.post('http://localhost:1000/SaveTrx', data=xml_input)
        print(response)
    context = {"xml": xml_input}
    return render(request, "setTrx.html")

def peticiones(request):
    return render(request, "peticiones.html")

def getEstCta(request):
    global estado_datos
    response = requests.get("http://localhost:1000/GetTrx")
    estado_datos = response.content
    root = ET.fromstring(estado_datos)
    facturasR = []
    for factura in root.findall('.//factura'):
        r = []
        r.append(factura.find('fecha').text)
        r.append(factura.find('numeroFactura').text)
        r.append(factura.find('NITcliente').text)
        r.append(factura.find('valor').text)
        facturasR.append(r)
    context = {"facturas": facturasR}
    return render(request, "getEstCta.html", context)