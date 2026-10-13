import requests
from datetime import date


def get_url(year):
    """
    Genera la URL para obtener los feriados de un año específico.

    :param year: Año para el cual se desea obtener los feriados.
    :return: URL como cadena de texto.
    """
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"


months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
          'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado',
        'Domingo']


def day_of_week(day, month, year):
    return days[date(year, month, day).weekday()]


class NextHoliday:
    """
    Clase para manejar la búsqueda del próximo feriado.

    Permite filtrar feriados por tipo y obtener información del próximo
    feriado disponible.
    """
    def __init__(self, holiday_type=None):
        """
        Inicializa la clase NextHoliday.

        :param holiday_type: Tipo de feriado a buscar (inamovible, trasladable,
                             nolaborable, puente) o None para buscar sin filtro
        """
        self.loading = True
        self.year = date.today().year
        self.holiday = None
        self.holiday_type = holiday_type

    def holiday_by_type(self, holidays):
        """
        Filtra los feriados por tipo.

        :param holidays: Lista de feriados.
        :return: Lista de feriados filtrados por tipo.
        """
        if self.holiday_type:
            filtered_list = []
            for h in holidays:
                if h['tipo'] == self.holiday_type:
                    filtered_list.append(h)
            return filtered_list
        return holidays

    def set_next(self, holidays):
        """
        Establece el próximo feriado basado en la fecha actual.

        :param holidays: Lista de feriados.
        """
        now = date.today()
        today = {
            'day': now.day,
            'month': now.month
        }

        filtered_holidays = self.holiday_by_type(holidays)

        if not filtered_holidays:
            self.holiday = None
        else:
            holiday = next(
                          (h for h in filtered_holidays if
                           h['mes'] == today['month'] and
                           h['dia'] > today['day'] or
                           h['mes'] > today['month']),
                          filtered_holidays[0]
                          )

            self.loading = False
            self.holiday = holiday

    def fetch_holidays(self):
        """
        Obtiene los feriados desde la API y establece el próximo feriado.
        """
        response = requests.get(get_url(self.year))
        data = response.json()
        self.set_next(data)

    def render(self):
        """
        Muestra información del próximo feriado en la consola.
        """
        if self.loading:
            print("Buscando...")
        elif self.holiday is None:
            print("No hay feriados de ese tipo")
        else:
            print("Próximo feriado")
            print(self.holiday['motivo'])
            print("Fecha:")
            print(day_of_week(self.holiday['dia'], self.holiday['mes'],
                              self.year))
            print(self.holiday['dia'])
            print(months[self.holiday['mes'] - 1])
            print("Tipo:")
            print(self.holiday['tipo'])


if __name__ == "__main__":
    holiday_type = input("Ingrese el tipo de feriado que desea buscar "
                         "(inamovible, trasladable, nolaborable o puente)"
                         " o presione Enter para buscar sin filtro: "
                         ).strip().lower() or None

    next_holiday = NextHoliday(holiday_type)

    next_holiday.fetch_holidays()
    next_holiday.render()