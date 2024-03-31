import flet as ft
from flet_route import Params, Basket


def RecentView(page: ft.Page, params: Params, basket: Basket):
    basket.test1 = "test1"
    basket.test2 = "test2"
    basket.test3 = "test3"

    return ft.View(
        "/recent",
        controls=[
            ft.SafeArea(
                ft.Column(
                    controls=[
                        ft.Text(
                            "You overestimated me if you though i would make this lmao"
                        ),
                    ]
                )
            )
        ],
        navigation_bar=None,
    )
