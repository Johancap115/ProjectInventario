import re
from flask import Flask, render_template, request
from werkzeug.utils import redirect

app = Flask(__name__)

lista_integrantes = [
    "Carlos Colmenares Arguelle", "Duber Mosquera Jimenez",
    "David Gutierrez Giraldo", "Daneli Rivera Pardo", "Johan Carreño Parada"
]

idNumber = 0
idProvider = 0
idProuct = 0
list_users = []
list_providers = []
list_prductos = []
userLog = ""
tipo_usuarios = ["Super-Administrador", "Administrador", "Usuario"]


@app.route('/home', methods=['GET', 'POST'])
def index():
    # Vista de Bienvenda para usuarios no logeados
    # si ya inicio sesión -> dependendiendo del tipo de usuario que incie sesión tendra acceso a las rutas y cruds
    if request.method == "GET":
        pass
    else:
        global userLog
        userLog = request.values["user"]

    return render_template('home.html',
                           integrantes=lista_integrantes,
                           username=userLog)


#Login
@app.route('/', methods=['GET', 'POST'])
def inicio():
    return render_template('index.html')


@app.route('/profile/<string:nombre>', methods=['GET'])
def perfil(nombre):
    return render_template('profile.html', name=nombre, username=userLog)


@app.route('/users', methods=['GET'])
def usuarios():
    return render_template('/user/users.html',
                           usuarios=list_users,
                           username=userLog)


@app.route('/users/adduser', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == "GET":
        return render_template('/user/addUser.html',
                               username=userLog,
                               typeUsers=tipo_usuarios)
    else:
        nombre = request.values["nombre"]
        apellido = request.values["apellido"]
        email = request.values["email"]
        telefono = request.values["telefono"]
        type_user = request.values["typeUser"]
        global idNumber
        idNumber += 1
        new_user = {
            'id': idNumber,
            'name': nombre,
            'lastname': apellido,
            'correo': email,
            'phone': telefono,
            'userType': type_user
        }

        list_users.append(new_user)
        return redirect("/users")


@app.route('/users/edit/<int:id_user>', methods=['GET', 'POST'])
def editar_usuario(id_user):
    if request.method == "GET":
        for i in list_users:
            if (i['id'] == id_user):
                return render_template('/user/editUser.html',
                                       username=userLog,
                                       usuario=i,
                                       typeUsers=tipo_usuarios)
            else:
                return redirect('/users')
    else:
        nombre = request.values["nombre"]
        apellido = request.values["apellido"]
        email = request.values["email"]
        telefono = request.values["telefono"]
        type_user = request.values["typeUser"]
        for i in list_users:
            if i['id'] == id_user:
                i['name'] = nombre
                i['lastname'] = apellido
                i['correo'] = email
                i['phone'] = telefono
                i['userType'] = type_user
        return redirect('/users')


@app.route('/users/delete/<int:id_user>', methods=['GET'])
def borrar_usuario(id_user):
    id_user = int(id_user)
    for i in list_users:
        if i['id'] == id_user:
            list_users.remove(i)
            return redirect('/users')


@app.route('/products', methods=['GET'])
def productos():
    return render_template('/products/productos.html',
                           productos=list_prductos,
                           username=userLog)


@app.route('/products/addproduct', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == "GET":
        return render_template('/products/addProducto.html',
                               username=userLog,
                               provider=list_providers)
    else:
        nombre = request.values["nombre"]
        description = request.values["desc"]
        proveedor = request.values["provider"]
        stock = request.values["stock"]
        stock_min = request.values["stock-min"]

        global idProuct
        idProuct += 1
        new_product = {
            'id': idProuct,
            'name': nombre,
            'desc': description,
            'provider': proveedor,
            'stock': stock,
            'stock_min': stock_min
        }

        list_prductos.append(new_product)
        return redirect('/products')


@app.route('/products/delete/<int:id_product>', methods=['GET'])
def borrar_prodcuto(id_product):
    for i in list_prductos:
        if (i['id'] == id_product):
            list_prductos.remove(i)
            return redirect('/products')


@app.route("/products/edit/<int:id_product>", methods=['GET', 'POST'])
def editar_producto(id_product):
    if request.method == "GET":
        for i in list_prductos:
            if (i['id'] == id_product):
                return render_template('/products/editProducto.html',
                                       username=userLog,
                                       producto=i,
                                       provider=list_providers)
            else:
                return redirect('/products')
    else:
        nombre = request.values["nombre"]
        description = request.values["desc"]
        proveedor = request.values["provider"]
        stock = request.values["stock"]
        stock_min = request.values["stock-min"]
        for i in list_prductos:
            if i['id'] == id_product:
                i['name'] = nombre
                i['desc'] = description
                i['provider'] = proveedor
                i['stock'] = stock
                i['stock_min'] = stock_min
        return redirect('/products')


@app.route('/providers', methods=['GET'])
def proveedores():
    return render_template('/provider/providers.html',
                           providers=list_providers,
                           username=userLog)


@app.route('/providers/edit/<int:id_provider>', methods=['GET', 'POST'])
def eitar_prveedor(id_provider):
    if request.method == "GET":
        for i in list_providers:
            if (i['id'] == id_provider):
                return render_template('/provider/editProvider.html',
                                       username=userLog,
                                       provider=i)
            else:
                return redirect('/providers')
    else:
        nombre = request.values["nombre"]
        direccion = request.values["direccion"]
        telefono = request.values["telefono"]
        email = request.values["email"]
        for i in list_providers:
            if (i['id'] == id_provider):
                i['name'] = nombre
                i['dir'] = direccion
                i['phone'] = telefono
                i['correo'] = email
        return redirect('/providers')


@app.route('/providers/addprovider', methods=['GET', 'POST'])
def agregar_proveedor():
    if request.method == "GET":
        return render_template('/provider/addProvider.html', username=userLog)
    else:
        nombre = request.values["nombre"]
        direccion = request.values["direccion"]
        telefono = request.values["telefono"]
        email = request.values["email"]

        global idProvider
        idProvider += 1
        new_provider = {
            'id': idProvider,
            'name': nombre,
            'dir': direccion,
            'phone': telefono,
            'correo': email
        }

        list_providers.append(new_provider)
        return redirect('/providers')


@app.route('/providers/delete/<int:id_provider>', methods=['GET'])
def borrar_proveedor(id_provider):
    for i in list_providers:
        if i['id'] == id_provider:
            list_providers.remove(i)
            return redirect('/providers')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
