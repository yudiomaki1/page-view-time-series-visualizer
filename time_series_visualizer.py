import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019") 
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy() #Cria uma copia do dataframe
    df_bar['year'] = df_bar.index.year   #Cria uma nova coluna de ano
    df_bar['month'] = df_bar.index.month    #Cria uma nova coluna de mês

    df_grouped = df_bar.groupby(["year", "month"])["value"].mean().unstack()  #Agrupa os valores que tem mes e ano coincidente e faz a media usando o .mean()

    # Draw bar plot
    fig = df_grouped.plot(kind='bar', figsize=(10, 7)).figure   #Configurações do grafico

    plt.xlabel('Years')     #Nome do eixo X
    plt.ylabel('Average Page Views')       #Nome do eixo Y
    plt.legend(title="Months", labels=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]) #Legenda do grafico
    plt.tight_layout()      #Evita a sobreposição no layout

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))  # Cria uma figura com dois graficos

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)') #Titulo do grafico
    axes[0].set_xlabel('Year')      #Nome do eixo X
    axes[0].set_ylabel('Page Views')        #Nome do eixo Y

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] #Define a ordem dos meses

    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1], order = month_order)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
