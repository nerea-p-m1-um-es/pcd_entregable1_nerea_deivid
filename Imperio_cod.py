from enum import Enum

# --- DEFINICIÓN DE EXCEPCIONES ---
class PermisoDenegadoError(Exception): # Control de acceso basado en roles de usuario
    pass

class StockInsuficienteError(Exception): # Validación de integridad en la cantidad de inventario
    pass

class RepuestoNoEncontradoError(Exception): # Excepción para búsquedas fallidas en colecciones
    pass

class ValorInvalidoError(Exception): # Validación de tipos de datos
    pass

# --- ENUMERACIONES ---
class Rol_usuario(Enum): # Definición de privilegios según el perfil laboral
    COMANDANTE = 1
    OPERARIO = 2

class Ubicacion(Enum): # Constantes de localización geográfica para la logística
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3

class Clase_nave(Enum): # Clasificación de naves 
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

# --- Clases ---
class Sistema_miimperio: # Clase que representa el Sistema MIIMPERIO
    def __init__(self): 
        # Inicialización de las estructuras de datos globales del sistema
        # Crea listas vacías para almacenar naves, almacenes y usuarios registrados.
        self.naves_imperiales = [] 
        self.almacenes_imperiales = [] 
        self.usuarios_registrados = [] 

    # Métodos para el registro de objetos en el sistema

    def registrar_usuario(self, usuario): # Agrega un objeto de tipo Usuario a la lista del sistema.
        self.usuarios_registrados.append(usuario)
        print(f"Usuario '{usuario.nombre}' registrado con éxito.")

    def registrar_almacen(self, almacen): # Agrega un objeto de tipo Almacen a la lista del sistema
        self.almacenes_imperiales.append(almacen)
        print(f"Instalación '{almacen.nombre}' añadida a la red imperial.")

    def registrar_nave(self, nave): # Agrega un objeto de tipo Nave a la lista del sistema
        self.naves_imperiales.append(nave)
        print(f"Nave '{nave.nombre}' incorporada a la flota estelar.")

    def __str__(self): # Representación del estado actual del sistema
        # Devuelve una cadena de texto (string) con el resumen del estado actual del sistema (totales y nombres de naves, almacenes y usuarios)

        info_naves = ", ".join([f"'{nave.nombre}' (ID: {nave.id_combate})" for nave in self.naves_imperiales])
        if not info_naves: info_naves = "Ninguna"

        info_almacenes = ", ".join([almacen.nombre for almacen in self.almacenes_imperiales])
        if not info_almacenes: info_almacenes = "Ninguno"

        info_usuarios = ", ".join([usuario.nombre for usuario in self.usuarios_registrados])
        if not info_usuarios: info_usuarios = "Ninguno"

        return (f"SISTEMA IMPERIAL\n"
                f" -> Naves ({len(self.naves_imperiales)}): {info_naves}\n"
                f" -> Almacenes ({len(self.almacenes_imperiales)}): {info_almacenes}\n"
                f" -> Usuarios ({len(self.usuarios_registrados)}): {info_usuarios}")


class Repuesto: 
    def __init__(self, nombre, proveedor, cantidad, precio): # Crea un objeto del tipo Repuesto.
        # Validación de tipos para asegurar la consistencia numérica
        try:
            cantidad_int = int(cantidad)
            precio_float = float(precio)
        except (ValueError, TypeError):
            raise ValorInvalidoError(
                f"Error al crear '{nombre}': La cantidad debe ser un número entero y el precio un número."
            )

        # Restricción lógica: las magnitudes físicas no pueden ser negativas
        if cantidad_int < 0 or precio_float < 0:
            raise ValorInvalidoError(
                f"Error al crear '{nombre}': La cantidad y el precio no pueden ser negativos."
            )
        
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad_int # Atributo privado de la cantidad de un repuesto
        self.precio = precio_float      

    def get_cantidad(self): # Método para obtener el valor. del atributo privado cantidad
        return self.__cantidad
    
    def set_cantidad(self, nueva_cantidad): # Método para modificar el atributo de cantidad
        
        # Validación del tipo de entrada. Si la entrada no es tipo númerico, se activa la excepción 'ValorInvalidoError'
        try:
            nueva_cantidad_int = int(nueva_cantidad)
        except (ValueError, TypeError):
            raise ValorInvalidoError(
                f"Error al actualizar '{self.nombre}': La nueva cantidad debe ser un número entero."
            )


        # Validación del valor de entrada. Si el valor de entrada es negativo, se activa la excepción 'ValorInvalidoError'
        if nueva_cantidad_int < 0:
            raise ValorInvalidoError(
                f"El stock de '{self.nombre}' no puede actualizarse a un valor negativo."
            )
            
        self.__cantidad = nueva_cantidad_int

    def __str__(self): # Representación de la ficha técnica del repuesto
        return f"Repuesto: {self.nombre} \nProveedor: {self.proveedor} \nStock: {self.__cantidad} \nPrecio: {self.precio} €"



