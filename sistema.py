from abc import ABC, abstractmethod

# ---------------------------------
# FUNCION PARA GUARDAR LOGS
# ---------------------------------

def guardar_log(mensaje):
    with open("errores.log", "a", encoding="utf-8") as archivo:
        archivo.write(mensaje + "\n")


# ---------------------------------
# EXCEPCIONES PERSONALIZADAS
# ---------------------------------

class ErrorCliente(Exception):
    pass


class ErrorServicio(Exception):
    pass


class ErrorReserva(Exception):
    pass


# ---------------------------------
# CLASE ABSTRACTA BASE
# ---------------------------------

class Entidad(ABC):

    def __init__(self, nombre):
        self._nombre = nombre

    @abstractmethod
    def descripcion(self):
        pass


# ---------------------------------
# CLASE CLIENTE
# ---------------------------------

class Cliente(Entidad):

    def __init__(self, nombre, correo):
        super().__init__(nombre)

        if "@" not in correo:
            raise ErrorCliente("Correo inválido")

        self._correo = correo

    def mostrar(self):
        return f"Cliente: {self._nombre} - {self._correo}"

    def descripcion(self):
        return f"Cliente registrado: {self._nombre}"


# ---------------------------------
# CLASE ABSTRACTA SERVICIO
# ---------------------------------

class Servicio(ABC):

    @abstractmethod
    def calcular_costo(self, descuento=0):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# ---------------------------------
# CLASE RESERVA DE SALA
# ---------------------------------

class ReservaSala(Servicio):

    def __init__(self, horas):

        try:
            if horas <= 0:
                raise ValueError

            self._horas = horas

        except ValueError as e:
            raise ErrorServicio("Horas inválidas") from e

    # SOBRECARGA CON PARAMETRO OPCIONAL
    def calcular_costo(self, descuento=0):

        costo = self._horas * 50000

        if descuento > 0:
            costo = costo - descuento

        return costo

    def descripcion(self):
        return f"Reserva de sala por {self._horas} horas"


# ---------------------------------
# CLASE ALQUILER DE EQUIPO
# ---------------------------------

class AlquilerEquipo(Servicio):

    def __init__(self, dias):

        try:
            if dias <= 0:
                raise ValueError

            self._dias = dias

        except ValueError as e:
            raise ErrorServicio("Días inválidos") from e

    def calcular_costo(self, descuento=0):

        costo = self._dias * 30000

        if descuento > 0:
            costo = costo - descuento

        return costo

    def descripcion(self):
        return f"Alquiler de equipo por {self._dias} días"


# ---------------------------------
# CLASE ASESORIA
# ---------------------------------

class Asesoria(Servicio):

    def __init__(self, sesiones):

        try:
            if sesiones <= 0:
                raise ValueError

            self._sesiones = sesiones

        except ValueError as e:
            raise ErrorServicio("Sesiones inválidas") from e

    def calcular_costo(self, descuento=0):

        costo = self._sesiones * 80000

        if descuento > 0:
            costo = costo - descuento

        return costo

    def descripcion(self):
        return f"Asesoría por {self._sesiones} sesiones"


# ---------------------------------
# CLASE RESERVA
# ---------------------------------

class Reserva:

    def __init__(self, cliente, servicio):

        if cliente is None or servicio is None:
            raise ErrorReserva("Datos incompletos")

        self._cliente = cliente
        self._servicio = servicio
        self._estado = "Pendiente"

    def confirmar(self):

        self._estado = "Confirmada"

        guardar_log(
            f"Reserva confirmada para {self._cliente._nombre}"
        )

    def cancelar(self):

        self._estado = "Cancelada"

        guardar_log(
            f"Reserva cancelada para {self._cliente._nombre}"
        )

    def procesar(self):

        return (
            f"{self._cliente.mostrar()} | "
            f"{self._servicio.descripcion()} | "
            f"Costo: ${self._servicio.calcular_costo()} | "
            f"Estado: {self._estado}"
        )


# ---------------------------------
# SIMULACION DEL SISTEMA
# ---------------------------------

clientes = []
reservas = []

print("\n--- INICIO DEL SISTEMA ---\n")


# ---------------------------------
# CREACION DE CLIENTES
# ---------------------------------

try:

    c1 = Cliente("Jose", "jose@gmail.com")
    clientes.append(c1)

    c2 = Cliente("Maria", "maria@gmail.com")
    clientes.append(c2)

    c3 = Cliente("Luis", "luis@gmail.com")
    clientes.append(c3)

    # ERROR INTENCIONAL
    c4 = Cliente("Ana", "correo_invalido")
    clientes.append(c4)

except ErrorCliente as e:

    print("Error cliente:", e)

    guardar_log("Error cliente: " + str(e))

else:

    print("Clientes creados correctamente")

finally:

    print("Proceso de clientes finalizado\n")


# ---------------------------------
# CREACION DE RESERVAS
# ---------------------------------

try:

    # RESERVA 1
    s1 = ReservaSala(2)
    r1 = Reserva(c1, s1)
    r1.confirmar()
    reservas.append(r1)

    # RESERVA 2
    s2 = AlquilerEquipo(3)
    r2 = Reserva(c2, s2)
    reservas.append(r2)

    # RESERVA 3
    s3 = Asesoria(1)
    r3 = Reserva(c3, s3)
    r3.confirmar()
    reservas.append(r3)

    # RESERVA 4
    s4 = ReservaSala(5)
    r4 = Reserva(c1, s4)
    r4.cancelar()
    reservas.append(r4)

    # RESERVA 5
    s5 = AlquilerEquipo(1)
    r5 = Reserva(c2, s5)
    r5.confirmar()
    reservas.append(r5)

    # ERROR INTENCIONAL
    s6 = Asesoria(-1)
    r6 = Reserva(c3, s6)
    reservas.append(r6)

except ErrorServicio as e:

    print("Error servicio:", e)

    guardar_log("Error servicio: " + str(e))

except ErrorReserva as e:

    print("Error reserva:", e)

    guardar_log("Error reserva: " + str(e))

else:

    print("Reservas creadas correctamente")

finally:

    print("Proceso de reservas finalizado\n")


# ---------------------------------
# MOSTRAR RESERVAS
# ---------------------------------

print("--- RESERVAS VALIDAS ---\n")

for reserva in reservas:

    try:

        print(reserva.procesar())

    except Exception as e:

        print("Error al procesar:", e)

        guardar_log("Error al procesar: " + str(e))


print("\n--- FIN DEL SISTEMA ---")