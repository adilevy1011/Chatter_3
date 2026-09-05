import flet as ft

def build_main_view(page: ft.Page) -> ft.View:
    page.title = "Chatter"
    page.window.icon = "chatter-icon2.ico"
    text = ft.Text('welcome')
    # rail = ft.NavigationRail(
    #     selected_index=0,
    #     label_type=ft.NavigationRailLabelType.ALL,
    #     min_width=100,
    #     min_extended_width=400,
    #     destinations=[
    #     ft.NavigationRailDestination(
    #         icon=ft.Icons.HOME_OUTLINED,
    #         selected_icon=ft.Icons.HOME,
    #         label="Home",
    #     ),],
    #     on_change=lambda e: print(f"Selected destination: {e.control.selected_index}"),

    # )

    return ft.View(
        route="/",
        controls=[
            text
            #rail
        ],
    )

