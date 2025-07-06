from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from io import TextIOWrapper
from .data_loader import DataLoader, DataChecker
from .optimizer import Optimizer
from .result import ResultsHandler

def index(request):
    context = {}
    if request.method == 'POST':
        # Si viene un archivo CSV
        if 'csv_file' in request.FILES and request.FILES['csv_file']:
            archivo = request.FILES['csv_file']
            # Cargar el CSV usando DataLoader
            data_loader = DataLoader(archivo)
            try:
                data_loader.load_data()
            except ValueError as e:
                context['error'] = f"Error en CSV: {e}"
                return render(request, 'index.html', context)

            # Suponiendo que el CSV tiene columnas: Ta1, Tb1, Ta2, Tb2, TM1, TM2, Pa, Pb
            fila = data_loader.get_data()
            opt = Optimizer(
                **fila # Desempaquetar el diccionario directamente
            )

        # Si viene desde inputs manuales
        else:
            try: 
                data = {
                    'Ta1': float(request.POST['Ta1']),
                    'Tb1': float(request.POST['Tb1']),
                    'Ta2': float(request.POST['Ta2']),
                    'Tb2': float(request.POST['Tb2']),
                    'TM1': float(request.POST['TM1']),
                    'TM2': float(request.POST['TM2']),
                    'Pa': float(request.POST['Pa']),
                    'Pb': float(request.POST['Pb']),
                }
            except (ValueError, KeyError) as e:
                context['error'] = f"Error en los datos ingresados: {e}"
                return render(request, 'optimizador/index.html', context)

            checker = DataChecker(data)  # Usamos DataLoader solo para validación
            try:
                checker.validate()
            except ValueError as e:
                context['error'] = f"Error en los datos ingresados: {e}"
                return render(request, 'optimizador/index.html', context)
            
            opt = Optimizer(**data)

        try:
            Xa, Xb, profit = opt.solve()

            handler = ResultsHandler(Xa, Xb, profit)

            result = handler.to_dict() 
            image = handler.generate_bar_chart_base64()

            return render(request, 'optimizador/resultado.html', 
                          {'resultado': result,
                           'grafico': image})
        except ValueError as e:
            return HttpResponse(f"Error: {str(e)}")

    return render(request, 'optimizador/index.html')