from enum import Enum

class Rol_usuario(Enum):
    COMANDANTE=1
    OPERARIO=2

class Ubicacion(Enum):
    ENDOR=1
    CUMULO_RAIMOS=2
    NEBULOSA_KALIIDA=3

class Clase_nave(Enum):
    EJECUTOR=1
    ECLIPSE=2
    SOBERANO=3


class Almacen:
    def __init__(self, nombre, localizacion):
        self.nombre=nombre
        self.localizacion=localizacion
        self.lista_repuestos=[]

    def agregar_repuesto(self, repuesto):
        self.lista_repuestos.append(repuesto)
        print(f'El repuesto {repuesto} se ha añadido al almacen {self.nombre}')

    def buscar_repuesto(self, repuesto):
        if repuesto in self.lista_repuestos:
            print(f'El repuesto {repuesto} está en la lista')
            return repuesto
        
        else:
            print(f'El repuesto no está en la lista')
            return None

    def actualizar_stock(self, repuesto, cantidad):
        repuesto_encontrado = self.buscar_repuesto(repuesto)

        if repuesto_encontrado != None and repuesto_encontrado.get_cantidad() >= cantidad:
            new_cant = repuesto_encontrado.get_cantidad() - cantidad
            repuesto_encontrado.set_cantidad(new_cant)

            return True

        else:
            print(f'Error \nRepuesto no encontrado o cantidad insuficiente en stock \nNo se puede actualizar el stock de {repuesto} en el almacen {self.nombre}')
            return False
        

class Repuesto:
    def __init__(self, nombre, proveedor, cantidad, precio):
        self.nombre=nombre
        self.proveedor=proveedor
        self.__cantidad=cantidad
        self.precio=precio

    def get_cantidad(self):
        return self.__cantidad
    
    def set_cantidad(self, nueva_cantidad):
        self.__cantidad = nueva_cantidad


class Sistema_miimperio:
    def __init__(self):
        self.naves_imperiales= []
        self.almacenes_imperiales=[]
        self.usuarios_registrados=[]


class Usuario:
    def __init__(self, rol):
        self.rol=rol

    def verificar_stock_repuesto(self, repuesto, almacen, cantidad):

        if self.rol == Rol_usuario.COMANDANTE:
            rep_disponible = almacen.buscar_repuesto(repuesto)

            if rep_disponible != None and rep_disponible.get_cantidad() >= cantidad:
                print(f'El repuesto {repuesto} está disponible en el almacen {almacen}')
                return rep_disponible
            else:
                print(f'El repuesto {repuesto} no está disponible en el almacen {almacen}')
                return None
        
        else:
            print('Acción restringida para Operarios')
            return None
    
    def adquirir_repuesto(self, repuesto, almacen, nave, cantidad):

        if self.rol == Rol_usuario.COMANDANTE:

            if self.verificar_stock_repuesto(repuesto, almacen) != None:
                nave._agregar_repuesto(repuesto, cantidad)
                print(f'Se ha adquirido {cantidad} unidades de {repuesto} con exito.')

        else:
            print('Acción restringida para Operarios')    


    def mantener_catalogo(self, almacen, repuesto):
            """Permite a los operarios añadir nuevos tipos de piezas al almacén."""
            if self.rol == Rol_usuario.OPERARIO:
                almacen.agregar_repuesto(repuesto)
                print(f"Operario {self.nombre} ha añadido {repuesto.nombre} al catálogo de {almacen.nombre}.")
            else:
                print("Acción denegada: Solo los operarios pueden mantener el catálogo.")

    def actualizar_stock(self, almacen, nombre_repuesto, nueva_cantidad):
            """Permite a los operarios reponer o ajustar el stock físico."""
            if self.rol == Rol_usuario.OPERARIO:
                repuesto = almacen.buscar_repuesto(nombre_repuesto)
                if repuesto:
                    repuesto.set_cantidad(nueva_cantidad)
                    print(f"Stock de {nombre_repuesto} actualizado a {nueva_cantidad} por {self.nombre}.")
                else:
                    print(f"No se encontró el repuesto {nombre_repuesto} para actualizar.")
            else:
                print("Acción denegada: Solo los operarios pueden actualizar stocks.")

class Unidad_combate:
    def __init__(self, id_combate, clave_cifrada):
        self.id_combate = id_combate
        self.clave_cifrada = clave_cifrada



class Nave(Unidad_combate):
    def __init__(self, nombre, id_combate, clave_cifrada):
        super().__init__(id_combate, clave_cifrada)
        self.nombre=nombre
        self.lista_repuestos= []


    def _agregar_repuesto(self, repuesto):
        self.lista_repuestos.append(repuesto)
        print(f'El repuesto {repuesto} se ha añadido a la lista de repuestos de la nave {self.nombre}')



class EstacionEspacial(Nave):
    def __init__(self, nombre, id_combate, clave_cifrada, tripulacion, pasaje, ubicacion):
        super().__init__(nombre, id_combate, clave_cifrada)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion 

        
class NaveEstelar(Nave):
    def __init__(self, nombre, id_combate, clave_cifrada, tripulacion, pasaje, clase):
        super().__init__(nombre, id_combate, clave_cifrada)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase 


class CazaEstelar(Nave):
    def __init__(self, nombre, id_combate, clave_cifrada, dotacion):
        super().__init__(nombre, id_combate, clave_cifrada)
        self.dotacion = dotacion







