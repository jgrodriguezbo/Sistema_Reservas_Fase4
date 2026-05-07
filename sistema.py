from abc import ABC, abstractmethod

# -----------------------------
# FUNCION PARA LOGS
# -----------------------------

def guardar_error(mensaje):
    with open("errores.log", "a") as archivo:
        archivo.write(mensaje + "\n")


# -----------------------------
# EXCEPCIONES PERSONALIZADAS
# -----------------------------

class ErrorCliente(Exception):
    pass

class ErrorServicio(Exception):
    pass

class ErrorReserva(Exception):
    pass


# -----------------------------
# CLASE ABSTRACTA BASE
# -----------------------------

class Entidad(ABC):

    def __init__(self, nombre):
        self._nombre = nombre


# -----------------------------
# CLASE CLIENTE
# -----------------------------

class Cliente(Entidad):

    def __init__(self, nombre, correo):
        super().__init__(nombre)

        if "@" not in correo:
            raise ErrorCliente("Correo inválido")

        self._correo = correo

    def mostrar(self):
        return f"Cliente: {self._nombre} - {self._correo}"


# -----------------------------
# CLASE ABSTRACTA SERVICIO
# -----------------------------

class Servicio(ABC):

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# -----------------------------
# SERVICIOS
# -----------------------------

class ReservaSala(Servicio):

    def __init__(self, horas):
        if horas <= 0:
            raise ErrorServicio("Horas inválidas")

        self._horas = horas

    def calcular_costo(self):
        return self._horas * 50000

    def descripcion(self):
        return f"Reserva de sala por {self._horas} horas"


class AlquilerEquipo(Servicio):

    def __init__(self, dias):
        if dias <= 0:
            raise ErrorServicio("Días inválidos")

        self._dias = dias

    def calcular_costo(self):
        return self._dias * 30000

    def descripcion(self):
        return f"Alquiler de equipo por {self._dias} días"


class Asesoria(Servicio):

    def __init__(self, sesiones):
        if sesiones <= 0:
            raise ErrorServicio("Sesiones inválidas")

        self._sesiones = sesiones

    def calcular_costo(self):
        return self._sesiones * 80000

    def descripcion(self):
        return f"Asesoría por {self._sesiones} sesiones"


# -----------------------------
# CLASE RESERVA
# -----------------------------

class Reserva:

    def __init__(self, cliente, servicio):
        if cliente is None or servicio is None:
            raise ErrorReserva("Datos incompletos")

        self._cliente = cliente
        self._servicio = servicio
        self._estado = "Pendiente"

    def confirmar(self):
        self._estado = "Confirmada"

    def cancelar(self):
        self._estado = "Cancelada"

    def procesar(self):
        return f"{self._cliente.mostrar()} | {self._servicio.descripcion()} | Estado: {self._estado}"


# -----------------------------
# SIMULACIÓN DEL SISTEMA
# -----------------------------

clientes = []
reservas = []

print("\n--- INICIO DEL SISTEMA ---\n")

# ----------- CLIENTES -----------

try:
    c1 = Cliente("Jose", "jose@gmail.com")
    clientes.append(c1)

    c2 = Cliente("Maria", "maria@gmail.com")
    clientes.append(c2)

    c3 = Cliente("Luis", "luis@gmail.com")
    clientes.append(c3)

    c4 = Cliente("Ana", "correo_invalido")  # ERROR

    clientes.append(c4)

except ErrorCliente as e:
    print("Error cliente:", e)
    guardar_error("Error cliente: " + str(e))

finally:
    print("Proceso de clientes finalizado\n")


# ----------- SERVICIOS Y RESERVAS -----------

try:
    s1 = ReservaSala(2)
    r1 = Reserva(c1, s1)
    r1.confirmar()
    reservas.append(r1)

    s2 = AlquilerEquipo(3)
    r2 = Reserva(c2, s2)
    reservas.append(r2)

    s3 = Asesoria(1)
    r3 = Reserva(c3, s3)
    r3.confirmar()
    reservas.append(r3)

    s4 = ReservaSala(-2)  # ERROR
    r4 = Reserva(c1, s4)
    reservas.append(r4)

    s5 = AlquilerEquipo(5)
    r5 = Reserva(c2, s5)
    r5.cancelar()
    reservas.append(r5)

    s6 = Asesoria(-1)  # ERROR
    r6 = Reserva(c3, s6)
    reservas.append(r6)

except (ErrorServicio, ErrorReserva) as e:
    print("Error reserva:", e)
    guardar_error("Error reserva: " + str(e))

finally:
    print("Proceso de reservas finalizado\n")


# ----------- MOSTRAR RESULTADOS -----------

print("--- RESERVAS VALIDAS ---\n")

for r in reservas:
    try:
        print(r.procesar())
    except Exception as e:
        print("Error al procesar:", e)
        guardar_error("Error al procesar: " + str(e))

print("\n--- FIN DEL SISTEMA ---")