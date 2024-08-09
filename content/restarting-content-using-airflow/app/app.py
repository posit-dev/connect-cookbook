import pandas as pd
from pins import board_connect
from shiny.express import input, render, ui

board = board_connect(allow_pickle_read=True)
encoder = board.pin_read("taylor_steinberg/encoder")
pipeline = board.pin_read("taylor_steinberg/pipeline")

def get_penguin() -> str:
    bill_length_mm = float(input.bill_length_mm())
    bill_depth_mm = float(input.bill_depth_mm())
    flipper_length_mm = float(input.flipper_length_mm())
    body_mass_g = float(input.body_mass_g())
    df = pd.DataFrame(
        [[bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g]],
        columns=[
            "bill_length_mm",
            "bill_depth_mm",
            "flipper_length_mm",
            "body_mass_g",
        ],
    )
    species = pipeline.predict(df)
    species = encoder.inverse_transform(species)
    return str(species[0])

with ui.layout_sidebar(height="100%"):
    with ui.sidebar():
        ui.input_slider("bill_length_mm", "Bill Length (mm)", 25, 65, value=45),
        ui.input_slider("bill_depth_mm", "Bill Depth (mm)", 10, 25, value=17),
        ui.input_slider(
            "flipper_length_mm", "Flipper Length (mm)", 160, 240, value=200
        ),
        ui.input_slider("body_mass_g", "Body Mass (g)", 2500, 6500, value=4000),

    @render.text
    def text():
        penguin = get_penguin()
        return f"I think this is a {penguin} penguin."

    @render.image
    def f():
        penguin = get_penguin()
        img = {
            "src": f"./{penguin.lower()}.png",
            "height": "100%",
        }
        return img
