import csv
from datetime import datetime, timedelta

# Leer el archivo CSV
columns = ['Fecha', 'Resultado']
rows = []
with open('requests.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        rows.append(row)

# Filtrar filas con valores de fecha no válidos
valid_rows = []
for row in rows:
    try:
        fecha = datetime.strptime(row['Fecha'], '%Y-%m-%d %H:%M:%S')
        row['Fecha'] = fecha
        valid_rows.append(row)
    except ValueError:
        pass

# Obtener la fecha actual
fecha_actual = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

# Filtrar por fechas de los dos meses anteriores
fecha_inicio = fecha_actual - timedelta(days=60)
rows_filtrado = [row for row in valid_rows if fecha_inicio <= row['Fecha'] < fecha_actual]

# Calcular la ratio de solicitudes realizadas correctamente
total_solicitudes = len(rows_filtrado)
solicitudes_correctas = len([row for row in rows_filtrado if row['Resultado'] == 'Petición OK'])
ratio = solicitudes_correctas / total_solicitudes if total_solicitudes > 0 else 0

# Obtener las ratios de los dos meses anteriores
fecha_anterior = fecha_actual - timedelta(days=30)
rows_anterior = [row for row in valid_rows if fecha_inicio <= row['Fecha'] < fecha_anterior]
solicitudes_correctas_anterior = len([row for row in rows_anterior if row['Resultado'] == 'Petición OK'])
ratio_anterior = solicitudes_correctas_anterior / len(rows_anterior) if len(rows_anterior) > 0 else 0

fecha_anteanterior = fecha_actual - timedelta(days=60)
rows_anteanterior = [row for row in valid_rows if fecha_inicio <= row['Fecha'] < fecha_anteanterior]
solicitudes_correctas_anteanterior = len([row for row in rows_anteanterior if row['Resultado'] == 'Petición OK'])
ratio_anteanterior = solicitudes_correctas_anteanterior / len(rows_anteanterior) if len(rows_anteanterior) > 0 else 0

# Determinar la tendencia mensual
if ratio_anterior < ratio or ratio_anteanterior < ratio:
    tendencia = "TENDENCIA POSITIVA"
elif ratio_anterior > ratio or ratio_anteanterior > ratio:
    tendencia = "TENDENCIA NEGATIVA"
else:
    tendencia = "TENDENCIA NULA"

# Obtener el número total de peticiones realizadas en cada mes
peticiones_totales = len(rows_filtrado)
peticiones_mes_anterior = len(rows_anterior)
peticiones_mes_anteanterior = len(rows_anteanterior)

# Generar un archivo con las ratios y el número total de peticiones
headers = ['Fecha Actual', 'Ratio Actual', 'Peticiones Total Mes Actual',
           'Ratio Mes Anterior', 'Peticiones Total Mes Anterior',
           'Ratio Mes Anteanterior', 'Peticiones Total Meses Anteanterior',
           'Tendencia']
data = [fecha_actual, ratio, peticiones_totales, ratio_anterior, peticiones_mes_anterior, ratio_anteanterior,
peticiones_mes_anteanterior, tendencia]

with open('ratios.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerow(data)
       
