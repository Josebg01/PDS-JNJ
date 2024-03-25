import reflex as rx
import requests as rq

class LoginState(rx.State):
    loader: bool = False
    username: str = "user"
    password: str 
    error = False
    response: dict={}
    session = {}
    
    @rx.background
    async def local_login(self, data: dict):
        async with self:  
            username = data.get('username')
            password = data.get('password')
            if username == 'jose' and password == '1234':
                self.error = False  
                self.session['logged_in'] = True  
                return rx.redirect('/')
            else:
                self.error = True  
                return None

    @rx.var
    def user_empty(self)->bool:
        return not self.username.strip()

    @rx.var
    def password_empty(self)->bool:
        return not self.password.strip()
    
    @rx.var
    def validate_fields(self)->bool:
        return (
            self.user_empty
            or self.password_empty
        )

    
        


@rx.page(route="/login", title= "login")
def login() ->rx.Component:
    return rx.section(
        rx.flex(
            rx.heading("Inicio de sesión"),
            rx.form.root(
                rx.flex(
                    field_form_component_general("Usuario", "Ingrese su usuario", "Ingrese un usuario valido", "username",
                                                    LoginState.set_username),   
                    field_form_component("Contraseña", "Ingrese su contraseña", "password", 
                                                    LoginState.set_password, "password"),                                            
                    rx.form.submit(
                        rx.cond(
                            LoginState.loader,
                            rx.chakra.spinner(color="red",size="xs" ),
                            rx.button(
                                "Iniciar sesión",
                                disabled=LoginState.validate_fields,
                                width="30vw"
                            ),
                        ),
                        as_child=True,
                    ),
                    justify= "center",
                    spacing="2",
                    direction="column",
                    align="center",
                ),
                    rx.cond(
                        LoginState.error,
                        rx.callout(
                            "Credenciales incorrectas",
                            icon="alert_triangle",
                            color_scheme="red",
                            role="alert",
                            style={"margin_top": "10px"} 
                        ),
                    ),
                    on_submit=LoginState.local_login,
                    reset_on_submit=True,
                    width="80%",
            ),
            justify= "center",
            width="100%",
            direction="column",
            align="center",
        ),
        style=style_section,
        justify= "center",
        width="100%",
    )

def field_form_component(label:str, placeholder: str, name_var: str,
                        on_change_function, type_field:str) -> rx.Component:
    return rx.form.field(
                rx.flex(
                    rx.form.label(label),
                    rx.form.control(
                        rx.input.input(
                            placeholder=placeholder,
                            on_change=on_change_function,
                            name=name_var,
                            type=type_field,
                            required=True
                        ),
                        as_child=True,
                ),
                rx.form.message(
                        "El campo no puede ser nulo",
                        match="valueMissing",
                        color="red",
                ),
                direction="column",
                spacing="2",
                align="stretch",
                ),
                name=name_var,
                width="30vw"
            )






def field_form_component_general(label: str, placeholder: str, message_validate: str, name: str,
                        on_change_function ) ->  rx.Component:
    return rx.form.field(
                rx.flex(
                    rx.form.label(label),
                    rx.form.control(
                    rx.input.input(
                        placeholder=placeholder,
                        on_change=on_change_function,
                        name=name,
                        required=True
                    ),
                    as_child=True    
                    ),
                    rx.form.message(
                        message_validate,
                        name=name,
                        match="valueMissing",
                        
                        color="red"
                    ),
                direction="column",
                spacing="2",
                align="stretch",
                ),
                name=name,
                width="30vw"
    )


style_section={
    "height": "90vh",
    "width": "80%",
    "margin": "auto",
}