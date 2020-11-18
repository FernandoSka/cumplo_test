# cumplo_test

 Proyecto de prueba para la aplicacion de cumplo

instalacion:
clonar el repositorio y entrar a la carpeta, luego instalar dependencias
```
pip install -r requirements.txt
python manage.py runserver
```

## Uso de la Vista personalizada de banxico
```
class BanxicoView(FormView):
    """
    Vista base para todos los recursos utilizados para los recursos de banxico
    Pensado para su consumo por ajax
    variables de clase:
        - series(tupla): lista o tupla de las series que se van a consultar

    metodos de clase:
        - get_request: hace un get request a la pagina de banxico y regresa un JSON
        - get_series: prepara el formato de la url hacia banxico y regresa un JSON
        - get_return_context: sirve para acomodar la data a nuestra conveniencia y regresa un JSON
        - form_valid: prepara la respuesta final del JSON
    """
    template_name = "range_form.html"
    form_class = DateForm
    base_url_banxico = "https://www.banxico.org.mx/"
    series = None

    def get_request(self, url, params=None):
        """
            Funcion para hacer un request hacia la pagina de banxico

            Parametros:
                -url(str) : url a consultar
                -params: parametros extra
            Returns:
                JSON: Respuesta de la app de banxico
        """
        headers = {'Bmx-Token': 'e546043c0f858d0a85dfe786337fa83c295788050ff762d74dc96e3a16dd9602'}
        x = requests.get(url, params=params, headers=headers)
        return(x.json())
    
    def get_series(self, gte, lte):
        """
            Funcion para dar formato a una url

            Parametros:
                -gte(str) : fecha inicial (aaaa-mm-dd)
                -lte(str): fecha final (aaaa-mm-dd)
            Returns:
                JSON: Respuesta de la app de banxico
        """
        series_str = ""
        series_str = ','.join(map(str, self.series)) 
        url = self.base_url_banxico + "SieAPIRest/service/v1/series/{series}/datos/{gte}/{lte}".format(
            series=series_str,
            gte=gte,
            lte=lte
        )
        return self.get_request(url)

    def get_return_context(self, form):
        """
            Funcion para preparar el contexto a regresar

            Parametros:
                -form(form) : formulario valido
            Returns:
                JSON: Respuesta de la app de banxico
        """
        return self.get_series(form.cleaned_data["gte"], form.cleaned_data["lte"])

    def form_valid(self, form):
        """
            Funcion para regresar JSON por defecto

            Parametros:
                -form(form) : formulario valido
            Returns:
                JSON: Respuesta de la app de banxico
        """
        return JsonResponse(self.get_return_context(form))
```
Clase personalizada
```
class ExampleView(BanxicoView):
    """
        Vista para ver los datos de alguna serie de banxico
    """
    series = ("EXAMPLE_SERIE1", "EXAMPLE_SERIE2")
```
