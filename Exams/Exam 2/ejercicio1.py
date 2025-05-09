# -*- coding: utf-8 -*-
"""ejercicio1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1IEvf6zaKA5JetBVIKs_Fj2b_5i8gADiI
"""

pip install pulp

from pulp import *

#Para resolver en pulp se define el problema
ciudades = pulp.LpProblem("Problema de transporte de ciudades", LpMinimize)

#se definen las plantas y sus capacidades
plantas = ["Los Angeles", "Detroit", "Nueva Orleans"]
capacidades = {"Los Angeles":1000, "Detroit":1500, "Nueva Orleans":1200}


#se definen los centros y sus demandas
centros = ["Denver", "Miami"]
demanda = {"Denver": 2300, "Miami": 1400}

#matriz de los costos
costos = [[80, 215],
          [100, 108],
          [102, 68]
          ]

#se transforman los costos en un diccionario de pulp
costos = makeDict([plantas, centros], costos, 0)

#se conectan las rutas entre cada elemento x11, x12, etc
rutas = [(p, c) for p in plantas for c in centros]

#se definen la cantidad de variables
nro_variables = LpVariable.dicts("Cantidad", (plantas, centros), 0, None, LpInteger)

#esta la función objetivo
ciudades += lpSum(nro_variables[p][c] * costos[p][c] for p in plantas for c in centros)

#restricciones para las plantas
for p in plantas:
  ciudades+=lpSum([nro_variables[p][c] for c in centros])==capacidades[p]

#restricciones para los centros
for c in centros:
  ciudades+=lpSum([nro_variables[p][c] for p in plantas])==demanda[c]

#se resuelve
ciudades.solve()

#se define la condición óptima
print(f"Condición: {LpStatus[ciudades.status]}")

#se le da valor a cada variable x11, x12, etc
for i in ciudades.variables():
  print(f"{i.name}={i.varValue}")

#se imprime el valor optimo
print(f"Optimizacion: = {ciudades.objective.value()}")