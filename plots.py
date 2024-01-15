import pandas as pd
import glob
import numpy as np

def round_half_up_average_csv(input_folder, output_csv_file):
    
    csv_files = glob.glob(input_folder + '/*.csv')

    first_df = pd.read_csv(csv_files[0])
    result_df = pd.DataFrame(columns=first_df.columns)

    num_files = len(csv_files)

    # Leer y sumar los datos de cada archivo CSV
    for file in csv_files:
        df = pd.read_csv(file)
        result_df = result_df.add(df, fill_value=0)

    # Promediar los valores sumados
    result_df = result_df / num_files

    # Redondear todos los valores 
    result_df = result_df.applymap(lambda x: np.ceil(x) if x - int(x) >= 0.2 else np.floor(x))

    result_df.to_csv(output_csv_file, index=False)

input_folder = 'resultados'
output_csv_file = 'simulaciones.csv'
round_half_up_average_csv(input_folder, output_csv_file)
