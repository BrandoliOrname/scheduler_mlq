"""
Simulador MLQ (Multilevel Queue) - Versión Simplificada
Esquema: Cola1=RR(3), Cola2=RR(5), Cola3=FCFS
"""

class Proceso:
    """Representa un proceso del sistema"""
    
    def __init__(self, nombre, bt, at, cola, prioridad):
        # Datos de entrada
        self.nombre = nombre
        self.bt = bt  # Burst Time (tiempo total necesario)
        self.at = at  # Arrival Time (tiempo de llegada)
        self.cola = cola  # Cola asignada (1, 2 o 3)
        self.prioridad = prioridad
        
        # Variables de control
        self.tiempo_restante = bt
        self.primer_ejecucion = None  # Para calcular RT
        self.ct = 0  # Completion Time
        
    def ejecutar(self, tiempo_actual, quantum=None):
        """Ejecuta el proceso y retorna cuánto tiempo uso"""
        # Registrar primera ejecución
        if self.primer_ejecucion is None:
            self.primer_ejecucion = tiempo_actual
        
        # Calcular tiempo de ejecución
        if quantum is None:  # FCFS: ejecuta todo
            tiempo = self.tiempo_restante
        else:  # RR: ejecuta quantum o lo que quede
            tiempo = min(quantum, self.tiempo_restante)
        
        self.tiempo_restante -= tiempo
        
        # Si terminó, guardar tiempo de completación
        if self.tiempo_restante == 0:
            self.ct = tiempo_actual + tiempo
        
        return tiempo
    
    def terminado(self):
        """Verifica si ya terminó"""
        return self.tiempo_restante == 0
    
    def calcular_metricas(self):
        """Calcula WT, RT y TAT"""
        self.tat = self.ct - self.at  # TAT = CT - AT
        self.wt = self.tat - self.bt  # WT = TAT - BT
        self.rt = self.primer_ejecucion - self.at  # RT = primera_ejecución - AT


