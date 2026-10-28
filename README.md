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
Loaded songs: 19

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



