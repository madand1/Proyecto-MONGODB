import pymongo

# Parámetros de conexión a MongoDB
MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIEMPO_FUERA = 1000
MONGO_URI = "mongodb://" + MONGO_HOST + ":" + MONGO_PUERTO + "/"
NOMBRE_BASE_DE_DATOS = "Proyecto_mongo"  # Nombre de tu base de datos
NOMBRE_COLECCION = "vehiculos"  # Nombre de tu colección

# Conexión a MongoDB
try:
    cliente = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
    db = cliente[NOMBRE_BASE_DE_DATOS]
    coleccion = db[NOMBRE_COLECCION]
    print("Conexión a la colección fue exitosa.")
except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
    print("Tiempo exedido:", errorTiempo)
except pymongo.errors.ConnectionFailure as errorConnection:
    print("Fallo al conectarse a MongoDB:", errorConnection)

#  mostrar el menú
def mostrar_menu():
    print("\n--- MENÚ ---")
    print("1. Insertar documento")
    print("2. Eliminar por modelo")
    print("3. Modificar potencia")
    print("4. Mostrarme todos los modelos de una marca")
    print("5. Eleguir color")
    print("6. Consultar marca y modelo entre fechas de fabricación")
    print("0. Salir")

#  insertar un documento
def insertar_documento():
    # Solicitar los datos al usuario
    id_ = input("Introduce el ID del vehículo: ")
    nombre = input("Introduce el nombre del propietario: ")
    apellido = input("Introduce el apellido del propietario: ")
    genero = input("Introduce el género del propietario: ")
    email = input("Introduce el email del fabricante: ")
    marca = input("Introduce la marca del vehículo: ")
    modelo = input("Introduce el modelo del vehículo: ")
    año = int(input("Introduce el año del vehículo: "))
    color = input("Introduce el color del vehículo (separado por comas si hay más de uno): ").split(",")
    disponibilidad = input("Introduce la disponibilidad del vehículo (True/False): ").lower() == "true"
    cv = int(input("Introduce los CV del vehículo: "))
    fecha = input("Introduce la fecha (YYYY-MM-DD): ")

    nuevo_documento = {
        "id": int(id_),
        "NombrePropietario": nombre,
        "ApellidoPropietario": apellido,
        "GeneroPropietario": genero,
        "Email_Fabricante": email,
        "Marca": marca,
        "Modelo": modelo,
        "Año": año,
        "Color": color,
        "Disponibilidad": disponibilidad,
        "CV": cv,
        "Fecha": fecha
    }
    coleccion.insert_one(nuevo_documento)
    print("Documento insertado con éxito.")

# Función para eliminar 
def eliminar_modelo():
    while True:
        modelo = input("Introduce el modelo del vehículo a eliminar: ")

        # Verificar si el modelo está en la base de datos
        if coleccion.count_documents({"Modelo": modelo}) > 0:
            # Realizar la eliminación de documentos por modelo
            resultado = coleccion.delete_many({"Modelo": modelo})
            # Mostrar el resultado de la eliminación
            print(f"Se han eliminado {resultado.deleted_count} documentos con el modelo '{modelo}' de la colección.")
            break
        else:
            respuesta = input(f"El modelo '{modelo}' no existe en la base de datos. ¿Deseas intentarlo de nuevo? (s/n): ")
            if respuesta.lower() != 's':
                break


# Función para modificar un documento
def modificar_potencia():
    while True:
        año = int(input("Introduce el año de los vehículos a actualizar: "))
        # Verificar si el año está en la base de datos
        if coleccion.count_documents({"Año": año}) > 0:
            potencia_nueva = int(input("Introduce la nueva potencia: "))
            # Realizar la actualización de la potencia de los vehículos
            nuevos_datos = {"$set": {"CV": potencia_nueva}}
            resultados = coleccion.update_many({"Año": año}, nuevos_datos)
            # Recopilar información de los vehículos actualizados
            vehiculos_actualizados = list(coleccion.find({"Año": año}))
            print(f"Se han modificado {resultados.modified_count} vehículos con éxito.")
            print("Información de los vehículos actualizados:")
            for vehiculo in vehiculos_actualizados:
                print(f"Marca: {vehiculo['Marca']}, Modelo: {vehiculo['Modelo']}")
            break
        else:
            print("Este año no está en su base de datos. Introduce un año que sí esté en su base de datos.")




# Función para realizar una consultasimple
def mostrar_modelos_por_marca():
    while True:
        marca_consulta = input("Introduce la marca del vehículo: ")

        # Realizar la consulta de modelos por marca
        resultados = list(coleccion.find({"Marca": marca_consulta}))

        if resultados:
            # Mostrar los modelos de la marca especificada
            print(f"Todos los modelos de la marca {marca_consulta}:")
            for resultado in resultados:
                print(f"Modelo: {resultado['Modelo']}, Año: {resultado['Año']}, Fecha: {resultado['Fecha']}, Color: {', '.join(resultado['Color'])}")
            break
        else:
            respuesta = input(f"No se encontraron vehículos de la marca '{marca_consulta}'. ¿Deseas intentarlo de nuevo? (s/n): ")
            if respuesta.lower() != 's':
                break




# Función para realizar una consulta con arrays
def consultar_vehiculos_por_color():
    while True:
        color = input("Introduce el color de los vehículos que deseas consultar: ")

        # Realizar la consulta de vehículos por color
        vehiculos = coleccion.find({"Color": color})

        # Verificar si se encontraron vehículos
        vehiculos_encontrados = list(vehiculos)
        if vehiculos_encontrados:
            # Mostrar las marcas y modelos de los vehículos con el color especificado
            print(f"Vehículos con el color '{color}':")
            for vehiculo in vehiculos_encontrados:
                print(f"Marca: {vehiculo['Marca']}, Modelo: {vehiculo['Modelo']}")
            break
        else:
            print(f"No se encontraron vehículos con el color '{color}'. Inténtalo de nuevo.\n")



# Función para realizar una consulta con documentos embebidos
def consultar_vehiculos_por_año_y_fechas():
    while True:
        año = int(input("Introduce el año de fabricación de los vehículos: "))
        fecha_inicio = input("Introduce la fecha de inicio (YYYY-MM-DD): ")
        fecha_fin = input("Introduce la fecha de fin (YYYY-MM-DD): ")

        # Realizar la consulta de vehículos por año y fechas
        vehiculos = coleccion.find({"Año": año, "Fecha": {"$gte": fecha_inicio, "$lte": fecha_fin}})

        # Verificar si se encontraron vehículos
        vehiculos_encontrados = list(vehiculos)
        if vehiculos_encontrados:
            # Mostrar la información de los vehículos encontrados
            print(f"Vehículos fabricados en el año {año} y registrados entre {fecha_inicio} y {fecha_fin}:")
            for vehiculo in vehiculos_encontrados:
                print(f"Marca: {vehiculo['Marca']}, Modelo: {vehiculo['Modelo']}, CV: {vehiculo['CV']}")
            break
        else:
            print("No se encontraron vehículos que cumplan con los criterios especificados. Inténtalo de nuevo.\n")



#Menu del programa 
while True:
    mostrar_menu()
    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        insertar_documento()
    elif opcion == "2":
        eliminar_modelo()
    elif opcion == "3":
        modificar_potencia()
    elif opcion == "4":
        mostrar_modelos_por_marca()
    elif opcion == "5":
        consultar_vehiculos_por_color()
    elif opcion == "6":
        consultar_vehiculos_por_año_y_fechas()
    elif opcion == "0":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Por favor, selecciona una opción válida.")
