from rest_framework import generics, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WatchEntry, Content
from .serializers import WatchEntrySerializer, ContentSerializer
from .services import TMDBService

class SearchContentView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q')
        if not query:
            return Response([])
        
        results = TMDBService.search_content(query)
        # We don't save to DB on search, just return raw results or transform them
        return Response(results)

class WatchListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchEntrySerializer

    def get_queryset(self):
        return WatchEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class WatchEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WatchEntrySerializer
    
    def get_queryset(self):
        return WatchEntry.objects.filter(user=self.request.user)