class PlanificadorMLQ:
    """Planificador con 3 colas: RR(3), RR(5), FCFS"""
    
    def __init__(self):
        # Tres colas vacías
        self.cola1 = []  # RR con quantum=3
        self.cola2 = []  # RR con quantum=5
        self.cola3 = []  # FCFS sin quantum
        
        self.todos_procesos = []
        self.tiempo = 0
    
    def leer_archivo(self, archivo):
        """Lee el archivo y crea los procesos"""
        with open(archivo, 'r') as f:
            for linea in f:
                linea = linea.strip()
                
                # Ignorar comentarios y líneas vacías
                if not linea or linea.startswith('#'):
                    continue
                
                # Parsear: nombre;BT;AT;cola;prioridad
                datos = linea.split(';')
                p = Proceso(
                    nombre=datos[0].strip(),
                    bt=int(datos[1]),
                    at=int(datos[2]),
                    cola=int(datos[3]),
                    prioridad=int(datos[4])
                )
                self.todos_procesos.append(p)
        
        print(f"✓ {len(self.todos_procesos)} procesos cargados\n")
    
    def agregar_a_colas(self):
        """Agrega procesos que ya llegaron a sus colas correspondientes"""
        for p in self.todos_procesos:
            # Si ya llegó y no está en ninguna cola y no terminó
            if (p.at <= self.tiempo and not p.terminado() and 
                p not in self.cola1 and p not in self.cola2 and p not in self.cola3):
                
                # Asignar según su cola
                if p.cola == 1:
                    self.cola1.append(p)
                elif p.cola == 2:
                    self.cola2.append(p)
                else:
                    self.cola3.append(p)
        
        # Ordenar por prioridad (mayor primero)
        self.cola1.sort(key=lambda x: -x.prioridad)
        self.cola2.sort(key=lambda x: -x.prioridad)
        self.cola3.sort(key=lambda x: -x.prioridad)
    
    def ejecutar(self):
        """Ejecuta la simulación del algoritmo MLQ"""
        print("="*60)
        print("INICIANDO SIMULACIÓN MLQ")
        print("Cola 1: Round Robin (Q=3)")
        print("Cola 2: Round Robin (Q=5)")
        print("Cola 3: FCFS")
        print("="*60 + "\n")
        
        # Mientras haya procesos sin terminar
        while any(not p.terminado() for p in self.todos_procesos):
            self.agregar_a_colas()
            
            proceso = None
            quantum = None
            cola_nombre = ""
            
            # PRIORIDAD: Cola1 > Cola2 > Cola3
            if self.cola1:
                proceso = self.cola1[0]
                quantum = 3
                cola_nombre = "Cola 1 (RR-3)"
            elif self.cola2:
                proceso = self.cola2[0]
                quantum = 5
                cola_nombre = "Cola 2 (RR-5)"
            elif self.cola3:
                proceso = self.cola3[0]
                quantum = None  # FCFS ejecuta todo
                cola_nombre = "Cola 3 (FCFS)"
            
            if proceso:
                # Ejecutar proceso
                tiempo_usado = proceso.ejecutar(self.tiempo, quantum)
                
                print(f"t={self.tiempo:2d}→{self.tiempo+tiempo_usado:2d}: "
                      f"[{proceso.nombre}] {cola_nombre} "
                      f"(queda {proceso.tiempo_restante})")
                
                # Actualizar tiempo
                self.tiempo += tiempo_usado
                
                # Si terminó, quitarlo de la cola
                if proceso.terminado():
                    if proceso in self.cola1:
                        self.cola1.remove(proceso)
                    elif proceso in self.cola2:
                        self.cola2.remove(proceso)
                    elif proceso in self.cola3:
                        self.cola3.remove(proceso)
                    print(f"     └─> [{proceso.nombre}] TERMINÓ ✓\n")
                else:
                    # RR: mover al final de la cola
                    if proceso in self.cola1:
                        self.cola1.remove(proceso)
                        self.cola1.append(proceso)
                    elif proceso in self.cola2:
                        self.cola2.remove(proceso)
                        self.cola2.append(proceso)
            else:
                # No hay procesos listos, avanzar tiempo
                self.tiempo += 1
        
        # Calcular métricas finales
        for p in self.todos_procesos:
            p.calcular_metricas()
        
        print("="*60)
        print("SIMULACIÓN COMPLETADA")
        print("="*60 + "\n")
    
    def mostrar_resultados(self):
        """Muestra resultados en tabla"""
        print("\n" + "="*80)
        print("RESULTADOS FINALES")
        print("="*80)
        print(f"{'Proc':<6} {'BT':<4} {'AT':<4} {'Cola':<6} {'Pr':<4} "
              f"{'WT':<5} {'CT':<5} {'RT':<5} {'TAT':<5}")
        print("-"*80)
        
        for p in sorted(self.todos_procesos, key=lambda x: x.ct):
            print(f"{p.nombre:<6} {p.bt:<4} {p.at:<4} {p.cola:<6} {p.prioridad:<4} "
                  f"{p.wt:<5} {p.ct:<5} {p.rt:<5} {p.tat:<5}")
        
        # Promedios
        n = len(self.todos_procesos)
        avg_wt = sum(p.wt for p in self.todos_procesos) / n
        avg_ct = sum(p.ct for p in self.todos_procesos) / n
        avg_rt = sum(p.rt for p in self.todos_procesos) / n
        avg_tat = sum(p.tat for p in self.todos_procesos) / n
        
        print("-"*80)
        print(f"PROMEDIOS: WT={avg_wt:.1f}  CT={avg_ct:.1f}  "
              f"RT={avg_rt:.1f}  TAT={avg_tat:.1f}")
        print("="*80 + "\n")
    
    def guardar_salida(self, nombre_salida):
        """Guarda resultados en archivo"""
        with open(nombre_salida, 'w') as f:
            f.write(f"# archivo: {nombre_salida}\n")
            f.write("# etiqueta; BT; AT; Q; Pr; WT; CT; RT; TAT\n")
            
            for p in sorted(self.todos_procesos, key=lambda x: x.ct):
                f.write(f"{p.nombre};{p.bt};{p.at};{p.cola};{p.prioridad};"
                       f"{p.wt};{p.ct};{p.rt};{p.tat}\n")
            
            # Promedios
            n = len(self.todos_procesos)
            avg_wt = sum(p.wt for p in self.todos_procesos) / n
            avg_ct = sum(p.ct for p in self.todos_procesos) / n
            avg_rt = sum(p.rt for p in self.todos_procesos) / n
            avg_tat = sum(p.tat for p in self.todos_procesos) / n
            
            f.write(f"WT={avg_wt:.1f}; CT={avg_ct:.1f}; "
                   f"RT={avg_rt:.1f}; TAT={avg_tat:.1f};\n")
        
        print(f"✓ Archivo guardado: {nombre_salida}\n")


# PROGRAMA PRINCIPAL


def main():
    print("\n" + "="*60)
    print("SIMULADOR MLQ - MULTILEVEL QUEUE")
    print("="*60 + "\n")
    
    # Pedir archivo de entrada
    archivo = input("Archivo de entrada: ")
    
    # Crear planificador y ejecutar
    mlq = PlanificadorMLQ()
    mlq.leer_archivo(archivo)
    mlq.ejecutar()
    mlq.mostrar_resultados()
    
    # Guardar salida
    salida = archivo.replace('.txt', '_output.txt')
    mlq.guardar_salida(salida)
    
    print("✓ Proceso completado\n")


if __name__ == "__main__":
    main()