from django.urls import include, path

app_name = "core"
urlpatterns = [
    path("user/", include("app.users.api.urls"), name="user"),
]
