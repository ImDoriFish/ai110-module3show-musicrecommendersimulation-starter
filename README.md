# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

### How real-world recommenders work

Platforms like Spotify and YouTube mainly combine two approaches. **Collaborative filtering** learns from user behavior (likes, skips, playlist adds, replays, listening time) and recommends what similar listeners enjoyed: "people who like what you like also liked this." **Content-based filtering** learns from the songs themselves (genre, mood, energy, tempo, valence) and recommends songs that are similar to what you already play. Real platforms blend both, plus context like time of day, because collaborative filtering struggles with brand-new songs and users, and content-based filtering tends to trap users in a "filter bubble" of the same sound.

### What my version prioritizes

My recommender is **content-based**, because the dataset only has song attributes and no listening history. It compares each song to a user's taste profile and gives it a score. **Genre** matters most, then **mood**, then how close the song's **energy** and **valence** are to what the user wants. Acoustic vs. electronic sound is a small bonus. After ranking, songs by the user's favorite artists get their positions shuffled within the top results, which adds some variety without letting weak matches in.

### Features used

| `Song` feature | Matching `UserProfile` preference | How they are compared |
|---|---|---|
| `genre` | `favorite_genre` | Exact match |
| `mood` | `favorite_mood` | Exact match |
| `energy` | `target_energy` | Closeness within a tolerance window |
| `valence` | `target_valence` | Closeness within a tolerance window |
| `acousticness` | `likes_acoustic` | Bonus if the song fits the preference |
| `artist` | `favorite_artists` | Used only to shuffle the final ranking |

`id` and `title` are labels for display. `tempo_bpm` and `danceability` are loaded but not scored, because in this dataset they mostly repeat what energy already captures.

### Dataset

The starter catalog had 10 songs. I expanded it to **22 songs** by adding tracks from Playboi Carti (hip-hop), Malcolm Todd (bedroom pop), Mac DeMarco (indie rock), and Dean Blunt (experimental). This added new genres, new moods (hype, euphoric, angry, romantic, nostalgic, playful, melancholy, dreamy), much lower valence values (down to 0.20) so valence can separate sad from happy songs, and several songs per artist so the favorite-artist shuffle has something to work with. The song titles are real, but the numeric features for the added songs are AI-estimated, not measured.

### User profile

The default profile used by `src/main.py`:

```python
user_prefs = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.8,          # 0 = very calm, 1 = very intense
    "valence": 0.8,         # 0 = sad/dark, 1 = happy/bright
    "likes_acoustic": False,
    # optional: "favorite_artists": ["Neon Echo"]
}
```

**Profile critique: can it tell "intense rock" from "chill lofi"?** Yes. I scored Storm Runner (intense rock) and Library Rain (chill lofi) against three profiles:

| Profile | Storm Runner (rock, intense) | Library Rain (lofi, chill) |
|---|---|---|
| pop / happy / energy 0.8 | 1.45 | 0.33 |
| rock / intense / energy 0.9 | **5.88** | 0.67 |
| lofi / chill / energy 0.38 / acoustic | 0.67 | **5.78** |

Energy and acousticness do most of the separating, so each profile clearly prefers its own style. The weakness is that the profile is **narrow**: it holds only one genre and one mood, so a user who likes both lofi and hip-hop cannot be represented. Also, genre is an exact match, so "indie pop" earns nothing for a "pop" user.

### Algorithm recipe

**Scoring rule (one song):**

| Rule | Points |
|---|---|
| Genre matches exactly | +2.0 |
| Mood matches exactly | +1.5 |
| Energy closeness | +2.0 × max(0, 1 − \|song energy − target\| / 0.3) |
| Valence closeness | +1.0 × max(0, 1 − \|song valence − target\| / 0.3) |
| Song's acoustic sound fits the user's preference (acoustic = acousticness ≥ 0.5) | +0.5 |
| **Maximum** | **7.0** |

*Weights updated after the Phase 4 experiment. The original plan used mood +1.0 and energy ×1.5 (max 6.0). See the Evaluation section of the [model card](model_card.md) for why.*

The tolerance window means a song gets full points for an exact match, fewer points as it drifts away, and zero once it is 0.3 or more away. Too calm and too intense are punished equally. Every rule that awards points also adds a reason, such as `genre match (+2.00)`.

**Ranking rule (all songs):**

1. Score every song in the catalog.
2. Sort from highest to lowest score.
3. Keep the top K (default 5).
4. If the user has favorite artists, shuffle the positions of those artists' songs among themselves inside the top K. Every other song keeps its spot.

**Data flow:**

```text
User prefs ──► for each song in songs.csv: score_song() ──► (song, score, reasons)
                                                                   │
                     sort by score ─► top K ─► favorite-artist shuffle ─► print
```

### Expected biases

- **Genre dominates.** A genre match (+2.0) is worth twice a mood match, so a song in the right genre but the wrong mood can outrank a song with the perfect mood. For example, Gym Hero (pop, intense) is expected to beat Rooftop Lights (indie pop, happy) for a happy pop listener.
- **Exact text matching.** Related genres like "pop" and "indie pop" are treated as completely different.
- **Filter bubble.** Because the system only recommends songs similar to what the user already says they like, it will rarely suggest anything outside their stated genre.
- **Small, hand-picked catalog.** With 22 songs and only one to three songs per genre, some users run out of good matches quickly, and the catalog reflects my own taste.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default "pop / happy" profile:

```text
Loaded songs: 22

============================================================
  User profile
------------------------------------------------------------
  genre            : pop
  mood             : happy
  energy           : 0.8
  valence          : 0.8
  likes_acoustic   : False
============================================================

#1  Sunrise City  -  Neon Echo
    pop / happy   |   Score: 5.77 / 6.00
    Why:
      - genre match (+2.00)
      - mood match (+1.00)
      - energy closeness (+1.40)
      - valence closeness (+0.87)
      - acoustic preference (+0.50)

#2  Gym Hero  -  Max Pulse
    pop / intense   |   Score: 4.25 / 6.00
    Why:
      - genre match (+2.00)
      - energy closeness (+0.85)
      - valence closeness (+0.90)
      - acoustic preference (+0.50)

#3  Rooftop Lights  -  Indigo Parade
    indie pop / happy   |   Score: 3.77 / 6.00
    Why:
      - mood match (+1.00)
      - energy closeness (+1.30)
      - valence closeness (+0.97)
      - acoustic preference (+0.50)

#4  Sky  -  Playboi Carti
    hip-hop / euphoric   |   Score: 2.17 / 6.00
    Why:
      - energy closeness (+1.50)
      - valence closeness (+0.17)
      - acoustic preference (+0.50)

#5  Night Drive Loop  -  Neon Echo
    synthwave / moody   |   Score: 1.75 / 6.00
    Why:
      - energy closeness (+1.25)
      - valence closeness (+0.00)
      - acoustic preference (+0.50)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



