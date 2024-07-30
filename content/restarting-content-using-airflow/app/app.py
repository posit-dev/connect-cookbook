import seaborn as sns
from pins import board_connect
from shiny import App, render, ui

board = board_connect()
# penguins = board.pin_read("taylor_steinberg/penguins")
penguins = sns.load_dataset('penguins')

app_ui = ui.page_fluid(
    ui.page_fluid(
        ui.row(
            ui.column(
                12, ui.output_plot("plot", height="100vh"), style="height: 100vh;"
            )
        )
    )
)


def server(input, output, session):
    @output
    @render.plot
    def plot():
        return sns.pairplot(penguins, hue="species")


app = App(app_ui, server)