class Almacen: 
    def __init__(self, nombre, localizacion): # Crea un objeto del tipo Almacen
        self.nombre = nombre
        self.localizacion = localizacion
        self.lista_repuestos = [] # Colección de objetos tipo Repuesto

    def agregar_repuesto(self, repuesto): # Inserción de nuevos objetos en la colección
        self.lista_repuestos.append(repuesto)
        print(f"El repuesto '{repuesto.nombre}' se ha añadido al almacen '{self.nombre}'.")

    def buscar_repuesto(self, nombre_repuesto): # Método de búsqueda de un repuesto
        for rep in self.lista_repuestos: # Se itera sobre la lista de repuestos del Almacen
            if rep.nombre == nombre_repuesto:
                return rep
        
        # Gestión de error, en caso de que el objeto no exista en la colección se activa la excepción 'RepuestoNoEncontradoError'
        raise RepuestoNoEncontradoError(f"El repuesto '{nombre_repuesto}' no existe en el catálogo.")

    def actualizar_stock(self, nombre_repuesto, cantidad_a_restar): # Método para actualizar el inventario del Almacen
        
        # Validación del tipo de entrada. Si la entrada no es tipo númerico, se activa la excepción 'ValorInvalidoError'
        try:
            cantidad_int = int(cantidad_a_restar)
        except ValueError:
            raise ValorInvalidoError(f"La cantidad a restar debe ser un número entero.")

        # Validación del valor de entrada. Si el valor de entrada es negativo, se activa la excepción 'ValorInvalidoError'
        if cantidad_int < 0:
            raise ValorInvalidoError("No se permiten decrementos de magnitud negativa.")

        repuesto_encontrado = self.buscar_repuesto(nombre_repuesto)

        # Verificación de disponibilidad de stock suficiente. Si la cantidad disponible es inferior a la requerida, se activa la excepción 'StockInsuficienteError'
        if repuesto_encontrado.get_cantidad() < cantidad_int:
            raise StockInsuficienteError(
                f"Stock insuficiente. Disponibles: {repuesto_encontrado.get_cantidad()}, Solicitados: {cantidad_int}."
            )

        # Actualización del estado del objeto Repuesto
        new_cant = repuesto_encontrado.get_cantidad() - cantidad_int
        repuesto_encontrado.set_cantidad(new_cant)
        return True
    
    def __str__(self): # Representación del estado del almacén, su ubicación, y lista de las piezas que contiene actualmente
        nombres_repuestos = ", ".join([f"'{rep.nombre}'" for rep in self.lista_repuestos])
        
        if not nombres_repuestos: 
            nombres_repuestos = "Ninguno"

        return (f"Almacén: {self.nombre}\n"
                f" -> Ubicación: {self.localizacion.name}\n"
                f" -> Catálogo ({len(self.lista_repuestos)} repuestos): {nombres_repuestos}")



