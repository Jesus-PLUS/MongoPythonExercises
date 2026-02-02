import pymongo

client = pymongo.MongoClient("mongodb+srv://chustappen:ALONSO-CAMPEON33@ej2.yy4swto.mongodb.net/") # O su string de conexión
db = client["gastronomia_db"]
collection = db["restaurantes"]

collection.delete_many({})

datos = [
    {"nombre": "La Bella Italia", "cocina": "Italiana", "barrio": "Centro", "calificacion": 4.5, "precio_promedio": 25, "menu": ["Pizza", "Pasta", "Risotto"], "abierto": True},
    {"nombre": "Sushimania", "cocina": "Japonesa", "barrio": "Norte", "calificacion": 4.8, "precio_promedio": 40, "menu": ["Sushi", "Ramen", "Tempura"], "abierto": True},
    {"nombre": "El Asador", "cocina": "Parrilla", "barrio": "Sur", "calificacion": 4.2, "precio_promedio": 35, "menu": ["Asado", "Chorizo", "Empanadas"], "abierto": False},
    {"nombre": "Tacos El Pastor", "cocina": "Mexicana", "barrio": "Centro", "calificacion": 4.0, "precio_promedio": 15, "menu": ["Tacos", "Quesadillas", "Burritos"], "abierto": True},
    {"nombre": "Burger King", "cocina": "Americana", "barrio": "Norte", "calificacion": 3.5, "precio_promedio": 12, "menu": ["Hamburguesa", "Papas", "Helado"], "abierto": True},
    {"nombre": "Veggie Life", "cocina": "Vegetariana", "barrio": "Sur", "calificacion": 4.6, "precio_promedio": 20, "menu": ["Ensalada", "Sopa", "Tofu"], "abierto": True},
    {"nombre": "Pasta & Basta", "cocina": "Italiana", "barrio": "Norte", "calificacion": 3.9, "precio_promedio": 22, "menu": ["Pasta", "Lasagna"], "abierto": True},
    {"nombre": "Tokyo Rolls", "cocina": "Japonesa", "barrio": "Centro", "calificacion": 4.1, "precio_promedio": 30, "menu": ["Sushi", "Sashimi"], "abierto": False},
]

collection.insert_many(datos)
print("Datos insertados correctamente.")

#Llega un nuevo competidor. Inserta un restaurante llamado "Café Central", de cocina "Cafetería", en el barrio "Centro", con calificación 4.39, precio promedio 10, menú ["Café", "Croissant"] y que esté abierto (True).

# 1
nuevo_res = {
    "nombre": "Café Central",
    "cocina": "Cafetería",
    "barrio": "Centro",
    "calificacion": 4.39,
    "precio_promedio": 10,
    "menu": ["Café", "Croissant"],
    "abierto": True}

result = collection.insert_one(nuevo_res)
print("1. Datos insertados correctamente. ID = ", {result.inserted_id})

# 2
italianos = collection.find({"cocina": "Italiana"})
print("2. Restaurantes de cocina Italiana:", { restaurante["nombre"] for restaurante in italianos })



# 3
# El restaurante "Burger King" ha mejorado su calidad. Actualiza su calificación a 3.89 y agrégale un campo nuevo llamado delivery con valor True.
update_BK = collection.update_one({"nombre": "Burger King"}, {"$set": {"calificacion": 3.89, "delivery": True}})
BK_updated = collection.find_one({"nombre": "Burger King" })
print("3. Burger King actualizado.", BK_updated)

# 4
# Eliminar un documento: El restaurante "El Asador" ha cerrado permanentemente. Elimínalo de la base de datos
res_totales = collection.count_documents({})
print("4. Total de restaurantes:", res_totales)
delete_Asador = collection.delete_one({"nombre": "El Asador"})
print("4. Restaurantes restantes (El Asador borrado):", collection.count_documents({}))

# 5
# Filtrado con Operadores Lógicos: Busca los restaurantes que tengan un precio promedio menor o igual a 200 Y que tengan una calificación mayor a 4.0.
restaurantes_filtrados = collection.find({"$and": [{"precio_promedio": {"$lte": 200}}, {"calificacion": {"$gt": 4.0}}]})
print("5. Restaurantes filtrados:", [restaurante["nombre"] for restaurante in restaurantes_filtrados])

# 6
# Búsqueda en Arrays: Encuentra todos los restaurantes que tengan "Sushi" dentro de su lista de menu (sin importar si tienen otros platos).
sushi_menu = collection.find({"menu": "Sushi"})
print("6. Restaurantes con Sushi en el menú:", [restaurante["nombre"] for restaurante in sushi_menu])

# 7
'''
Agrupación simple ($group): Queremos saber cuántos restaurantes hay en cada barrio. 
Escribe un pipeline que agrupe por barrio y cuente la cantidad (count) de restaurantes en cada uno.
'''
pipeline = [
    {"$group": {"_id": "$barrio", "count": {"$sum": 1}}}
]

print("7. Cantidad de restaurantes por barrio:")
result = collection.aggregate(pipeline)
for item in result:
    print(item)

# 8
'''
Promedios ($avg): Calcula cuál es el precio promedio de comer en cada tipo de cocina (ej: ¿Es más caro comer Japonés o Italiano en promedio?).
'''
pipeline_avg = [
    {"$group": {"_id": "$cocina", "avg_precio": {"$avg": "$precio_promedio"}}}
]
print("8. Precio promedio por tipo de cocina:")
result_avg = collection.aggregate(pipeline_avg)
for item in result_avg:
    print(item)

# 9
'''
Ordenamiento y Límites ($sort, $limit): Obtén el Top 3 de restaurantes con mejor calificación. Muestra solo el nombre y la calificación.
'''
pipeline_sort = [
    {"$sort": {"calificacion": -1}},
    {"$limit": 3},
    {"$project": {"_id": 0, "nombre": 1, "calificacion": 1}}
]
print("9. Top 3 restaurantes con mejor calificación:")
result_sort = collection.aggregate(pipeline_sort)
for item in result_sort:
    print(item)

# 10
'''
El "Jefe Final" ($unwind, $group, $sort): Queremos saber cuáles son los platos más populares (los que más se repiten en los menús de todos los restaurantes). 
Pista: Tendrás que "desenrollar" el array de menús, agrupar por el nombre del plato y contarlos, ordenándolos de mayor a menor frecuencia.
'''
pipeline_final = [
    {"$unwind": "$menu"},
    {"$group": {"_id": "$menu", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
print("10. Platos más populares:")
result_final = collection.aggregate(pipeline_final)
for item in result_final:
    print(item)