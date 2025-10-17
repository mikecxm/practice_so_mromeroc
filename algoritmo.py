class Proceso:
    def __init__(self, nombre, llegada, duracion, cola):
        self.nombre = nombre
        self.llegada = int(llegada)
        self.duracion = int(duracion)
        self.resto = int(duracion)
        self.cola = int(cola)
        self.finalizado = False
        self.tiempo_final = 0
        self.tiempo_espera = 0

def leer_procesos(nombre_archivo):
    lista = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            if linea.startswith('#') or linea.strip() == '':
                continue
            partes = linea.strip().split(';')
            nombre = partes[0].strip()
            duracion = partes[1].strip()
            llegada = partes[2].strip()
            cola = partes[3].strip()
            proceso = Proceso(nombre, llegada, duracion, cola)
            lista.append(proceso)
    return lista

def ejecutar_round_robin(procesos, quantum, tiempo):
    cola = [p for p in procesos if p.cola == 1]
    cola.sort(key=lambda p: p.llegada)
    lista_espera = cola.copy()
    while lista_espera:
        proceso = lista_espera.pop(0)
        if proceso.llegada > tiempo:
            tiempo = proceso.llegada
        ejecucion = min(quantum, proceso.resto)
        tiempo += ejecucion
        proceso.resto -= ejecucion
        if proceso.resto == 0:
            proceso.finalizado = True
            proceso.tiempo_final = tiempo
            proceso.tiempo_espera = tiempo - proceso.llegada - proceso.duracion
        else:
            lista_espera.append(proceso)
    return tiempo

def ejecutar_fcfs(procesos, tiempo, cola_num):
    cola = [p for p in procesos if p.cola == cola_num]
    cola.sort(key=lambda p: p.llegada)
    for proceso in cola:
        if proceso.llegada > tiempo:
            tiempo = proceso.llegada
        tiempo += proceso.duracion
        proceso.finalizado = True
        proceso.tiempo_final = tiempo
        proceso.tiempo_espera = tiempo - proceso.llegada - proceso.duracion
    return tiempo

def guardar_resultados(procesos, nombre_salida):
    with open(nombre_salida, 'w') as archivo:
        archivo.write("Nombre,Llegada,Duración,Cola,Final,Espera\n")
        for p in procesos:
            linea = f"{p.nombre},{p.llegada},{p.duracion},{p.cola},{p.tiempo_final},{p.tiempo_espera}"
            archivo.write(linea + '\n')
            print(linea)

def main():
    procesos = leer_procesos('mlq007.txt')
    tiempo = 0
    tiempo = ejecutar_round_robin(procesos, quantum=4, tiempo=tiempo)
    tiempo = ejecutar_fcfs(procesos, tiempo=tiempo, cola_num=2)
    tiempo = ejecutar_fcfs(procesos, tiempo=tiempo, cola_num=3)
    guardar_resultados(procesos, 'salida.txt')

main()