class Usuario: 
    def __init__(self, nombre, rol): #Crea un objeto del tipo Usuario
        self.nombre = nombre 
        self.rol = rol

    def verificar_stock_repuesto(self, nombre_repuesto, almacen, cantidad): # Función que comprueba de forma preventiva si hay stock de una pieza (solo lectura), y devuelve el objeto Repuesto si hay stock suficiente.
        # Restricción de acceso: Solo el rol COMANDANTE puede verificar el stock
        # En caso de no tener acceso, se activa la excepción 'PermisoDenegadoError'
        if self.rol != Rol_usuario.COMANDANTE:
            raise PermisoDenegadoError(f"Acción denegada: Privilegios insuficientes (Requiere COMANDANTE).")

        # Validación del tipo de entrada. Si la entrada no es tipo númerico, se activa la excepción 'ValorInvalidoError'
        try:
            cantidad_int = int(cantidad)
        except ValueError:
            raise ValorInvalidoError(f"La cantidad debe ser un número entero.")
            
        rep_disponible = almacen.buscar_repuesto(nombre_repuesto)

        # Verificación de disponibilidad de stock suficiente. Si la cantidad disponible es inferior a la requerida, se activa la excepción 'StockInsuficienteError'
        if rep_disponible.get_cantidad() < cantidad_int:
            raise StockInsuficienteError(f"Disponibilidad nula en '{almacen.nombre}' para '{nombre_repuesto}'.")
        
        return rep_disponible
    
    def adquirir_repuesto(self, nombre_repuesto, almacen, nave, cantidad): # Función de adquisición e instalación de un repuesto en la nave
        # Restricción de acceso: Solo el rol COMANDANTE puede adquirir un repuesto
        # En caso de no tener acceso, se activa la excepción 'PermisoDenegadoError'
        if self.rol != Rol_usuario.COMANDANTE:
            raise PermisoDenegadoError(f"Acción denegada: Autorización denegada para instalación de componentes.")

        self.verificar_stock_repuesto(nombre_repuesto, almacen, cantidad)
        almacen.actualizar_stock(nombre_repuesto, cantidad)
        nave._agregar_repuesto_nave(nombre_repuesto) 
        print(f"ÉXITO: Instalación completada en la unidad '{nave.nombre}'.")

    def mantener_catalogo(self, almacen, repuesto): # Función que agrega un nuevo tipo de repuesto en un Almacen
        # Tarea administrativa asignada exclusivamente al rol OPERARIO
        # En caso de no tener acceso, se activa la excepción 'PermisoDenegadoError'
        if self.rol != Rol_usuario.OPERARIO:
            raise PermisoDenegadoError(f"Acción denegada: Privilegios insuficientes (Requiere OPERARIO).")
        
        almacen.agregar_repuesto(repuesto)

    def actualizar_stock_almacen(self, almacen, nombre_repuesto, nueva_cantidad): # Función de actualización de la cantidad total de un repuesto en un Almacén
        # Tarea administrativa asignada exclusivamente al rol OPERARIO
        # En caso de no tener acceso, se activa la excepción 'PermisoDenegadoError'
        if self.rol != Rol_usuario.OPERARIO:
            raise PermisoDenegadoError(f"Acción denegada: Privilegios insuficientes (Requiere OPERARIO).")
        
        repuesto = almacen.buscar_repuesto(nombre_repuesto)
        repuesto.set_cantidad(nueva_cantidad)
        print(f"Inventario de '{nombre_repuesto}' actualizado por {self.nombre}.")

    def __str__(self): # Representación de la ficha de identificación del usuario
        return f"Usuario: {self.nombre} \nRol: {self.rol.name}"



class Unidad_combate:
    def __init__(self, id_combate, clave_cifrada): # Crea un objeto del tipo Unidad de Combate
        self.id_combate = id_combate 
        self.clave_cifrada = clave_cifrada 

    def __str__(self): # Representación de ficha de identificación de una unidad de combate
        return f"ID Combate: {self.id_combate} \nClave: {self.clave_cifrada} "

class Nave(Unidad_combate):
    def __init__(self, nombre, id_combate, clave_cifrada): # Crea un objeto del tipo Nave, una subclase de 'Unidad_Combate'
        super().__init__(id_combate, clave_cifrada) 
        self.nombre = nombre
        self.lista_repuestos = [] # Historial de componentes integrados

    def _agregar_repuesto_nave(self, repuesto): # Método para agregar un repuesto al historial de componentes de la nave
        self.lista_repuestos.append(repuesto)
        print(f"Componente '{repuesto}' integrado en el sistema de '{self.nombre}'")

    def __str__(self): # Representación técnica de la nave
        nombres_repuestos = ", ".join([f"'{rep}'" for rep in self.lista_repuestos])
        if not nombres_repuestos: nombres_repuestos = "Ninguno"

        return (f"Nave: {self.nombre}\n"
                f" -> {super().__str__()}\n"
                f" -> Repuestos instalados ({len(self.lista_repuestos)}): {nombres_repuestos}")

