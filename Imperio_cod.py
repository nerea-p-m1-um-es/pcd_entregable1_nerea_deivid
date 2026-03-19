from enum import Enum

class PermisoDenegadoError(Exception):
    pass

class StockInsuficienteError(Exception):
    pass

class RepuestoNoEncontradoError(Exception):
    pass

class ValorInvalidoError(Exception):
    pass

class Rol_usuario(Enum):
    COMANDANTE = 1
    OPERARIO = 2

class Ubicacion(Enum):
    ENDOR = 1
    CUMULO_RAIMOS = 2
    NEBULOSA_KALIIDA = 3

class Clase_nave(Enum):
    EJECUTOR = 1
    ECLIPSE = 2
    SOBERANO = 3

class Sistema_miimperio:
    def __init__(self):
        self.naves_imperiales = []
        self.almacenes_imperiales = []
        self.usuarios_registrados = []

    def registrar_usuario(self, usuario):
        self.usuarios_registrados.append(usuario)
        print(f"Usuario '{usuario.nombre}' registrado con éxito.")

    def registrar_almacen(self, almacen):
        self.almacenes_imperiales.append(almacen)
        print(f"Instalación '{almacen.nombre}' añadida a la red imperial.")

    def registrar_nave(self, nave):
        self.naves_imperiales.append(nave)
        print(f"Nave '{nave.nombre}' incorporada a la flota estelar.")

    def __str__(self):
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
    def __init__(self, nombre, proveedor, cantidad, precio):
        try:
            cantidad_int = int(cantidad)
            precio_float = float(precio)
        except (ValueError, TypeError):
            raise ValorInvalidoError(
                f"Error al crear '{nombre}': La cantidad debe ser un número entero y el precio un número (entero o decimal)."
            )

        if cantidad_int < 0 or precio_float < 0:
            raise ValorInvalidoError(
                f"Error al crear '{nombre}': La cantidad y el precio no pueden ser negativos."
            )
        
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad_int  
        self.precio = precio_float      

    def get_cantidad(self):
        return self.__cantidad
    
    def set_cantidad(self, nueva_cantidad):
        try:
            nueva_cantidad_int = int(nueva_cantidad)
        except (ValueError, TypeError):
            raise ValorInvalidoError(
                f"Error al actualizar '{self.nombre}': La nueva cantidad debe ser un número entero."
            )

        if nueva_cantidad_int < 0:
            raise ValorInvalidoError(
                f"El stock de '{self.nombre}' no puede actualizarse a un valor negativo ({nueva_cantidad_int})."
            )
            
        self.__cantidad = nueva_cantidad_int

    def __str__(self):
        return f"Repuesto: {self.nombre} \nProveedor: {self.proveedor} \nStock: {self.__cantidad} \nPrecio: {self.precio} €"

class Almacen:
    def __init__(self, nombre, localizacion):
        self.nombre = nombre
        self.localizacion = localizacion
        self.lista_repuestos = []

    def agregar_repuesto(self, repuesto):
        self.lista_repuestos.append(repuesto)
        print(f"El repuesto '{repuesto.nombre}' se ha añadido al almacen '{self.nombre}'.")

    def buscar_repuesto(self, nombre_repuesto):
        for rep in self.lista_repuestos:
            if rep.nombre == nombre_repuesto:
                return rep
        
        raise RepuestoNoEncontradoError(f"El repuesto '{nombre_repuesto}' no existe en el catálogo del almacén '{self.nombre}'.")

    def actualizar_stock(self, nombre_repuesto, cantidad_a_restar):
        try:
            cantidad_int = int(cantidad_a_restar)
        except ValueError:
            raise ValorInvalidoError(f"La cantidad a restar de '{nombre_repuesto}' debe ser un número entero.")
            
        if cantidad_int < 0:
            raise ValorInvalidoError("No puedes restar una cantidad negativa.")

        repuesto_encontrado = self.buscar_repuesto(nombre_repuesto)

        if repuesto_encontrado.get_cantidad() < cantidad_int:
            raise StockInsuficienteError(
                f"No hay stock suficiente de '{nombre_repuesto}'. "
                f"Disponibles: {repuesto_encontrado.get_cantidad()}, Solicitados: {cantidad_int}."
            )

        new_cant = repuesto_encontrado.get_cantidad() - cantidad_int
        repuesto_encontrado.set_cantidad(new_cant)
        return True
    
    def __str__(self):
        nombres_repuestos = ", ".join([f"'{rep.nombre}'" for rep in self.lista_repuestos])
        
        if not nombres_repuestos: 
            nombres_repuestos = "Ninguno"

        return (f"Almacén: {self.nombre}\n"
                f" -> Ubicación: {self.localizacion.name}\n"
                f" -> Catálogo ({len(self.lista_repuestos)} repuestos): {nombres_repuestos}")

