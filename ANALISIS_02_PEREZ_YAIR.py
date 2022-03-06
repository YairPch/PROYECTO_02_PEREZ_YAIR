#!/usr/bin/env python
# coding: utf-8

# ### Yair Arturo Pérez Chávez
# 
# ### Proyecto 2: Introducción al Análisis de Datos

# Synergy Logistics es una empresa dedicada a la intermediación de servicios de importación de diferentes productos. Recientemente, la dirección de la compañía ha solicitado al área de operaciones, recomendar una estrategia en la que se pueda analizar la viabilidad de 3 opciones de enfoque, que a continuación se presentan.

# In[148]:


import pandas as pd
import matplotlib.pyplot as plt


# ### 1) Rutas de Importación y Exportación
# 
# SL está considerando enfocar sus esfuerzos a las 10 rutas más demandadas, que son las siguientes:

# #### Importamos la base de datos y la guardamos en una variable

# In[78]:


database = pd.read_csv("synergy_logistics_database.csv",index_col=0, parse_dates=[5])


# #### Agrupamos la base por origen, destino y modo de transporte
# #### Luego, sumamos el valor de cada ruta

# In[79]:


route = database.groupby(by=["direction","origin","destination","transport_mode"])
valor_total = route.sum()["total_value"]


# #### Se hace un análisis descriptivo de las rutas y se ordenan de mayor a menor considerando qué tanto se repiten

# In[80]:


route = route["total_value"].describe().sort_values(by="count", ascending = False)


# #### Se agrega el total en una columna nueva para poder hacer el análisis en conjunto

# In[81]:


route["total"] = valor_total
route = route.reset_index()


# #### Sólo consideraremos las importaciones

# In[82]:


imp = route[route["direction"] == "Imports"]
imp


# #### Sólo consideramos las exportaciones

# In[14]:


exp = route[route["direction"] == "Exports"]
exp


# #### Top 10 rutas de exportación por cantidad

# In[15]:


top_10_exp = exp.head(9)
top_10_exp


# #### Calculamos el valor total de todas las exportaciones

# In[16]:


valor_exportaciones = exp["total"].sum()
valor_exportaciones


# #### Calculamos el valor total de las 10 principales exportaciones por cantidad

# In[17]:


valor_top_10 = top_10_exp["total"].sum()
valor_top_10


# #### Rutas más usadas

# In[196]:


tabla = top_10_exp[["origin","destination","total"]]
tabla


# #### ¿Cuánto representa el valor del top 10 del total de exportaciones?

# In[197]:


porcent_exp = int(valor_top_10 / valor_exportaciones * 10000) / 100
print(f"Las rutas más utilizadas representan un {porcent_exp}% de las ventas siendo: \n {tabla}")


# ### Todo lo anterior se puede simplificar con una función que toma la base de datos, el número de transacciones principales que se quieren analizar y el nombre del valor por el que se desean ordenar.

# In[199]:


def rutas(data,top,order):
    valor_data = exp["total"].sum()
    valor_top = data.sort_values(by = order,ascending = False).head(top)
    valor_data = data["total"].sum()
    valor_top_10 = valor_top["total"].sum()
    viaje = valor_top[["origin","destination","total"]]
    porcentaje = int(valor_top_10 / valor_data * 10000) / 100
    print(f"El top {top} representa el {porcentaje}% de las ventas, siendo las siguientes: \n {viaje}")


# #### Rutas más demandadas (Importaciones)

# In[200]:


r_imp = rutas(imp, 10, "count")


# #### Rutas con mayor valor (Importaciones)

# In[201]:


rutas(imp, 10, "total")


# #### Rutas más demandadas (Exportaciones)

# In[202]:


rutas(exp, 10, "count")


# #### Rutas con mayor valor (Exportaciones)

# In[203]:


rutas(exp, 10, "total")


# ### 2) Medio de Transporte Utilizado
# 
# SL está considerando reducir los medios de transporte que son menos importantes para la empresa, siendo éstos los siguientes:

# #### Utilizaremos la base de route, cambiando su nombre para no generar confusión

# In[105]:


transporte = route


# #### Separamos la base en importaciones y exportaciones como se hizo anteriormente

# In[106]:


export = transporte[transporte["direction"] == "Exports"]
impor = transporte[transporte["direction"] == "Imports"]


# #### Se consideran las 10 rutas de exportación que generan mayor valor económico, destacando su respectivo medio de transporte

# In[107]:


top_tran_exp = export.sort_values(by="total",ascending=False).head(10)
top_tran_exp


# #### Se toma en consideración sólo el medio de transporte y dirección para calcular el valor total por medio de transporte

# In[103]:


transport = database.groupby(by=["direction","transport_mode"])
valor_tot = transport.sum()["total_value"]
transport = transport["total_value"].describe().sort_values(by="count", ascending = False)
transport["total"] = valor_tot
transport = transport.reset_index()


# #### Separamos por exportaciones e importaciones

# In[111]:


transport_exp = transport[transport["direction"] == "Exports"]
transport_imp = transport[transport["direction"] == "Imports"]


# #### Se ordenan de forma ascendente de acuerdo al valor total

# In[113]:


top_transport_exp = transport_exp.sort_values(by="total",ascending = False)
top_transport_exp


# In[161]:


top_transport_exp.plot(x = "transport_mode", y ="total",kind="bar",width = 0.9,color="lightgreen")


# In[114]:


top_transport_imp = transport_imp.sort_values(by="total",ascending = False)
top_transport_imp


# In[205]:


top_transport_imp.plot(x = "transport_mode", y ="total",kind="bar",width = 0.9,color="navy")


# #### Se ordenan de forma ascendente de acuerdo a la cantidad de viajes realizados

# In[115]:


top_transport_expc = transport_exp.sort_values(by="count",ascending = False)
top_transport_expc


# In[177]:


top_transport_expc.plot(x = "transport_mode", y ="total",kind="barh",width = 0.9,color="lightblue")


# In[116]:


top_transport_impc = transport_imp.sort_values(by="count",ascending = False)
top_transport_impc


# In[178]:


top_transport_impc.plot(x = "transport_mode", y ="total",kind="barh",width = 0.9,color="lightblue")


# ### 3) Valor total de importaciones y exportaciones
# 
# SL está considerando enfocarse en los países que le generan el 80% del valor de las exportaciones e importaciones, siendo los siguientes:

# In[117]:


eighty = route
eighty


# #### Separamos en exportaciones e importaciones

# In[119]:


eighty_exp = eighty[eighty["direction"] == "Exports"]
eighty_imp = eighty[eighty["direction"] == "Imports"]


# #### Ordenamos la base por país de origen

# In[126]:


pais = eighty_exp.groupby("origin").sum()


# #### Calculamos el porcentaje que representa el valor de cada país con respecto al total y ordenamos de mayor a menor.

# In[140]:


pais["%"] = (pais["total"] / pais["total"].sum()*10000)/100
pais_perc = pais.sort_values(by = "%", ascending = False)
pais_perc


# #### Se acumula el porcentaje de mayor a menor

# In[143]:


acumulado = pais_perc.cumsum()["%"]
acumulado


# In[209]:


pais_perc["% acum"] = acumulado
pais_perc[["%","% acum"]].head(10)


# #### Obtenemos el top 80

# In[147]:


top80 = pais_perc[pais_perc["% acum"] < 83]
top80


# In[167]:


top80["% acum"].plot(kind="barh",width = 0.9,color="lightgreen")


# #### Link Github

# https://github.com/YairPch/PROYECTO_02_PEREZ_YAIR.git
