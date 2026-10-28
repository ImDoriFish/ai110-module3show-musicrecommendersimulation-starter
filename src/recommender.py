import csv
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_valence: Optional[float] = None                         # optional: skipped if not given
    favorite_artists: List[str] = field(default_factory=list)      # optional: used for the shuffle

    def to_prefs(self) -> Dict:
        """Convert this profile into the prefs dict that score_song() expects."""
        prefs = {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "likes_acoustic": self.likes_acoustic,
            "favorite_artists": self.favorite_artists,
        }
        if self.target_valence is not None:
            prefs["valence"] = self.target_valence
        return prefs

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    Thin wrapper: converts objects to dicts and reuses score_song / recommend_songs.
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user."""
        song_dicts = [asdict(song) for song in self.songs]
        results = recommend_songs(user.to_prefs(), song_dicts, k)
        return [Song(**song_dict) for song_dict, _, _ in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a readable explanation of why this song got its score."""
        score, reasons = score_song(user.to_prefs(), asdict(song))
        return f"Score {score:.2f}: " + (", ".join(reasons) or "no strong matches")

INT_FIELDS = ["id"]
FLOAT_FIELDS = ["energy", "tempo_bpm", "valence", "danceability", "acousticness"]

def _convert_types(row: Dict) -> Dict:
    """Turn numeric text values into int/float so we can do math with them."""
    for field in INT_FIELDS:
        row[field] = int(row[field])
    for field in FLOAT_FIELDS:
        row[field] = float(row[field])
    return row

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file into a list of dicts with numeric columns converted."""
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        # Each row becomes a dict like {"title": "Sunrise City", "energy": "0.82", ...}
        rows = csv.DictReader(csv_file)
        return [_convert_types(row) for row in rows]

# --- Algorithm Recipe weights ---
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 1.5
VALENCE_WEIGHT = 1.0
ACOUSTIC_WEIGHT = 0.5
TOLERANCE = 0.3          # how far a number can be from the target and still earn points
ACOUSTIC_CUTOFF = 0.5    # acousticness at or above this counts as an "acoustic" song

def closeness(song_value: float, target_value: float, tolerance: float = TOLERANCE) -> float:
    """Return 1.0 for a perfect match, sliding down to 0.0 once the gap reaches the tolerance."""
    gap = abs(song_value - target_value)
    return max(0.0, 1 - gap / tolerance)

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Text features: exact match or nothing
    if "genre" in user_prefs and song["genre"] == user_prefs["genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match (+{GENRE_WEIGHT:.2f})")

    if "mood" in user_prefs and song["mood"] == user_prefs["mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match (+{MOOD_WEIGHT:.2f})")

    # Number features: points based on closeness within the tolerance window
    if "energy" in user_prefs:
        points = ENERGY_WEIGHT * closeness(song["energy"], user_prefs["energy"])
        score += points
        reasons.append(f"energy closeness (+{points:.2f})")

    if "valence" in user_prefs:
        points = VALENCE_WEIGHT * closeness(song["valence"], user_prefs["valence"])
        score += points
        reasons.append(f"valence closeness (+{points:.2f})")

    # Acoustic bonus: does the song's sound fit what the user likes?
    if "likes_acoustic" in user_prefs:
        song_is_acoustic = song["acousticness"] >= ACOUSTIC_CUTOFF
        if song_is_acoustic == user_prefs["likes_acoustic"]:
            score += ACOUSTIC_WEIGHT
            reasons.append(f"acoustic preference (+{ACOUSTIC_WEIGHT:.2f})")

    return score, reasons

def shuffle_favorite_artists(ranked: List[Tuple[Dict, float, str]], favorite_artists: List[str],
                             seed: Optional[int] = None) -> List[Tuple[Dict, float, str]]:
    """Shuffle songs by favorite artists among their own slots; all other songs keep their positions."""
    slots = [i for i, (song, _, _) in enumerate(ranked) if song["artist"] in favorite_artists]
    favorites = [ranked[i] for i in slots]
    random.Random(seed).shuffle(favorites)

    reordered = list(ranked)
    for slot, item in zip(slots, favorites):
        reordered[slot] = item
    return reordered

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    seed: Optional[int] = None) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest first, keep the top k, then shuffle favorite artists within them."""
    # 1. Judge: score every song in the catalog
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, ", ".join(reasons)))

    # 2. Rank: sort by score (highest first) and keep the top k
    top_k = sorted(scored, key=lambda item: item[1], reverse=True)[:k]

    # 3. Variety: shuffle favorite-artist songs among their own spots in the top k
    favorite_artists = user_prefs.get("favorite_artists", [])
    if favorite_artists:
        top_k = shuffle_favorite_artists(top_k, favorite_artists, seed)

    return top_k
