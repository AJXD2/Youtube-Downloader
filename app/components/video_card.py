import flet as ft
from pytube import YouTube, Channel
from datetime import datetime

from numerize.numerize import numerize


def format_time_ago(dt):
    now = datetime.now()
    time_difference = now - dt

    if time_difference.days < 0:
        return "in the future"

    if time_difference.days == 0:
        if time_difference.seconds < 60:
            return "just now"
        elif time_difference.seconds < 3600:
            minutes = time_difference.seconds // 60
            return f"{minutes} minutes ago"
        else:
            hours = time_difference.seconds // 3600
            return f"{hours} hours ago"

    if time_difference.days == 1:
        return "yesterday"

    if time_difference.days < 7:
        return f"{time_difference.days} days ago"

    weeks = time_difference.days // 7
    if weeks < 4:
        return f"{weeks} weeks ago"

    months = time_difference.days // 30
    if months < 12:
        return f"{months} months ago"

    years = time_difference.days // 365
    return f"{years} years ago"


def truncate_text(text, max_length):
    if len(text) > max_length:
        return text[: max_length - 3] + "..."
    else:
        return text


class VideoCard(ft.UserControl):

    def __init__(self, url: str | YouTube, following: ft.Control = None):
        super().__init__()
        if isinstance(url, YouTube):
            self.video = url
        else:
            self.video = YouTube(url)

        self.following = following if following is not None else ft.Container()

    def build(self):

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.Image(
                                            src=self.video.thumbnail_url,
                                            width=150,
                                            height=100,
                                        ),
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    truncate_text(self.video.title, 50)
                                                ),
                                                ft.Text(self.video.author),
                                                ft.Text(
                                                    f"{numerize(self.video.views)} views • {format_time_ago(self.video.publish_date)}"
                                                ),
                                            ]
                                        ),
                                    ]
                                ),
                                ft.Container(
                                    self.following,
                                    padding=ft.Padding(
                                        10,
                                        0,
                                        0,
                                        0,
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        )
                    ]
                ),
                padding=10,
                bgcolor="#0f0f0f",
                border_radius=10,
            ),
        )
