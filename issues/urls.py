from django.urls import path
from .views import get_issues, get_Reporter, post_issues, post_Reporter

urlpatterns = [
    path("issues/", get_issues),
    path("issues/<int:id>/", get_issues),
    path("postissues/", post_issues),
    path("postreporters/", post_Reporter),
    path("reporters/", get_Reporter),
    path("reporters/<int:reporter_id>/", get_Reporter),
]