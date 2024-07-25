import seaborn as sns
from shiny import App, render, ui
from pins import board_connect


board = board_connect()
iris = board.pin_read("taylor_steinberg/iris_dataset")

app_ui = ui.page_fluid(
    ui.page_fluid(
        ui.row(
            ui.column(
                12, ui.output_plot("pairplot", height="100vh"), style="height: 100vh;"
            )
        )
    )
)


def server(input, output, session):
    @output
    @render.plot
    def pairplot():
        return sns.pairplot(iris, hue="species", markers=["o", "s", "D"])


app = App(app_ui, server)