class EstacionEspacial(Nave): 
    def __init__(self, nombre, id_combate, clave_cifrada, tripulacion, pasaje, ubicacion): # Crea un objeto del tipo Estación Espacial, una subclase de 'Nave'
        super().__init__(nombre, id_combate, clave_cifrada)
        
        # Validación del tipo de entrada. Si la entrada no es tipo numérico, se activa la excepción 'ValorInvalidoError'
        try:
            tripulacion_int = int(tripulacion)
            pasaje_int = int(pasaje)
        except (ValueError, TypeError):
            raise ValorInvalidoError(f"Error en '{nombre}': La tripulación y el pasaje deben ser números enteros.")
            
        # Restricción lógica de los valores. Si la tripulación o el pasaje son negativos, se activa la excepción 'ValorInvalidoError'
        if tripulacion_int < 0 or pasaje_int < 0:
            raise ValorInvalidoError(f"Error en '{nombre}': La tripulación y el pasaje no pueden ser valores negativos.")

        self.tripulacion = tripulacion_int 
        self.pasaje = pasaje_int 
        self.ubicacion = ubicacion 

    def __str__(self): # Representación técnica de la Estación Espacial
        return f"Estación Espacial: {self.nombre} \nTripulación: {self.tripulacion} \nPasaje: {self.pasaje} \nUbicación: {self.ubicacion.name}"
        

class NaveEstelar(Nave):
    def __init__(self, nombre, id_combate, clave_cifrada, tripulacion, pasaje, clase):  # Crea un objeto del tipo Nave Estelar, una subclase de 'Nave'
        super().__init__(nombre, id_combate, clave_cifrada)
        
        # Validación del tipo de entrada. Si la entrada no es tipo numérico, se activa la excepción 'ValorInvalidoError'
        try:
            tripulacion_int = int(tripulacion)
            pasaje_int = int(pasaje)
        except (ValueError, TypeError):
            raise ValorInvalidoError(f"Error en '{nombre}': La tripulación y el pasaje deben ser números enteros.")
            
        # Restricción lógica de los valores. Si la tripulación o el pasaje son negativos, se activa la excepción 'ValorInvalidoError'
        if tripulacion_int < 0 or pasaje_int < 0:
            raise ValorInvalidoError(f"Error en '{nombre}': La tripulación y el pasaje no pueden ser valores negativos.")

        self.tripulacion = tripulacion_int
        self.pasaje = pasaje_int
        self.clase = clase 

    def __str__(self): # Representación técnica de la Nave Estelar
        return f"Nave Estelar: {self.nombre} \nClase: {self.clase.name}"


class CazaEstelar(Nave): 
    def __init__(self, nombre, id_combate, clave_cifrada, dotacion): # Crea un objeto del tipo Caza Estelar, una subclase de 'Nave'
        super().__init__(nombre, id_combate, clave_cifrada)
        
        # Validación del tipo de entrada. Si la entrada no es tipo numérico, se activa la excepción 'ValorInvalidoError'
        try:
            dotacion_int = int(dotacion)
        except (ValueError, TypeError):
            raise ValorInvalidoError(f"Error en '{nombre}': La dotación debe ser un número entero.")
            
        # Restricción lógica de los valores. Si la dotación es negativa, se activa la excepción 'ValorInvalidoError'
        if dotacion_int < 0:
            raise ValorInvalidoError(f"Error en '{nombre}': La dotación no puede ser negativa.")

        self.dotacion = dotacion_int 

    def __str__(self): # Representación técnica del Caza Estelar
        return f"Caza Estelar: {self.nombre} \nID: {self.id_combate} \nDotación: {self.dotacion}"




# ==================
# BLOQUE DE PRUEBAS 
# ==================


