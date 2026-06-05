from rest_framework import serializers
from .models import Content, WatchEntry
from .services import TMDBService

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = "__all__"


class WatchEntrySerializer(serializers.ModelSerializer):
    content = ContentSerializer(read_only=True)
    tmdb_id = serializers.IntegerField(write_only=True)
    media_type = serializers.CharField(write_only=True, required=False, default="movie")

    item_tmdb_id = serializers.SerializerMethodField()
    item_media_type = serializers.SerializerMethodField()

    class Meta:
        model = WatchEntry
        fields = (
            "id",
            "content",
            "tmdb_id",
            "media_type",
            "item_tmdb_id",
            "item_media_type",
            "status",
            "rating",
            "note",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user",)

    def get_item_tmdb_id(self, obj):
        return obj.content.tmdb_id

    def get_item_media_type(self, obj):
        return obj.content.media_type

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user

        tmdb_id = validated_data.pop("tmdb_id")
        media_type = validated_data.pop("media_type", "movie")

        # 1️⃣ Try to get existing Content
        content = Content.objects.filter(tmdb_id=tmdb_id, media_type=media_type).first()

        # 2️⃣ Fetch from TMDB if it doesn't exist
        if not content:
            tmdb_data = TMDBService.get_details(tmdb_id, media_type)

            title = tmdb_data.get("title") or tmdb_data.get("name")
            if not title:
                raise serializers.ValidationError("TMDB did not return a valid title.")

            content = Content.objects.create(
                tmdb_id=tmdb_id,
                title=title,
                poster_path=tmdb_data.get("poster_path"),
                overview=tmdb_data.get("overview", ""),
                release_date=tmdb_data.get("release_date") or tmdb_data.get("first_air_date"),
                genres=[g["id"] for g in tmdb_data.get("genres", [])],
                runtime=tmdb_data.get("runtime"),
                media_type=media_type,
            )

        # 3️⃣ Prevent duplicate watchlist entries
        if WatchEntry.objects.filter(user=user, content=content).exists():
            raise serializers.ValidationError("This item is already in your watchlist.")

        # 4️⃣ Create the WatchEntry
        return WatchEntry.objects.create(
            user=user,
            content=content,
            **validated_data,
        )
