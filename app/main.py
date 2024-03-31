import flet as ft
from flet_route import Routing, Params, Basket
from routes import app_routes
from middlewares.app_middleware import AppBasedMiddleware


def main(page: ft.Page):

    def change_by_index(index: int):
        page.go(app_routes[index][0])

    def on_change(e: ft.ControlEvent):
        # print(e.data)
        # page.go("test")
        change_by_index(int(e.data))

    page.title = "Youtube Downloader"
    page.window_height = 600
    page.window_width = 600
    page.window_resizable = False
    page.window_min_height = 600
    page.window_min_width = 600
    page.window_max_height = 600
    page.window_max_width = 600
    page.window_always_on_top = False

    navbar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(
                label="Home",
                icon=ft.icons.HOME_OUTLINED,
                selected_icon=ft.icons.HOME_ROUNDED,
            ),
            ft.NavigationDestination(
                label="Recents",
                icon=ft.icons.HISTORY_OUTLINED,
                selected_icon=ft.icons.HISTORY_ROUNDED,
            ),
            ft.NavigationDestination(
                label="Search",
                icon=ft.icons.SEARCH_OUTLINED,
                selected_icon=ft.icons.SEARCH_ROUNDED,
            ),
        ],
        on_change=on_change,
    )

    def test(page: ft.Page, params: Params, basket: Basket):

        return ft.View(
            "/test",
            controls=[
                ft.Text("Not Found"),
                ft.ElevatedButton("Go Home", on_click=lambda e: change_by_index(0)),
            ],
        )

    rt = Routing(
        page=page,
        app_routes=app_routes,
        navigation_bar=navbar,
        not_found_view=test,
    )

    page.go(page.route)


ft.app(target=main, assets_dir="assets")
