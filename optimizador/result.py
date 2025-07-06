import io
import base64
import matplotlib.pyplot as plt

class ResultsHandler:
    def __init__(self, Xa, Xb, profit):
        self.Xa = Xa
        self.Xb = Xb
        self.profit = profit

    def to_dict(self):
        return {
            'Xa': round(self.Xa, 2),
            'Xb': round(self.Xb, 2),
            'profit': round(self.profit, 2),
        }

    def to_base64(self):
        result_str = f"Xa: {self.Xa}, Xb: {self.Xb}, Profit: {self.profit}"
        result_bytes = result_str.encode('utf-8')
        return base64.b64encode(result_bytes).decode('utf-8')
    
    def generate_bar_chart_base64(self):
        fig, ax = plt.subplots()
        ax.bar(['Producto A', 'Producto B'], [self.Xa, self.Xb], color=['#4CAF50', '#2196F3'])
        ax.set_ylabel('Unidades a Producir')
        ax.set_title('Producción Óptima por Producto')

        buffer = io.BytesIO()
        plt.tight_layout()
        fig.savefig(buffer, format='png')
        plt.close(fig)
        buffer.seek(0)
        image_png = buffer.getvalue()
        encoded = base64.b64encode(image_png).decode('utf-8')
        buffer.close()
        return encoded
    
    def to_csv(self):
        output = io.StringIO()
        output.write("Xa,Xb,Profit\n")
        output.write(f"{self.Xa},{self.Xb},{self.profit}\n")
        return output.getvalue()
    
    def plot_results(self):
        fig, ax = plt.subplots()
        ax.bar(['Producto A', 'Producto B'], [self.Xa, self.Xb], color=['#4CAF50', '#2196F3'])
        ax.set_ylabel('Unidades a Producir')
        ax.set_title('Producción Óptima por Producto')
        plt.show()