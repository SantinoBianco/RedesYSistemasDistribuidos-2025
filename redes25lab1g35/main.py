from flask import Flask, jsonify, request, Response
from typing import Union
import random
from proximo_feriado import NextHoliday

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


def obtener_peliculas() -> Response:
    return jsonify(peliculas)


def obtener_pelicula(id: int) -> Union[Response, None]:
    """
    Busca una película por su ID y devuelve sus detalles.

    :param id: ID de la película a buscar.
    :return: Respuesta JSON con los detalles de la película si se encuentra,
             o un mensaje de error si no se encuentra.
    """
    # Lógica para buscar la película por su ID y devolver sus detalles
    for p in peliculas:
        if p['id'] == id:
            pelicula_encontrada = p
            return jsonify(pelicula_encontrada)
    return jsonify({'Mensaje': 'Pelicula no encontrada'}), 404


def agregar_pelicula() -> Union[Response, None]:
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id: int) -> Union[Response, None]:
    """
    Actualiza los detalles de una película existente.

    :param id: ID de la película a actualizar.
    :return: Respuesta JSON con los detalles de la película actualizada,
             o un mensaje de error si no se encuentra.
    """
    # Lógica para buscar la película por su ID y actualizar sus detalles
    for p in peliculas:
        if p['id'] == id:
            p['titulo'] = request.json.get('titulo', p['titulo'])
            p['genero'] = request.json.get('genero', p['genero'])
            pelicula_actualizada = p
            return jsonify(pelicula_actualizada)
    return jsonify({'Mensaje': 'Pelicula no encontrada'}), 404


def eliminar_pelicula(id: int) -> Union[Response, None]:
    """
    Elimina una película de la lista por su ID.

    :param id: ID de la película a eliminar.
    :return: Respuesta JSON indicando si la película fue eliminada
             o si no se encontró.
    """
    # Lógica para buscar la película por su ID y eliminarla
    for p in peliculas:
        if p['id'] == id:
            peliculas.remove(p)
            return jsonify({'mensaje': 'Película eliminada correctamente'})
    return jsonify({'mensaje': 'Pelicula no encontrada'}), 404


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


def pelicula_por_genero(genero: str) -> Union[Response, None]:
    """
    Devuelve una lista de películas que coincidan con el género especificado.

    :param genero: Género de las películas a buscar.
    :return: Respuesta JSON con la lista de películas del género.
    """
    list_gen = []
    for p in peliculas:
        if p['genero'] == genero:
            list_gen.append(p)
    return jsonify(list_gen)


def pelicula_por_titulo(titulo: str) -> Union[Response, None]:
    """
    Devuelve una lista de películas que coincidan con el título especificado.

    :param titulo: Título de las películas a buscar.
    :return: Respuesta JSON con la lista de películas que coincidan
             con el título.
    """
    list_tit = []
    for p in peliculas:
        if p['titulo'] == titulo:
            list_tit.append(p)
    return jsonify(list_tit)


def pelicula_aleatoria() -> Union[Response, None]:
    """
    Devuelve una película aleatoria de la lista.

    :return: Respuesta JSON con los detalles de una película aleatoria,
             o un mensaje de error si no hay películas disponibles.
    """
    if len(peliculas) > 0:
        pelicula = random.choice(peliculas)
        return jsonify(pelicula)
    else:
        return jsonify({'mensaje': 'No hay peliculas disponibles'}), 404


def pelicula_aleatoria_segun_genero(genero: str) -> Union[Response, None]:
    """
    Devuelve una película aleatoria de un género específico.

    :param genero: Género de la película a buscar.
    :return: Respuesta JSON con los detalles de una película aleatoria
            del género, o un mensaje de error si no hay películas disponibles.
    """
    list_gen = []
    for p in peliculas:
        if p['genero'] == genero:
            list_gen.append(p)
    if len(list_gen) > 0:
        pelicula = random.choice(list_gen)
        return jsonify(pelicula)
    else:
        return jsonify({'mensaje': 'No hay peliculas disponibles'
                        'de ese genero'}), 404


def sugerir_pelicula_por_feriado_y_genero(genero: str) -> Union[Response, None]:
    """
    Sugiere una película de un género específico para el próximo feriado.

    :param genero: Género de la película a sugerir.
    :return: Respuesta JSON con los detalles del próximo feriado y la
             película sugerida, o un mensaje de error si no hay películas
             disponibles o no se encuentra un feriado.
    """
    # Crea una instancia de NextHoliday y carga los feriados
    proximo_feriado = NextHoliday()
    proximo_feriado.fetch_holidays()  # formato json

    # Verifica si se encontró un próximo feriado
    if not proximo_feriado.holiday:
        return jsonify({'mensaje': 'No se pudo obtener información del'
                        'próximo feriado'}), 404

    # armo lista de peliculas respecto al genero dado
    peliculas_por_genero = []
    for p in peliculas:
        if p['genero'] == genero:
            peliculas_por_genero.append(p)

    if peliculas_por_genero:
        # Selecciona una película aleatoria del género solicitado
        pelicula_sugerida = random.choice(peliculas_por_genero)
        return jsonify({
            'feriado': {
                'fecha': f"{proximo_feriado.holiday['dia']}/"
                         f"{proximo_feriado.holiday['mes']}/"
                         f"{proximo_feriado.year}",
                'motivo': proximo_feriado.holiday['motivo']
            },
            'recomendacion': {
                'genero': genero,
                'pelicula': pelicula_sugerida
            }
        })
    else:
        return jsonify({
            'feriado': {
                'fecha': f"{proximo_feriado.holiday['dia']}/"
                         f"{proximo_feriado.holiday['mes']}/"
                         f"{proximo_feriado.year}",
                'motivo': proximo_feriado.holiday['motivo']
            },
            'mensaje': f'No hay películas disponibles del género {genero}'
            }), 404


app.add_url_rule('/peliculas', 'obtener_peliculas',
                 obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula',
                 obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula',
                 agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula',
                 actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula',
                 eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/aleatoria', 'pelicula_aleatoria',
                 pelicula_aleatoria, methods=['GET'])
app.add_url_rule('/peliculas/aleatoria/<string:genero>',
                 'pelicula_aleatoria_segun_genero',
                 pelicula_aleatoria_segun_genero, methods=['GET'])
app.add_url_rule('/peliculas/por_titulo/<string:titulo>',
                 'pelicula_por_titulo',
                 pelicula_por_titulo, methods=['GET'])
app.add_url_rule('/peliculas/por_genero/<string:genero>',
                 'pelicula_por_genero',
                 pelicula_por_genero, methods=['GET'])
app.add_url_rule('/peliculas/sugerencia_feriado/<string:genero>',
                 'sugerir_pelicula_por_feriado_y_genero',
                 sugerir_pelicula_por_feriado_y_genero, methods=['GET'])

if __name__ == '__main__':
    app.run()