if __name__ == "__main__":

    print("INICIANDO PRUEBAS DEL SISTEMA IMPERIAL ")
    print("\n" * 2)

    try:
        # 1. Instanciamos el Sistema y usamos sus métodos de registro
        mi_imperio = Sistema_miimperio()
        
        print("--- REGISTRO DE PERSONAL ---")
        comandante = Usuario("Darth Vader", Rol_usuario.COMANDANTE)
        operario = Usuario("TK-421", Rol_usuario.OPERARIO)
        mi_imperio.registrar_usuario(comandante)
        mi_imperio.registrar_usuario(operario)

        print("\n--- REGISTRO DE INSTALACIONES ---")
        almacen_principal = Almacen("Almacén Central Endor", Ubicacion.ENDOR)
        mi_imperio.registrar_almacen(almacen_principal)
        
        motor_ionico = Repuesto("Motor Iónico", "Sienar Fleet Systems", 50, 1500.50)
        panel_solar = Repuesto("Panel Solar TIE", "Sienar Fleet Systems", 200, 300.0)
        
        print("\n--- GESTIÓN DE CATÁLOGO ---")
        operario.mantener_catalogo(almacen_principal, motor_ionico)
        operario.mantener_catalogo(almacen_principal, panel_solar)

        print("\n--- REGISTRO DE NAVES ---")
        caza_tie = CazaEstelar("TIE-Fighter Avanzado", "TIE-X1", "alfa-omega", 1)
        destructor = NaveEstelar("Ejecutor", "EXE-01", "cifrado-rojo", 250000, 38000, Clase_nave.EJECUTOR)
        estrella_muerte = EstacionEspacial("Estrella de la Muerte", "DS-1", "top-secret", 342953, 843342, Ubicacion.CUMULO_RAIMOS)
        
        mi_imperio.registrar_nave(caza_tie)
        mi_imperio.registrar_nave(destructor)
        mi_imperio.registrar_nave(estrella_muerte)

        print("\n--- OPERACIONES LOGÍSTICAS COMPLEJAS (Usuarios) ---")
        # El Comandante verifica y adquiere un repuesto
        print("El Comandante verifica stock...")
        comandante.verificar_stock_repuesto("Motor Iónico", almacen_principal, 2)
        comandante.adquirir_repuesto("Motor Iónico", almacen_principal, caza_tie, 2)
        
        # El Operario actualiza el stock
        print("\nEl Operario hace inventario...")
        operario.actualizar_stock_almacen(almacen_principal, "Panel Solar TIE", 210)

        print("\n" * 5) 


        # COMPROBACIÓN EXPLÍCITA DE MÉTODOS INTERNOS / AUXILIARES

        print("COMPROBACIÓN EXPLÍCITA DE MÉTODOS AUXILIARES")
        print("\n" * 2)

        # Prueba directa de buscar_repuesto() en Almacen
        print("1. Probando Almacen.buscar_repuesto():")
        repuesto_encontrado = almacen_principal.buscar_repuesto("Panel Solar TIE")
        print(f"   -> Búsqueda exitosa. Objeto devuelto: {repuesto_encontrado.nombre}")
        
        # Prueba directa de get_cantidad() en Repuesto
        print("\n2. Probando Repuesto.get_cantidad():")
        cantidad_actual = motor_ionico.get_cantidad()
        print(f"   -> El método get_cantidad() devuelve: {cantidad_actual} unidades de Motor Iónico.")
        
        # Prueba directa de set_cantidad() en Repuesto 
        print("\n3. Probando Repuesto.set_cantidad():")
        motor_ionico.set_cantidad(45)
        print(f"   -> El método set_cantidad(45) se ha ejecutado correctamente. Nuevo stock: {motor_ionico.get_cantidad()}")

        # Prueba directa de agregar_repuesto() puro en Almacen (saltándonos al operario)
        print("\n4. Probando Almacen.agregar_repuesto() directo:")
        pieza_extra = Repuesto("Tornillo Imperial", "SFS", 1000, 1.5)
        almacen_principal.agregar_repuesto(pieza_extra)

        print("\n" * 5) 

        # Impresión final para comprobar todos los __str__
        print("IMPRESIÓN DE OBJETOS (__str__) ")
        print("\n" + "-"*40 + "\n")        
        print(mi_imperio)
        print("\n" + "-"*40 + "\n")
        print(comandante)
        print("\n" + "-"*40 + "\n")
        print(operario)
        print("\n" + "-"*40 + "\n")
        print(motor_ionico)
        print("\n" + "-"*40 + "\n")
        print(panel_solar)
        print("\n" + "-"*40 + "\n")
        print(almacen_principal)
        print("\n" + "-"*40 + "\n")
        print(caza_tie)
        print("\n" + "-"*40 + "\n")
        print(destructor)
        print("\n" + "-"*40 + "\n")
        print(estrella_muerte)
        print("\n" + "-"*40 + "\n")
        print("\n" * 10)        


    except Exception as e:
        print(f"\n[ERROR DURANTE LAS PRUEBAS] {e}")




