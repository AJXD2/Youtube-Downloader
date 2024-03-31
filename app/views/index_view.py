from pathlib import Path
import flet as ft
from flet_route import Params, Basket
from pytube import YouTube, exceptions
from components.video_card import VideoCard

BASE = Path(__file__).resolve().parent
USER_DIR = Path.home().joinpath("Downloads")


def set_defaults(basket: Basket):
    basket.destination = USER_DIR
    basket.format = "video"
    basket.url = ""


def IndexView(page: ft.Page, params: Params, basket: Basket):
    if not (basket.get("destination") or basket.get("format")):
        set_defaults(basket)

    def on_url_change(e: ft.ControlEvent):
        global preview
        try:
            vid = YouTube(e.data)
            preview = VideoCard(vid)
        except exceptions.RegexMatchError as e:
            return

    def clear(e):
        basket.delete("destination")
        basket.delete("format")
        basket.delete("url")

        destination_text.value = Path.home().joinpath("Downloads")
        video_field.value = ""
        destination_text.update()
        video_field.update()

    def download(e: ft.ControlEvent = None):

        basket.url = str(video_field.value).strip()
        basket.destination = Path(destination_text.value).resolve()
        basket.format = str(dropdown.value).strip()

        video_field.error_text = ""
        destination_text.error_text = ""
        dropdown.error_text = ""
        if not basket.get("url"):
            video_field.error_text = "Enter a URL"
        if not basket.get("destination"):
            destination_text.error_text = "Enter a destination"
        if not basket.get("format"):
            dropdown.error_text = "Select a format"
        page.update()

        if basket.get("url") and basket.get("destination") and basket.get("format"):
            e.page.go("/download")

    def get_dest(e: ft.FilePickerResultEvent):
        if e.path is None:
            return
        basket.destination = Path(e.path).resolve()

        destination_text.disabled = False
        destination_text.value = str(basket.destination)
        destination_text.disabled = True
        destination_text.update()

    destination_text = ft.TextField(
        disabled=True, value=Path.home().joinpath("Downloads"), expand=True
    )

    video_field = ft.TextField(
        label="Youtube Video URL",
        on_change=on_url_change,
    )
    dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("video", "Video"),
            ft.dropdown.Option("audio", "Just Audio"),
        ],
        value="video",
        label="Select Format",
    )
    preview = ft.Container()
    filepicker = ft.FilePicker(on_result=get_dest)
    form = ft.Container(
        ft.Column(
            [
                filepicker,
                video_field,
                dropdown,
                ft.Row(
                    [
                        destination_text,
                        ft.IconButton(
                            ft.icons.FOLDER_OPEN_OUTLINED,
                            on_click=lambda _: filepicker.get_directory_path(
                                "Pick Destination Folder", USER_DIR
                            ),
                        ),
                    ],
                ),
                preview,
                ft.Row(
                    [
                        ft.ElevatedButton("Download", on_click=download),
                        ft.ElevatedButton("Clear", on_click=clear),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                ),
            ]
        )
    )

    return ft.View("/", controls=[ft.SafeArea(ft.Column(controls=[form]))])
