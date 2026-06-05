from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from content.models import WatchEntry
from content.services import TMDBService


class RecommendationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1️⃣ Last highly rated completed item
        last_liked = (
            WatchEntry.objects.filter(
                user=request.user,
                status="COMPLETED",
                rating__gte=4
            )
            .select_related("content")
            .order_by("-updated_at")
            .first()
        )

        # 2️⃣ Use TMDB recommendations
        if last_liked:
            content = last_liked.content
            tmdb_id = content.tmdb_id
            media_type = content.media_type

            try:
                results = TMDBService.get_similar(
                    tmdb_id=tmdb_id,
                    media_type=media_type
                )

                for item in results:
                    item["media_type"] = media_type

                
            except Exception:
                results = []

            if results:
                return Response({
                    "source": "based_on_watch_history",
                    "seed": content.title,
                    "results": results
                })

        # 3️⃣ Fallback → trending
        results = TMDBService.get_trending()

        for item in results:
            item.setdefault("media_type", "movie")

            
        return Response({
            "source": "trending",
            "results": results
        })
