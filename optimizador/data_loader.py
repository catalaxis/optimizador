import pandas as pd

class DataLoader:
    ## Buscamos: ['Ta1', 'Tb1', 'Ta2', 'Tb2', 'TM1', 'TM2', 'Pa', 'Pb']

    ## El CSV debe contener las siguientes columnas:
    REQUIRED_COLUMNS = [    
        'Product_A_Production_Time_Machine_1',
        'Product_A_Production_Time_Machine_2',
        'Product_B_Production_Time_Machine_1',
        'Product_B_Production_Time_Machine_2',
        'Machine_1_Available_Hours',
        'Machine_2_Available_Hours',
        'Price_Product_A',
        'Price_Product_B'
    ]

    def __init__(self, file):
        self.file = file
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(self.file)
        self.validate_data()

    def validate_data(self):
        ## 1.- Checkeamos si el DataFrame está vacío
        if self.df.empty:
            self.df = None
            raise ValueError("CSV file is empty. Please upload a valid CSV file with data.")
        ## 2.- Chequeamos si las columnas requeridas están presentes y si hay columnas inesperadas
        missing_cols = set(self.REQUIRED_COLUMNS) - set(self.df.columns)
        outer_cols = set(self.df.columns) - set(self.REQUIRED_COLUMNS)
        if missing_cols:
            self.df = None
            raise ValueError(f"Missing columns in CSV: {missing_cols}")
        if outer_cols:
            self.df = None
            raise ValueError(f"Unexpected columns in CSV: {outer_cols}. Please ensure the CSV contains only the required columns.")
        ## 3.- Chequeamos si hay valores NaN en el DataFrame
        if self.df.isnull().values.any():
            self.df = None
            raise ValueError("CSV contains NaN values. Please clean the data before uploading.")
        ## 4.- Chequeamos si las columnas requeridas son numéricas
        for col in self.REQUIRED_COLUMNS:
            if not pd.api.types.is_numeric_dtype(self.df[col]):
                self.df = None
                raise ValueError(f"Column '{col}' must be numeric. Please check the data types in the CSV file.")
        ## 5.- Chequeamos si hay valores cero o negativos en las columnas requeridas
        if (self.df[self.REQUIRED_COLUMNS] <= 0).any().any():
            self.df = None
            raise ValueError("CSV contains zero or negative values. All values must be positive.")

    def get_data(self):
        if self.df is None:
            raise ValueError("Data not loaded or invalid. Please load a valid CSV file first.")
        
        ## Finalmente cambiamos los nombres de las columnas a los nombres esperados por el optimizador
        self.df.rename(columns={
            'Product_A_Production_Time_Machine_1': 'Ta1',
            'Product_A_Production_Time_Machine_2': 'Ta2',
            'Product_B_Production_Time_Machine_1': 'Tb1',
            'Product_B_Production_Time_Machine_2': 'Tb2',
            'Machine_1_Available_Hours': 'TM1',
            'Machine_2_Available_Hours': 'TM2',
            'Price_Product_A': 'Pa',
            'Price_Product_B': 'Pb'
        }, inplace=True)

        return self.df.iloc[0].to_dict()

class DataChecker():
    ## Utilizado para validar los datos de entrada del usuario
    REQUIRED_COLUMNS = ['Ta1', 'Tb1', 'Ta2', 'Tb2', 'TM1', 'TM2', 'Pa', 'Pb']

    def __init__(self, data):
        self.data = data

    def validate(self):
        if not isinstance(self.data, dict):
            raise ValueError("Input data must be a dictionary.")
        
        for key in self.REQUIRED_COLUMNS:
            if key not in self.data:
                raise ValueError(f"Missing required field: {key}")
            if not isinstance(self.data[key], (int, float)):
                raise ValueError(f"Field '{key}' must be a number.")
            if self.data[key] <= 0:
                raise ValueError(f"Field '{key}' must be greater than zero.")
        
        return True
