"""Welcome to Reflex! This file outlines the steps to create a basic app."""

from rxconfig import config

import reflex as rx

docs_url = "https://reflex.dev/docs/getting-started/introduction/"
filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The app state."""


def index() -> rx.Component:
    return rx.center(
        
        rx.vstack(
            rx.image(src='/Wlogo.png', width="200px"),
            rx.heading("Bienvenido a WikiMath!", size="9"),
            rx.text("Una herramienta para empezar con las Matematicas"),
            rx.button(
                "Inicia sesión",
                on_click=lambda: rx.redirect('/login'),
                size="4",
            ),
            align="center",
            spacing="7",
            font_size="2em",
        ),
        height="100vh",
    )


app = rx.App()
app.add_page(index)