class Usuario:
    def __init__(self, nombre, rol):
        self.nombre = nombre 
        self.rol = rol

    def verificar_stock_repuesto(self, nombre_repuesto, almacen, cantidad):
        if self.rol != Rol_usuario.COMANDANTE:
            raise PermisoDenegadoError(f"Acción denegada para {self.nombre}: Solo los Comandantes pueden verificar stock.")

        try:
            cantidad_int = int(cantidad)
        except ValueError:
            raise ValorInvalidoError(f"La cantidad a verificar debe ser un número entero.")
            
        if cantidad_int < 0:
            raise ValorInvalidoError(f"La cantidad a verificar no puede ser negativa.")

        rep_disponible = almacen.buscar_repuesto(nombre_repuesto)

        if rep_disponible.get_cantidad() < cantidad_int:
            raise StockInsuficienteError(f"El almacén '{almacen.nombre}' no tiene {cantidad_int} unidades de '{nombre_repuesto}'.")
        
        return rep_disponible
    
    def adquirir_repuesto(self, nombre_repuesto, almacen, nave, cantidad):
        if self.rol != Rol_usuario.COMANDANTE:
            raise PermisoDenegadoError(f"Acción denegada para {self.nombre}: Solo los Comandantes pueden instalar repuestos.")

        try:
            cantidad_int = int(cantidad)
        except ValueError:
            raise ValorInvalidoError(f"La cantidad a adquirir debe ser un número entero.")

        self.verificar_stock_repuesto(nombre_repuesto, almacen, cantidad_int)
        
        almacen.actualizar_stock(nombre_repuesto, cantidad_int)
        nave._agregar_repuesto_nave(nombre_repuesto)
        print(f"ÉXITO: Se instalaron {cantidad_int} unidades de '{nombre_repuesto}' en la nave '{nave.nombre}'.")

    def mantener_catalogo(self, almacen, repuesto):
        if self.rol != Rol_usuario.OPERARIO:
            raise PermisoDenegadoError(f"Acción denegada para {self.nombre}: Solo los Operarios pueden mantener el catálogo.")
        
        almacen.agregar_repuesto(repuesto)
        print(f"Operario {self.nombre} ha añadido el nuevo tipo de pieza '{repuesto.nombre}' al catálogo de '{almacen.nombre}'.")

    def actualizar_stock_almacen(self, almacen, nombre_repuesto, nueva_cantidad):
        if self.rol != Rol_usuario.OPERARIO:
            raise PermisoDenegadoError(f"Acción denegada para {self.nombre}: Solo los Operarios pueden hacer recuentos.")
        
        try:
            nueva_cantidad_int = int(nueva_cantidad)
        except ValueError:
            raise ValorInvalidoError("La nueva cantidad del inventario debe ser un número entero.")

        repuesto = almacen.buscar_repuesto(nombre_repuesto)
        repuesto.set_cantidad(nueva_cantidad_int)
        print(f"Stock de '{nombre_repuesto}' actualizado a {nueva_cantidad_int} por {self.nombre}.")

    def __str__(self):
        return f"Usuario: {self.nombre} \nRol: {self.rol.name}"

class Unidad_combate:
    def __init__(self, id_combate, clave_cifrada):
        self.id_combate = id_combate
        self.clave_cifrada = clave_cifrada

    def __str__(self):
        return f"ID Combate: {self.id_combate} \nClave: {self.clave_cifrada} "

class Nave(Unidad_combate):
    def __init__(self, nombre, id_combate, clave_cifrada):
        super().__init__(id_combate, clave_cifrada)
        self.nombre = nombre
        self.lista_repuestos = []

    def _agregar_repuesto_nave(self, repuesto):
        self.lista_repuestos.append(repuesto)
        print(f"El repuesto '{repuesto}' se ha añadido a la lista de repuestos de la nave '{self.nombre}'")

    def __str__(self):
        nombres_repuestos = ", ".join([f"'{rep}'" for rep in self.lista_repuestos])
        
        if not nombres_repuestos:
            nombres_repuestos = "Ninguno"

        return (f"Nave: {self.nombre}\n"
                f" -> {super().__str__()}\n"
                f" -> Repuestos instalados ({len(self.lista_repuestos)}): {nombres_repuestos}")

class EstacionEspacial(Nave):
    def __init__(self, nombre, id_combate, clave_cifrada, tripulacion, pasaje, ubicacion):
        super().__init__(nombre, id_combate, clave_cifrada)
        
        try:
            self.tripulacion = int(tripulacion)
            self.pasaje = int(pasaje)
        except ValueError:
            raise ValorInvalidoError(f"Error en '{nombre}': La tripulación y el pasaje deben ser números enteros.")
            
        if self.tripulacion < 0 or self.pasaje < 0:
            raise ValorInvalidoError(f"Error en '{nombre}': La tripulación y el pasaje no pueden ser negativos.")
            
        self.ubicacion = ubicacion 

    def __str__(self):
        return f"Estación Espacial: {self.nombre} \nTripulación: {self.tripulacion} \nPasaje: {self.pasaje} \nUbicación: {self.ubicacion.name}"
        
class NaveEstelar(Nave):
    def __init__(self, nombre, id_combate, clave_cifrada, tripulacion, pasaje, clase):
        super().__init__(nombre, id_combate, clave_cifrada)
        
        try:
            self.tripulacion = int(tripulacion)
            self.pasaje = int(pasaje)
        except ValueError:
            raise ValorInvalidoError(f"Error en '{nombre}': La tripulación y el pasaje deben ser números enteros.")
            
        if self.tripulacion < 0 or self.pasaje < 0:
            raise ValorInvalidoError(f"Error en '{nombre}': La tripulación y el pasaje no pueden ser negativos.")
            
        self.clase = clase 

    def __str__(self):
        return f"Nave Estelar: {self.nombre} \nTripulación: {self.tripulacion} \nPasaje: {self.pasaje} \nClase: {self.clase.name}"

class CazaEstelar(Nave):
    def __init__(self, nombre, id_combate, clave_cifrada, dotacion):
        super().__init__(nombre, id_combate, clave_cifrada)
        
        try:
            self.dotacion = int(dotacion)
        except ValueError:
            raise ValorInvalidoError(f"Error en '{nombre}': La dotación debe ser un número entero.")
            
        if self.dotacion < 0:
            raise ValorInvalidoError(f"Error en '{nombre}': La dotación no puede ser negativa.")

    def __str__(self):
        return f"Caza Estelar: {self.nombre} \nID: {self.id_combate} \nDotación: {self.dotacion}"