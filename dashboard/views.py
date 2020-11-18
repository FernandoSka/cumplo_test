from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import (
    TemplateView,
    FormView,
)
from .forms import DateForm

import requests


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

    #def form_valid(self, form):
    #    return render_to_string(self.return_template, self.get_return_context(form))


class GetUDIS(BanxicoView):
    """
        Vista para ver los datos de UDIS de banxico
    """
    series = ("SP68257",)
    
    def get_return_context(self, form):
        """
            metodo para ordenar y dar formato flotante a los datos numericos

            returns: diccionario con los datos ordenados
                min: valor minimo
                max: valor maximo
                avg: promedio del valor del dolar
                data: datos ordenados por fecha
                    fecha: fecha en formato aaaa/mm/dd
                    dato: cantidad flotante
        """
        data = super().get_return_context(form)
        ordered_data = []
        for serie in data["bmx"]["series"]:
            if serie["idSerie"] == "SP68257":
                ordered_data = [{
                    "fecha": x["fecha"],
                    "dato": float(x["dato"])
                } for x in serie["datos"]]
        try:
            avg = sum([x["dato"] for x in ordered_data]) / float(len(ordered_data))
        except ZeroDivisionError as e:
            avg = 0
        
        return_data = {
            "data": ordered_data,
            "max": max([x["dato"] for x in ordered_data]),
            "min": min([x["dato"] for x in ordered_data]),
            "avg": avg,
        }
        return return_data


class GetDolar(BanxicoView):
    """
        Vista para ver los datos del valor del dolar de banxico
    """
    series = ("SF43718",)
    
    def get_return_context(self, form):
        """
            metodo para ordenar y dar formato flotante a los datos numericos

            returns: diccionario con los datos ordenados
                min: valor minimo
                max: valor maximo
                avg: promedio del valor del dolar
                data: diccionario de datos ordenados por fecha
                    fecha: fecha en formato aaaa/mm/dd
                    dato: cantidad flotante
        """

        data = super().get_return_context(form)
        ordered_data = []
        for serie in data["bmx"]["series"]:
            if serie["idSerie"] == "SF43718":
                ordered_data = [{
                    "fecha": x["fecha"],
                    "dato": float(x["dato"])
                } for x in serie["datos"]]
        try:
            avg = sum([x["dato"] for x in ordered_data]) / float(len(ordered_data))
        except ZeroDivisionError as e:
            avg = 0
        
        return_data = {
            "data": ordered_data,
            "max": max([x["dato"] for x in ordered_data]),
            "min": min([x["dato"] for x in ordered_data]),
            "avg": avg,
        }
        return return_data


class GetTIIE(BanxicoView):
    """
        Vista para ver los datos del valor del TIIE
    """
    series = ("SF61745", "SF331451", "SF43783", "SF43878", "SF111916")

    def get_return_context(self, form):
        """
            metodo para ordenar y dar formato flotante a los datos numericos

            returns: diccionario con los datos ordenados de los valores del TIIE
                idSerie: id de serie de banxico
                titulo: nombre del encabezado
                datos: diccionario de datos ordenados por fecha
                    fecha: fecha en formato aaaa/mm/dd
                    dato: cantidad flotante
        """
        data = super().get_return_context(form)
        ordered_data = [{
            "idSerie":serie["idSerie"],
            "titulo":serie["titulo"],
            "datos": [{
                "fecha": x["fecha"],
                "dato": float(x["dato"])
            } for x in serie["datos"]]
        } for serie in data["bmx"]["series"]]
        for serie in data["bmx"]["series"]:
            if serie["idSerie"] == "SF43718":
                ordered_data = [{
                    "fecha": x["fecha"],
                    "dato": float(x["dato"])
                } for x in serie["datos"]]
        ordered_data.sort(key=lambda k:k["idSerie"], reverse=True)
        return_data = {
            "data": ordered_data,
        }
        return return_data

class HomeView(TemplateView):
    """
        Pagina principal
    """
    template_name = "home.html"