# ======================================
# BLOQUE DE PRUEBAS: GESTIÓN DE ERRORES
# ======================================

if __name__ == "__main__":

    print("INICIANDO SIMULADOR DE FALLOS DEL SISTEMA IMPERIAL ")
    print("\n" * 2)

    almacen = Almacen("Almacén de Pruebas", Ubicacion.ENDOR)
    vader = Usuario("Darth Vader", Rol_usuario.COMANDANTE)
    tk421 = Usuario("TK-421", Rol_usuario.OPERARIO)
    caza = CazaEstelar("TIE de Pruebas", "TIE-00", "clave", 1)
    
    motor_valido = Repuesto("Motor Iónico", "SFS", 10, 1500)
    tk421.mantener_catalogo(almacen, motor_valido)
    print("-" * 50 + "\n")



    # 1. PRUEBAS DE VALOR INVÁLIDO (ValorInvalidoError)

    print(">>> PRUEBA 1A: Crear repuesto con stock negativo")
    try:
        Repuesto("Láser Roto", "SFS", -5, 100)
    except ValorInvalidoError as e:
        print(f"ERROR CAPTURADO: {e}\n")

    print(">>> PRUEBA 1B: Crear nave con texto en lugar de números")
    try:
        CazaEstelar("TIE Kamikaze", "TIE-99", "clave", "cinco pilotos")
    except ValorInvalidoError as e:
        print(f"ERROR CAPTURADO: {e}\n")

    print(">>> PRUEBA 1C: Intentar adquirir una cantidad de texto")
    try:
        vader.adquirir_repuesto("Motor Iónico", almacen, caza, "veinte")
    except ValorInvalidoError as e:
        print(f"ERROR CAPTURADO: {e}\n")



    # 2. PRUEBAS DE PERMISOS (PermisoDenegadoError)

    print(">>> PRUEBA 2A: Operario intenta equipar una nave (Solo Comandantes)")
    try:
        tk421.adquirir_repuesto("Motor Iónico", almacen, caza, 1)
    except PermisoDenegadoError as e:
        print(f"ERROR CAPTURADO: {e}\n")

    print(">>> PRUEBA 2B: Comandante intenta manipular el catálogo (Solo Operarios)")
    try:
        nuevo_canon = Repuesto("Cañón Pesado", "Kuat", 5, 3000)
        vader.mantener_catalogo(almacen, nuevo_canon)
    except PermisoDenegadoError as e:
        print(f"ERROR CAPTURADO: {e}\n")

    print(">>> PRUEBA 2C: Comandante intenta hacer recuento de stock (Solo Operarios)")
    try:
        vader.actualizar_stock_almacen(almacen, "Motor Iónico", 50)
    except PermisoDenegadoError as e:
        print(f"ERROR CAPTURADO: {e}\n")



    # 3. PRUEBA DE EXISTENCIA DE UN REPUESTO EN ALMACEN (RepuestoNoEncontradoError)

    print(">>> PRUEBA 3: Buscar/Adquirir un repuesto que no existe en el almacén")
    try:
        vader.adquirir_repuesto("Condensador de Fluzo", almacen, caza, 1)
    except RepuestoNoEncontradoError as e:
        print(f"ERROR CAPTURADO: {e}\n")



    # 4. PRUEBAS DE INVENTARIO (StockInsuficienteError)

    print(">>> PRUEBA 4: Pedir más piezas de las que hay (Hay 10 motores)")
    try:
        vader.adquirir_repuesto("Motor Iónico", almacen, caza, 999)
    except StockInsuficienteError as e:
        print(f"ERROR CAPTURADO: {e}\n")



















