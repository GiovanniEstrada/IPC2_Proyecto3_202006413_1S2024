from flask import Flask, request, jsonify, make_response
import xml.etree.ElementTree as ET
from xml.dom import minidom
app = Flask(__name__)

@app.route('/Reset', methods=['DELETE'])
def reset():
    with open('Config.xml', 'w') as file:
        file.write('')
    
    with open('Transac.xml', 'w') as file:
        file.write('')

    response = jsonify({'message': '¡Se ha borrado los datos!'})
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:8000')
    return response

@app.route('/GetConfig', methods=['GET'])
def getConfig():
    data = request.data
    with open('Config.xml', 'a') as file:
        file.write(data.decode('utf-8') + '\n')

@app.route('/GetTrx', methods=['GET'])
def getTrx():
    try:
        # Lee el contenido del archivo XML
        with open('Transac.xml', 'r') as xml_file:
            xml_content = xml_file.read()

        # Crea una respuesta con el contenido XML
        response = make_response(xml_content)
        response.headers['Content-Type'] = 'application/xml'
        return response
    except FileNotFoundError:
        return "Error: El archivo Transac.xml no se encontró"

@app.route('/SaveConfig', methods=['POST'])
def saveConfig():
    data = request.data.decode('utf-8')

    newReg = ET.fromstring(data)
    listClient = []
    listBank = []
    newListClient = []
    newListBank = []

    for cli in newReg.findall('.//cliente'):
        # print(cli.find('NIT').text)
        # print(cli.find('nombre').text)
        client = []
        client.append(cli.find('NIT').text)
        client.append(cli.find('nombre').text)
        newListClient.append(client)

    for bnk in newReg.findall('.//banco'):
        # print(bnk.find('codigo').text)
        # print(bnk.find('nombre').text)
        banco = []
        banco.append(bnk.find('codigo').text)
        banco.append(bnk.find('nombre').text)
        newListBank.append(banco)
    try:
        info = minidom.parse('Config.xml')
        xmlClient = info.getElementsByTagName('cliente')
        xmlBank = info.getElementsByTagName('banco')
    except Exception as e:
        xmlClient = []
        xmlBank = []
    # newClient = 0
    # updClient = 0

    # root = ET.Element('respuesta')
    # clients = ET.SubElement(root, 'clientes')
    # createdCli = ET.SubElement(clients, 'creados')

    for cli in xmlClient:
        client = []
        # print(cli.getElementsByTagName('NIT')[0].firstChild.data)
        # print(cli.getElementsByTagName('nombre')[0].firstChild.data)
        client.append(cli.getElementsByTagName('NIT')[0].firstChild.data)
        client.append(cli.getElementsByTagName('nombre')[0].firstChild.data)

        listClient.append(client)

    for bnk in xmlBank:
        bank = []
        # print(bnk.getElementsByTagName('codigo')[0].firstChild.data)
        # print(bnk.getElementsByTagName('nombre')[0].firstChild.data)
        bank.append(bnk.getElementsByTagName('codigo')[0].firstChild.data)
        bank.append(bnk.getElementsByTagName('nombre')[0].firstChild.data)
        listBank.append(bank)
    
    # SE VALIDA HACE LA INSERSIÓN O ACTUALIZACION
    newClient = 0
    updClient = 0
    for i in newListClient:
        flgTrue = True
        for j in listClient:
            if i[0] == j[0]:
                updClient += 1
                j[1] = i[1]
                flgTrue = False
        if flgTrue:
            newClient += 1
            listClient.append(i)
    
    newBank = 0
    updBank = 0
    for i in newListBank:
        flgTrue = True
        for j in listBank:
            if i[0] == j[0]:
                updBank += 1
                j[1] = i[1]
                flgTrue = False
        if flgTrue:
            newBank += 1
            listBank.append(i)

    #SE ALMACENA LA CONFIGURACION
    doc = minidom.Document()
    root = doc.createElement('config')
    doc.appendChild(root)
    clientes = doc.createElement('clientes')
    root.appendChild(clientes)
    for cli in listClient:
        cliente = doc.createElement('cliente')
        clientes.appendChild(cliente)
        nit = doc.createElement('NIT')
        nit.appendChild(doc.createTextNode(cli[0]))
        cliente.appendChild(nit)
        nombre = doc.createElement('nombre')
        nombre.appendChild(doc.createTextNode(cli[1]))
        cliente.appendChild(nombre)

    bancos = doc.createElement('bancos')
    root.appendChild(bancos)
    for bnk in listBank:
        banco = doc.createElement('banco')
        bancos.appendChild(banco)
        codigo = doc.createElement('codigo')
        codigo.appendChild(doc.createTextNode(bnk[0]))
        banco.appendChild(codigo)
        nombre = doc.createElement('nombre')
        nombre.appendChild(doc.createTextNode(bnk[1]))
        banco.appendChild(nombre)

    with open('Config.xml', 'w') as f:
        f.write(doc.toprettyxml(indent='\t'))

    
    resp = minidom.Document()
    root = resp.createElement('respuesta')
    resp.appendChild(root)
    clientes = resp.createElement('clientes')
    root.appendChild(clientes)
    creados = resp.createElement('creados')
    creados.appendChild(resp.createTextNode(str(newClient)))
    clientes.appendChild(creados)
    actualizado = resp.createElement('actualizados')
    actualizado.appendChild(resp.createTextNode(str(updClient)))
    clientes.appendChild(actualizado)

    bancos = resp.createElement('bancos')
    root.appendChild(bancos)
    creadoBnk = resp.createElement('creados')
    creadoBnk.appendChild(resp.createTextNode(str(newBank)))
    bancos.appendChild(creadoBnk)
    actualizaBnk = resp.createElement('actualizados')
    actualizaBnk.appendChild(resp.createTextNode(str(updBank)))
    bancos.appendChild(actualizaBnk)

    with open('configResponse.xml', 'w') as f:
        f.write(resp.toprettyxml(indent='\t'))

    return '¡Configuración guardada!'

