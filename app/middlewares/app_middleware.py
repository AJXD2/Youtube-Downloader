import flet as ft
from flet_route import Params,Basket

def AppBasedMiddleware(page:ft.Page,params:Params,basket:Basket):

    print("App Based Middleware Called")
    #page.route = "/another_view" # If you want to change the route for some reason, use page.route
