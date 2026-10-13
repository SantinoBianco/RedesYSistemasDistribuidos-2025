import requests

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']},"
          f"Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas',
                         json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']},"
          f"Título: {pelicula_agregada['titulo']},"
          f"Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']},"
          f"Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}',
                        json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']},"
          f"Título: {pelicula_actualizada['titulo']},"
          f"Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()

# Lista de peliculas por genero
genero = 'Acción'  # Genero cualquiera
response = requests.get(f'http://localhost:5000/peliculas/por_genero/{genero}')
print(f"Peliculas por genero: {genero}")
if response.status_code == 200:
    peliculas_por_genero = response.json()
    print('[')
    for pelicula in peliculas_por_genero:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']},"
              f"Género: {pelicula['genero']}")
    print(']')
else:
    print('[]')

# Lista de peliculas por titulo
titulo = 'Star Wars'  # Genero cualquiera
response = requests.get(f'http://localhost:5000/peliculas/por_titulo/{titulo}')
print(f"Peliculas por titulo: {titulo}")
if response.status_code == 200:
    peliculas_por_titulo = response.json()
    print('[')
    for pelicula in peliculas_por_titulo:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']},"
              f"Género: {pelicula['genero']}")
    print(']')
else:
    print('[]')
print()

# Pelicula aleatoria
response = requests.get(f'http://localhost:5000/peliculas/aleatoria')
if response.status_code == 200:
    print("Pelicula aleatoria:")
    pelicula = response.json()
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']},"
          f"Género: {pelicula['genero']}")
else:
    print("No hay peliculas para recomendar")
print()

# Pelicula aleatoria segun genero
genero = 'Acción'  # Genero cualquiera
response = requests.get(f'http://localhost:5000/peliculas/aleatoria/{genero}')
print(f"Pelicula aleatoria por genero: {genero}")
if response.status_code == 200:
    pelicula = response.json()
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']},"
          f"Género: {pelicula['genero']}")
else:
    print("Error al obtener la película aleatoria por genero.")
print()

# Sugerir pelicula por feriado segun genero
genero = 'Drama'
response = requests.get(f'http://localhost:5000/peliculas/'
                        f'sugerencia_feriado/{genero}')
if response.status_code == 200:
    sugerencia = response.json()
    print("Detalles de la sugerencia:")
    feriado = sugerencia.get('feriado', {})
    recomendacion = sugerencia.get('recomendacion', {})

    print(f"feriado: {feriado['fecha']}, motivo: {feriado['motivo']}")

    pelicula = recomendacion.get('pelicula', {})

    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']},"
          f"Género: {pelicula['genero']}")
else:
    print("No hay películas con este género o no se pudo obtener"
          "la sugerencia.")
print()
