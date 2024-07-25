import seaborn as sns
import matplotlib.pyplot as plt
from shiny import App, render, ui
from posit import connect
from pins import board_connect

client = connect.Client()

board = board_connect()
iris = board.pin_read(f"{client.me.username}/iris_dataset")

app_ui = ui.page_fluid(
    ui.input_select("x_var", "X-axis variable", choices=list(iris.columns[:-1]), selected=iris.columns[0]),
    ui.input_select("y_var", "Y-axis variable", choices=list(iris.columns[:-1]), selected=iris.columns[1]),
    ui.output_plot("iris_plot")
)

def server(input, output, session):
    @output
    @render.plot
    def iris_plot():
        # Create the plot
        fig, ax = plt.subplots()
        sns.scatterplot(data=iris, x=input.x_var(), y=input.y_var(), hue="species", ax=ax)
        return fig

app = App(app_ui, server)
