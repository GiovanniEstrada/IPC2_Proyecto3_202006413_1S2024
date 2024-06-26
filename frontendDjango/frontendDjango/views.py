from django.shortcuts import render, HttpResponse
from xml.dom import minidom
from .clases.Cliente import Cliente
from .clases.EstadoCuenta import EstadoCuenta
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
    
    result = requests.get('http://localhost:1000/configResponse')
    resultadoConfig = result.text
    context = {"xml": xml_input, "resultadoConfig": resultadoConfig}
    return render(request, "setConfig.html", context)

def setTrx(request):
    global xml
    xml_input = request.GET.get("xml")
    if (xml_input is not "" and xml_input is not None):
        response = requests.post('http://localhost:1000/SaveTrx', data=xml_input)
        print(response)

    result = requests.get('http://localhost:1000/trxResponse')
    resultadoConfig = result.text

    context = {"xml": xml_input, "resultadoConfig": resultadoConfig}
    return render(request, "setTrx.html", context)

def peticiones(request):
    return render(request, "peticiones.html")

def getEstCta(request):
    global estado_datos
    nit = request.GET.get("nit")
    response = requests.get("http://localhost:1000/GetTrx")
    estado_datos = response.content
    if str(estado_datos) == "b''":
        return render(request, "getEstCta.html")
    root = ET.fromstring(estado_datos)

    if nit is None:
        facturas = []
        for factura in root.findall('.//factura'):
            facturas.append(EstadoCuenta(factura.find('fecha').text, 
                                        factura.find('valor').text, 
                                        factura.find('numeroFactura').text))
        
        pagos = []
        for pago in root.findall('.//pago'):
            nomBanco = requests.get("http://localhost:1000/getBankName", params={"id": pago.find('codigoBanco').text})
            pagos.append(EstadoCuenta(pago.find('fecha').text, 
                                        pago.find('valor').text,
                                        nomBanco.text))
    else:
        facturas = []
        for factura in root.findall('.//factura'):
            if int(nit) == int(factura.find('NITcliente').text):
                facturas.append(EstadoCuenta(factura.find('fecha').text, 
                                            factura.find('valor').text, 
                                            factura.find('numeroFactura').text))
        
        pagos = []
        for pago in root.findall('.//pago'):
            if int(nit) == int(pago.find('NITcliente').text):
                nomBanco = requests.get("http://localhost:1000/getBankName", params={"id": pago.find('codigoBanco').text})
                pagos.append(EstadoCuenta(pago.find('fecha').text, 
                                            pago.find('valor').text,
                                            nomBanco.content))

    context = {"facturas": facturas, "pagos": pagos}
    return render(request, "getEstCta.html", context)

def getReport(request):
    return render(request, "getReport.html")
