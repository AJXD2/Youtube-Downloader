from flet_route import path
from views.index_view import IndexView
from views.recent_view import RecentView
from views.download_view import DownloadView
from views.search_view import SearchView

app_routes = [
    path(url="/", clear=True, view=IndexView),
    path(url="/recent", clear=True, view=RecentView),
    path(url="/search", clear=True, view=SearchView),
    path(url="/download", clear=True, view=DownloadView),
]
