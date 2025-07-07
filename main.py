## Archivo para probar el funcionamiento general sin levantar el servidor
from optimizador.data_loader import DataLoader
from optimizador.optimizer import Optimizer
from optimizador.result import ResultsHandler



def main():
    # Cargar los datos desde el CSV
    def load_optimization_data(file_path):
        data_loader = DataLoader(file_path)
        data_loader.load_data()
        return data_loader.get_data()

    # Ejemplo de uso
    data = load_optimization_data('optimizador/optimization_problem_data.csv')
    optimizer = Optimizer(**data)
    result = optimizer.solve()
    print("Resultados de la optimización, a partir de los datos ejemplo:")
    print(f"Solución óptima de producción: Producto A = {round(result[0], 2)}, Producto B = {round(result[1], 2)}")
    print(f"Beneficio máximo: {round(result[2], 2)}")

if __name__ == "__main__":
    main()