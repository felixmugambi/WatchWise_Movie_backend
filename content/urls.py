from django.urls import path
from .views import SearchContentView, WatchListCreateView, WatchEntryDetailView

urlpatterns = [
    path('search/', SearchContentView.as_view(), name='search-content'),
    path('watchlist/', WatchListCreateView.as_view(), name='watchlist-list-create'),
    path('watchlist/<int:pk>/', WatchEntryDetailView.as_view(), name='watchlist-detail'),
]
