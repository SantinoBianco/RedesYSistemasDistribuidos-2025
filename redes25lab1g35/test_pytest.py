import requests
import pytest
import requests_mock


@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/peliculas', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201,
               json={'id': 3, 'titulo': 'Pelicula de prueba',
                     'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película
        # específica
        m.get('http://localhost:5000/peliculas/1',
              json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200,
              json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        # Simulamos la respuesta para obtener las películas por género
        m.get('http://localhost:5000/peliculas/por_genero/Acción', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para obtener las películas por título
        m.get('http://localhost:5000/peliculas/por_titulo/Indiana%20Jones',
              json=[{'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'}])

        # Simulamos la respuesta para obtener una película aleatoria
        m.get('http://localhost:5000/peliculas/aleatoria',
              json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener una película aleatoria por género
        m.get('http://localhost:5000/peliculas/aleatoria/Acción',
              json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener el próximo feriado
        m.get('https://nolaborables.com.ar/api/v2/feriados/2025', json=[{
            'dia': 1,
            'mes': 5,
            'year': 2025,
            'motivo': 'Día del Trabajo',
            'tipo': 'inamovible'
        }])

        # Simulamos la respuesta para sugerir película por feriado y género
        m.get(
            'http://localhost:5000/peliculas/sugerencia_feriado/Acción',
            json={
                'feriado': {
                    'fecha': '01/05/2025',
                    'motivo': 'Día del Trabajo'
                },
                'recomendacion': {
                    'genero': 'Acción',
                    'pelicula': {
                        'id': 1,
                        'titulo': 'Indiana Jones',
                        'genero': 'Acción'
                    }
                }
            }
        )

        yield m


def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/peliculas')
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas',
                             json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3


def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'


def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1',
                            json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'


def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200


def test_pelicula_por_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/'
                            'por_genero/Acción')
    assert response.status_code == 200
    assert all(p['genero'] == 'Acción' for p in response.json())


def test_pelicula_por_titulo(mock_response):
    response = requests.get('http://localhost:5000/peliculas/'
                            'por_titulo/Indiana%20Jones')
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['titulo']


def test_pelicula_aleatoria(mock_response):
    response = requests.get('http://localhost:5000/peliculas/aleatoria')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'


def test_pelicula_aleatoria_por_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/aleatoria/Acción')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'


def test_sugerir_pelicula_por_feriado_y_genero(mock_response):
    response = requests.get('http://localhost:5000/peliculas/'
                            'sugerencia_feriado/Acción')
    assert response.status_code == 200
    assert response.json()['feriado']['fecha'] == '01/05/2025'
    assert response.json()['feriado']['motivo'] == 'Día del Trabajo'
    assert response.json()['recomendacion']['genero'] == 'Acción'
    assert response.json()['recomendacion']['pelicula']['titulo'] == \
        'Indiana Jones'