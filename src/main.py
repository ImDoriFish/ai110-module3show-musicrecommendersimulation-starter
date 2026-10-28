"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

LINE_WIDTH = 60


def print_profile(user_prefs: dict) -> None:
    """Print the user's taste profile as a header."""
    print("=" * LINE_WIDTH)
    print("  User profile")
    print("-" * LINE_WIDTH)
    for key, value in user_prefs.items():
        print(f"  {key:<17}: {value}")
    print("=" * LINE_WIDTH)


def print_recommendations(recommendations: list) -> None:
    """Print each recommended song with its rank, score, and reasons."""
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  -  {song['artist']}")
        print(f"    {song['genre']} / {song['mood']}   |   Score: {score:.2f} / 6.00")
        print("    Why:")
        for reason in explanation.split(", "):
            print(f"      - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Default "pop / happy" profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.8,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_profile(user_prefs)
    print_recommendations(recommendations)


if __name__ == "__main__":
    main()
