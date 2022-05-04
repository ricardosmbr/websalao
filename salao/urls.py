from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
import debug_toolbar

urlpatterns = [
    path("__debug__/", include(debug_toolbar.urls)),
    path("", admin.site.urls),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
