import logging

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.gis.geos import Point

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiParameter

from app.core.pagination import CustomPagination
from app.core.utils import get_or_not_found
from app.users.api.serializers import GeoJsonSerializer, NerbyUserSerializer
from app.users.models import User, UserVectorLine

logger = logging.getLogger(__name__)


class GeoJsonView(APIView):
    serializer_class = GeoJsonSerializer

    def get_query_set(self, user_id):
        """
        A queryset to retrieve the custom made geojson of a user.
        """
        get_or_not_found(User.objects.all(), id=user_id)
        obj = get_or_not_found(UserVectorLine.objects.all(), user_id=user_id)
        return {
            "type": " Feature",
            "geometry": obj.line.geojson,
            "properties": {"user_id": user_id, "username": obj.user.username},
        }

    @extend_schema(
        operation_id="Geo Json fetch Api.",
        summary="BT-UR-01",
        description="""
        An Api to get Geo Json.
        """,
        request=serializer_class,
        tags=[
            "User",
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_get_json_fetch_response",
                fields={
                    "message": serializers.CharField(
                        default="Geo Json Fetched Successfully"
                    ),
                    "data": serializer_class(),
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve get geojson.

        Args:
            request: HTTP request object.

        Returns:
            Response: A geojson of that user.
        """
        qs = self.get_query_set(user_id=kwargs.get("user_id"))
        serializer = self.serializer_class(qs)
        logger.info("GeoJsonData Fetched Successfully.")
        return Response(
            {
                "message": "GeoJsonData Fetched Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class NearbyUsersView(APIView):
    serializer_class = NerbyUserSerializer
    pagination_class = CustomPagination

    def get_queryset(self, point):
        """
        Queryset that uses the custom manager to fetch only those
        users whose distance are nearby.
        """
        return User.objects.nearby_users(point)

    def get_params_data(self, request):
        """
        Utility for validating the lng and lat query params.
        """
        try:
            lat = float(request.query_params.get("lat"))
            lng = float(request.query_params.get("lng"))
        except ValueError:
            raise serializers.ValidationError("Longitude and Latitude must be numbers")

        if not lat or not lng:
            raise serializers.ValidationError(
                "Must provide both longitude and latitude values."
            )
        return Point(lng, lat)

    @extend_schema(
        operation_id="Nearby Users fetch Api.",
        summary="BT-UR-02",
        description="""
        An Api to get nearby users.
        """,
        request=serializer_class,
        tags=[
            "User",
        ],
        parameters=[
            OpenApiParameter(
                name="lng",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="lat",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="page",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
            OpenApiParameter(
                name="page_size",
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            status.HTTP_200_OK: inline_serializer(
                "success_nearby_users_fetch_response",
                fields={
                    "message": serializers.CharField(
                        default="Nearby Users Fetched Successfully"
                    ),
                    "data": serializer_class(),
                },
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        """
        Handle GET request to retrieve nearby users with pagination.

        Args:
            request: HTTP request object.

        Returns:
            Response: List of nearby users with pagination (if applicable).
        """
        point = self.get_params_data(request)
        qs = self.get_queryset(point)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(qs, request)

        if page is not None:
            serializer = NerbyUserSerializer(page, many=True)
            paginated_response = paginator.get_paginated_response(serializer.data)
            paginated_data = paginated_response.data
            logger.info("Nearby users fetched with pagination.")
            return Response(
                {
                    "message": "Nearby Users Fetched Successfully",
                    "data": paginated_data,
                },
                status=status.HTTP_200_OK,
            )
        serializer = NerbyUserSerializer(qs, many=True)
        logger.info("Nearby users fetched without pagination.")
        return Response(
            {
                "message": "Nearby Users Fetched Successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
