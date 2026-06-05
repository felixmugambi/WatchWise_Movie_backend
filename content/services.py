from django.conf import settings
import requests


class TMDBService:
    BASE_URL = "https://api.themoviedb.org/3"
    API_KEY = getattr(settings, "TMDB_API_KEY", None)
    TIMEOUT = 10  # seconds

    @staticmethod
    def _check_api_key():
        if not TMDBService.API_KEY:
            raise ValueError("TMDB_API_KEY is not set in Django settings")

    @staticmethod
    def _get(url, params=None):
        TMDBService._check_api_key()

        params = params or {}
        params["api_key"] = TMDBService.API_KEY

        try:
            response = requests.get(url, params=params, timeout=TMDBService.TIMEOUT)
        except requests.RequestException as e:
            raise ValueError(f"TMDB request failed: {str(e)}")

        if response.status_code != 200:
            raise ValueError(
                f"TMDB API error {response.status_code}: {response.text}"
            )

        return response.json()

    # 🔍 Search movies, tv, or multi
    @staticmethod
    def search_content(query, media_type="multi"):
        if not query:
            return []

        url = f"{TMDBService.BASE_URL}/search/{media_type}"
        data = TMDBService._get(url, {"query": query})
        return data.get("results", [])

    # 🎬 Movie / TV details
    @staticmethod
    def get_details(tmdb_id, media_type="movie"):
        url = f"{TMDBService.BASE_URL}/{media_type}/{tmdb_id}"
        return TMDBService._get(url)

    # 🤝 Similar content
    @staticmethod
    def get_similar(tmdb_id, media_type="movie"):
        url = f"{TMDBService.BASE_URL}/{media_type}/{tmdb_id}/similar"
        data = TMDBService._get(url)
        return data.get("results", [])

    # 🔥 Trending (weekly)
    @staticmethod
    def get_trending():
        url = f"{TMDBService.BASE_URL}/trending/all/week"
        data = TMDBService._get(url)
        return data.get("results", [])
