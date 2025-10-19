# scheduler_mlq
# Simulador MLQ (Multilevel Queue Scheduling)

## Descripción
Implementación del algoritmo de planificación MLQ con el esquema:
- Cola 1: Round Robin (Quantum = 3)
- Cola 2: Round Robin (Quantum = 5)
- Cola 3: FCFS (First Come First Serve)

## Estructura del Proyecto
```
MLQ_Scheduler/
├── src/
│   └── mlq_scheduler.py
├── input/
│   └── mlq001.txt
├── output/
│   └── (archivos de salida)
└── README.md
```

## Cómo Ejecutar

1. Navegar a la carpeta src:
```bash
   cd src
```

2. Ejecutar el programa:
```bash
   python mlq_scheduler.py
```

3. Ingresar el archivo de entrada:
```
   ../input/mlq001.txt
```

## Requisitos
- Python 3.14.0

## Autor
Brandon Alexis Franco Flor

## Curso
Sistemas Operativos - Universidad del Valle