@app.route('/SaveTrx', methods=['POST'])
def saveTrx():
    data = request.data.decode('utf-8')

    newReg = ET.fromstring(data)
    listBill = []
    listBuy = []
    newListBill = []
    newListBuy = []

    for bll in newReg.findall('.//factura'):
        # print(bll.find('NIT').text)
        # print(bll.find('nombre').text)
        bill = []
        bill.append(bll.find('numeroFactura').text)
        bill.append(bll.find('NITcliente').text)
        bill.append(bll.find('fecha').text)
        bill.append(bll.find('valor').text)
        newListBill.append(bill)

    for by in newReg.findall('.//pago'):
        # print(by.find('codigo').text)
        # print(by.find('nombre').text)
        buy = []
        buy.append(by.find('codigoBanco').text)
        buy.append(by.find('fecha').text)
        buy.append(by.find('NITcliente').text)
        buy.append(by.find('valor').text)
        newListBuy.append(buy)
    try:
        info = minidom.parse('transac.xml')
        xmlBill = info.getElementsByTagName('factura')
        xmlBuy = info.getElementsByTagName('pago')
    except Exception as e:
        xmlBill = []
        xmlBuy = []
    # newClient = 0
    # updClient = 0

    # root = ET.Element('respuesta')
    # clients = ET.SubElement(root, 'clientes')
    # createdCli = ET.SubElement(clients, 'creados')

    for bll in xmlBill:
        bill = []
        # print(bll.getElementsByTagName('NIT')[0].firstChild.data)
        # print(bll.getElementsByTagName('nombre')[0].firstChild.data)
        bill.append(bll.getElementsByTagName('numeroFactura')[0].firstChild.data)
        bill.append(bll.getElementsByTagName('NITcliente')[0].firstChild.data)
        bill.append(bll.getElementsByTagName('fecha')[0].firstChild.data)
        bill.append(bll.getElementsByTagName('valor')[0].firstChild.data)

        listBill.append(bill)

    for by in xmlBuy:
        buy = []
        # print(by.getElementsByTagName('codigo')[0].firstChild.data)
        # print(by.getElementsByTagName('nombre')[0].firstChild.data)
        buy.append(by.getElementsByTagName('codigoBanco')[0].firstChild.data)
        buy.append(by.getElementsByTagName('fecha')[0].firstChild.data)
        buy.append(by.getElementsByTagName('NITcliente')[0].firstChild.data)
        buy.append(by.getElementsByTagName('valor')[0].firstChild.data)
        listBuy.append(buy)
    
    # SE VALIDA HACE LA INSERSIÓN O ACTUALIZACION
    newBill = 0
    updBill = 0
    for i in newListBill:
        flgTrue = True
        for j in listBill:
            if i[0] == j[0]:
                updBill += 1
                flgTrue = False
        if flgTrue:
            newBill += 1
        listBill.append(i)
    
    newBuy = 0
    updBuy = 0
    for i in newListBuy:
        flgTrue = True
        for j in listBuy:
            if i[0] == j[0]:
                updBuy += 1
                flgTrue = False
        if flgTrue:
            newBuy += 1
        listBuy.append(i)

    #SE ALMACENA LA CONFIGURACION
    doc = minidom.Document()
    root = doc.createElement('transacciones')
    doc.appendChild(root)
    facturas = doc.createElement('facturas')
    root.appendChild(facturas)
    for cli in listBill:
        factura = doc.createElement('factura')
        facturas.appendChild(factura)
        num = doc.createElement('numeroFactura')
        num.appendChild(doc.createTextNode(cli[0]))
        factura.appendChild(num)
        nit = doc.createElement('NITcliente')
        nit.appendChild(doc.createTextNode(cli[1]))
        factura.appendChild(nit)
        fecha = doc.createElement('fecha')
        fecha.appendChild(doc.createTextNode(cli[2]))
        factura.appendChild(fecha)
        valor = doc.createElement('valor')
        valor.appendChild(doc.createTextNode(cli[3]))
        factura.appendChild(valor)

    pagos = doc.createElement('pagos')
    root.appendChild(pagos)
    for by in listBuy:
        pago = doc.createElement('pago')
        pagos.appendChild(pago)
        codigo = doc.createElement('codigoBanco')
        codigo.appendChild(doc.createTextNode(by[0]))
        pago.appendChild(codigo)
        fecha = doc.createElement('fecha')
        fecha.appendChild(doc.createTextNode(by[1]))
        pago.appendChild(fecha)
        nit = doc.createElement('NITcliente')
        nit.appendChild(doc.createTextNode(by[2]))
        pago.appendChild(nit)
        valor = doc.createElement('valor')
        valor.appendChild(doc.createTextNode(by[3]))
        pago.appendChild(valor)

    with open('transac.xml', 'w') as f:
        f.write(doc.toprettyxml(indent='\t'))

    
    # resp = minidom.Document()
    # root = resp.createElement('transacciones')
    # resp.appendChild(root)
    # clientes = resp.createElement('clientes')
    # root.appendChild(clientes)
    # creados = resp.createElement('creados')
    # creados.appendChild(resp.createTextNode(str(newBill)))
    # clientes.appendChild(creados)
    # actualizado = resp.createElement('actualizados')
    # actualizado.appendChild(resp.createTextNode(str(updBill)))
    # clientes.appendChild(actualizado)

    # bancos = resp.createElement('bancos')
    # root.appendChild(bancos)
    # creadoBnk = resp.createElement('creados')
    # creadoBnk.appendChild(resp.createTextNode(str(newBuy)))
    # bancos.appendChild(creadoBnk)
    # actualizaBnk = resp.createElement('actualizados')
    # actualizaBnk.appendChild(resp.createTextNode(str(updBuy)))
    # bancos.appendChild(actualizaBnk)

    # with open('configResponse.xml', 'w') as f:
    #     f.write(resp.toprettyxml(indent='\t'))

    return '¡Configuración guardada!'

if __name__=='__main__':
    app.run(debug=True, port=1000)