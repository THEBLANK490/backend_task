from django.urls import path

from app.users.api.views import GeoJsonView, NearbyUsersView

app_name = "user"

urlpatterns = [
    path("line/<int:user_id>/geojson/", GeoJsonView.as_view(), name="geo-json"),
    path("nearby/", NearbyUsersView.as_view(), name="nearby-users"),
]
