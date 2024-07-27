import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_data(data):
    # Configurar el estilo de los gráficos de Seaborn
    sns.set(style="darkgrid")
    
    # Crear un gráfico de líneas usando los datos proporcionados
    sns.lineplot(x="time", y="value", data=data)
    
    # Mostrar el gráfico
    plt.show()
