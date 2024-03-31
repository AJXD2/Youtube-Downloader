from tkinter import Y
import flet as ft
from flet_route import Params, Basket
import pytube
from components.video_card import VideoCard


def SearchView(page: ft.Page, params: Params, basket: Basket):

    ref_query = ft.Ref[ft.TextField]()
    ref_submit = ft.Ref[ft.IconButton]()
    ref_vidlist = ft.Ref[ft.Column]()
    ref_info = ft.Ref[ft.Row]()

    def close_dialog(e: ft.ControlEvent):
        page.dialog.open = False

        page.update()

    page.dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row([ft.Icon(ft.icons.WARNING_OUTLINED), ft.Text("WARNING")]),
        content=ft.Text(
            "This feature is still in development. It will probably not work lol"
        ),
        actions=[
            ft.TextButton(
                "I fully accept that if i continue i may explode", on_click=close_dialog
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        open=True,
    )

    def search(e: ft.ControlEvent):
        query = ref_query.current.value
        print(query)
        if not query:
            print("Nort query")
            ref_vidlist.current.controls = []
            ref_vidlist.current.visible = False
            ref_info.current.controls = [
                ft.Icon(ft.icons.INFO_OUTLINED),
                ft.Text("Please enter a search query."),
            ]
            ref_info.current.visible = True
            page.update()
            return
        print("Yes query")
        ref_vidlist.current.visible = True
        ref_info.current.visible = False
        ref_vidlist.current.controls = []

        def download(url: str | pytube.YouTube):

            basket.url = url if isinstance(url, str) else url.watch_url

            page.go("/download")

        e.page.update()
        s = pytube.Search(query)
        for v in s.results:
            print(f"Processing {v}")
            download_button = ft.IconButton(
                icon=ft.icons.DOWNLOAD,
                on_click=lambda e: download(v),
            )
            card = VideoCard(v, following=download_button)

            ref_vidlist.current.controls.append(card)
        ref_info.current.controls = [
            ft.Icon(ft.icons.INFO_OUTLINED),
            ft.Text("Please enter a search query."),
        ]
        ref_info.current.visible = False
        e.page.update()

    return ft.View(
        "/search",
        controls=[
            ft.SafeArea(
                ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.TextField(
                                    ref=ref_query,
                                    label="Search:",
                                    expand=True,
                                    on_submit=search,
                                ),
                                ft.IconButton(
                                    ref=ref_submit,
                                    icon=ft.icons.SEARCH,
                                    on_click=search,
                                ),
                            ]
                        ),
                        ft.Column(
                            ref=ref_vidlist,
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            visible=False,
                        ),
                        ft.Row(
                            ref=ref_info,
                            controls=[
                                ft.Icon(ft.icons.INFO_OUTLINED),
                                ft.Text("Use the search bar to search for a video."),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    expand=True,
                ),
                expand=True,
            )
        ],
        navigation_bar=None,
    )
