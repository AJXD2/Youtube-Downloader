import flet as ft
from flet_route import Params, Basket
from pytube import YouTube, Stream
from pytube.exceptions import AgeRestrictedError
from pathlib import Path
import os
from components.video_card import VideoCard
from threading import Thread

BASE = Path(__file__).resolve().parent


def loading_dots(text: str):
    if text.endswith("..."):
        return "."
    return text + "."


def background_download(stream: Stream, path: Path):
    task = Thread(target=stream.download, args=(path,), daemon=True)

    return task


def DownloadView(page: ft.Page, params: Params, basket: Basket):
    current_video = basket.get("url")

    def progress(stream: Stream, chunk: bytes, bytes_remaining: int):
        total = stream.filesize

        bytes_downloaded = float(total) - float(bytes_remaining)
        percentage = bytes_downloaded / total
        progressbar.value = percentage
        status_text.value = f"{int(percentage * 100)}%"
        button.text = loading_dots(button.text)
        print(percentage)
        page.update()

    def done(stream, file_path):
        status_text.value = "Download Completed"
        progressbar.value = 0
        progressbar.visible = False
        os.system(f"explorer {Path(file_path).resolve().parent}")
        button.text = "Go home"
        button.on_click = lambda e: page.go("/")
        button.disabled = False
        page.update()

    def start_download(e):
        if current_video is None:
            return

        video = YouTube(
            current_video,
            on_progress_callback=progress,
            on_complete_callback=done,
            use_oauth=False,
            allow_oauth_cache=True,
        )
        try:
            button.disabled = True
            button.text = "."
            button.update()
            if basket.get("format") == "video":

                dl_task = background_download(
                    video.streams.get_highest_resolution(),
                    str(basket.get("destination")),
                )

            elif basket.get("format") == "audio":
                dl_task = background_download(
                    video.streams.get_audio_only(),
                    str(basket.get("destination")),
                )
            else:
                dl_task = background_download(
                    video.streams.get_highest_resolution(),
                    str(basket.get("destination")),
                )
            dl_task.start()
            # TODO How to cancel?
        except AgeRestrictedError:
            status_text.value = "Video is age restricted"
            progressbar.value = 0
            progressbar.visible = False
            page.update()

    status_text = ft.Text("Waiting for download to start...")
    progressbar = ft.ProgressBar()
    button = ft.ElevatedButton("Download", on_click=start_download)

    return ft.View(
        "/download",
        controls=[
            ft.SafeArea(
                ft.Column(
                    controls=[
                        VideoCard(current_video),
                        ft.Container(
                            ft.Column(
                                [ft.Row([status_text], alignment="center"), progressbar]
                            ),
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            padding=15,
                            border_radius=15,
                        ),
                        ft.Row([button], alignment="center"),
                    ]
                )
            )
        ],
    )
