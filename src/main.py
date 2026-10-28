"""
Command line runner for the Music Recommender Simulation.

Run with:  python -m src.main
"""

from src.recommender import load_songs, recommend_songs

LINE_WIDTH = 60
TOP_K = 5
SEED = 42   # fixed so the favorite-artist shuffle is repeatable; set to None for a random order each run

PROFILES = {
    # --- Normal listeners ---
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.8,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.38, "valence": 0.58,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.9, "valence": 0.5,
        "likes_acoustic": False,
    },
    "Hip-Hop Hype (Playboi Carti fan)": {
        "genre": "hip-hop", "mood": "hype", "energy": 0.75, "valence": 0.45,
        "likes_acoustic": False, "favorite_artists": ["Playboi Carti"],
    },
    # --- Edge cases: trying to trick the scoring ---
    "EDGE: Hyped but Sad (conflicting)": {
        "genre": "indie rock", "mood": "melancholy", "energy": 0.9, "valence": 0.2,
        "likes_acoustic": False,
    },
    "EDGE: Unknown Genre (k-pop)": {
        "genre": "k-pop", "mood": "happy", "energy": 0.7, "valence": 0.75,
        "likes_acoustic": False,
    },
    "EDGE: Capitalized 'Pop'": {
        "genre": "Pop", "mood": "Happy", "energy": 0.8, "valence": 0.8,
        "likes_acoustic": False,
    },
}


def print_profile(name: str, user_prefs: dict) -> None:
    """Print the profile name and its preferences as a header."""
    print("=" * LINE_WIDTH)
    print(f"  Profile: {name}")
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

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=TOP_K, seed=SEED)
        print_profile(name, user_prefs)
        print_recommendations(recommendations)


if __name__ == "__main__":
    main()
