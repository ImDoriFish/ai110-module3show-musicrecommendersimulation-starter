# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The recommender works like a judge at a talent show. It looks at every song in the catalog one at a time, gives it a score out of 6 based on how well it fits the user's taste, then lines the songs up from highest to lowest score and shows the top 5.

**What it looks at.** Each song has a genre, a mood, an energy level (calm to intense), a valence level (sad to happy sounding), and an acousticness level (electronic to acoustic). The user says what they like: a favorite genre, a favorite mood, how energetic and how happy they want the music to feel, whether they like acoustic sound, and optionally some favorite artists.

**How a song earns points.**

- **Genre:** if the song's genre is exactly the user's favorite, it gets 2 points. Otherwise it gets 0, even for a close genre like "indie pop" vs. "pop."
- **Mood:** if the mood matches exactly, it gets 1 point.
- **Energy:** up to 1.5 points. A song with exactly the energy the user wants gets the full 1.5. The further away it is, the fewer points it gets, and once it is 0.3 or more away it gets nothing. A song that is too intense loses points the same way as a song that is too calm.
- **Valence:** up to 1 point, using the same "closer is better, too far gets nothing" rule. This gives partial credit to songs whose mood label is different but whose feeling is similar, like "relaxed" vs. "happy."
- **Acoustic sound:** a small 0.5 bonus if the song's sound (acoustic or electronic) fits what the user prefers.

Every time a song earns points, the system writes down a short reason, like "genre match (+2.00)," so the user can see why each song was picked.

**Ranking and variety.** After scoring, songs are sorted from highest to lowest and the top 5 are kept. If the user has favorite artists, any songs by those artists inside the top 5 swap places with each other at random. The other songs keep their spots. This adds some variety without letting weak matches sneak into the list.

**Changes from the starter logic.** The starter only suggested genre, mood, and energy. I added valence to give mood a "partial credit" option, scored energy and valence with a tolerance window instead of a straight line so far-off songs drop to zero, added an acoustic bonus, and added the favorite-artist shuffle as a separate ranking step.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

### Profile test results

Output of `python -m src.main` (22 songs, top 5 per profile, `SEED = 42`).

#### High-Energy Pop

```text
============================================================
  Profile: High-Energy Pop
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

#### Chill Lofi

```text
============================================================
  Profile: Chill Lofi
------------------------------------------------------------
  genre            : lofi
  mood             : chill
  energy           : 0.38
  valence          : 0.58
  likes_acoustic   : True
============================================================

#1  Library Rain  -  Paper Lanterns
    lofi / chill   |   Score: 5.78 / 6.00
    Why:
      - genre match (+2.00)
      - mood match (+1.00)
      - energy closeness (+1.35)
      - valence closeness (+0.93)
      - acoustic preference (+0.50)

#2  Midnight Coding  -  LoRoom
    lofi / chill   |   Score: 5.73 / 6.00
    Why:
      - genre match (+2.00)
      - mood match (+1.00)
      - energy closeness (+1.30)
      - valence closeness (+0.93)
      - acoustic preference (+0.50)

#3  Focus Flow  -  LoRoom
    lofi / focused   |   Score: 4.87 / 6.00
    Why:
      - genre match (+2.00)
      - energy closeness (+1.40)
      - valence closeness (+0.97)
      - acoustic preference (+0.50)

#4  Spacewalk Thoughts  -  Orbit Bloom
    ambient / chill   |   Score: 3.27 / 6.00
    Why:
      - mood match (+1.00)
      - energy closeness (+1.00)
      - valence closeness (+0.77)
      - acoustic preference (+0.50)

#5  Coffee Shop Stories  -  Slow Stereo
    jazz / relaxed   |   Score: 2.52 / 6.00
    Why:
      - energy closeness (+1.45)
      - valence closeness (+0.57)
      - acoustic preference (+0.50)
```

#### Deep Intense Rock

```text
============================================================
  Profile: Deep Intense Rock
------------------------------------------------------------
  genre            : rock
  mood             : intense
  energy           : 0.9
  valence          : 0.5
  likes_acoustic   : False
============================================================

#1  Storm Runner  -  Voltline
    rock / intense   |   Score: 5.88 / 6.00
    Why:
      - genre match (+2.00)
      - mood match (+1.00)
      - energy closeness (+1.45)
      - valence closeness (+0.93)
      - acoustic preference (+0.50)

#2  Gym Hero  -  Max Pulse
    pop / intense   |   Score: 2.95 / 6.00
    Why:
      - mood match (+1.00)
      - energy closeness (+1.35)
      - valence closeness (+0.10)
      - acoustic preference (+0.50)

#3  Sky  -  Playboi Carti
    hip-hop / euphoric   |   Score: 2.33 / 6.00
    Why:
      - energy closeness (+1.00)
      - valence closeness (+0.83)
      - acoustic preference (+0.50)

#4  Stop Breathing  -  Playboi Carti
    hip-hop / angry   |   Score: 2.23 / 6.00
    Why:
      - energy closeness (+1.40)
      - valence closeness (+0.33)
      - acoustic preference (+0.50)

#5  Night Drive Loop  -  Neon Echo
    synthwave / moody   |   Score: 2.22 / 6.00
    Why:
      - energy closeness (+0.75)
      - valence closeness (+0.97)
      - acoustic preference (+0.50)
```

#### Hip-Hop Hype (Playboi Carti fan)

```text
============================================================
  Profile: Hip-Hop Hype (Playboi Carti fan)
------------------------------------------------------------
  genre            : hip-hop
  mood             : hype
  energy           : 0.75
  valence          : 0.45
  likes_acoustic   : False
  favorite_artists : ['Playboi Carti']
============================================================

#1  Sky  -  Playboi Carti
    hip-hop / euphoric   |   Score: 4.42 / 6.00
    Why:
      - genre match (+2.00)
      - energy closeness (+1.25)
      - valence closeness (+0.67)
      - acoustic preference (+0.50)

#2  Magnolia  -  Playboi Carti
    hip-hop / hype   |   Score: 5.12 / 6.00
    Why:
      - genre match (+2.00)
      - mood match (+1.00)
      - energy closeness (+0.65)
      - valence closeness (+0.97)
      - acoustic preference (+0.50)

#3  Stop Breathing  -  Playboi Carti
    hip-hop / angry   |   Score: 3.85 / 6.00
    Why:
      - genre match (+2.00)
      - energy closeness (+0.85)
      - valence closeness (+0.50)
      - acoustic preference (+0.50)

#4  Night Drive Loop  -  Neon Echo
    synthwave / moody   |   Score: 2.87 / 6.00
    Why:
      - energy closeness (+1.50)
      - valence closeness (+0.87)
      - acoustic preference (+0.50)

#5  Storm Runner  -  Voltline
    rock / intense   |   Score: 2.10 / 6.00
    Why:
      - energy closeness (+0.70)
      - valence closeness (+0.90)
      - acoustic preference (+0.50)
```

#### EDGE: Hyped but Sad (conflicting)

```text
============================================================
  Profile: EDGE: Hyped but Sad (conflicting)
------------------------------------------------------------
  genre            : indie rock
  mood             : melancholy
  energy           : 0.9
  valence          : 0.2
  likes_acoustic   : False
============================================================

#1  Chamber of Reflection  -  Mac DeMarco
    indie rock / melancholy   |   Score: 4.33 / 6.00
    Why:
      - genre match (+2.00)
      - mood match (+1.00)
      - energy closeness (+0.00)
      - valence closeness (+0.83)
      - acoustic preference (+0.50)

#2  Stop Breathing  -  Playboi Carti
    hip-hop / angry   |   Score: 2.57 / 6.00
    Why:
      - energy closeness (+1.40)
      - valence closeness (+0.67)
      - acoustic preference (+0.50)

#3  My Kind of Woman  -  Mac DeMarco
    indie rock / romantic   |   Score: 2.17 / 6.00
    Why:
      - genre match (+2.00)
      - energy closeness (+0.00)
      - valence closeness (+0.17)

#4  Storm Runner  -  Voltline
    rock / intense   |   Score: 2.02 / 6.00
    Why:
      - energy closeness (+1.45)
      - valence closeness (+0.07)
      - acoustic preference (+0.50)

#5  Salad Days  -  Mac DeMarco
    indie rock / nostalgic   |   Score: 2.00 / 6.00
    Why:
      - genre match (+2.00)
      - energy closeness (+0.00)
      - valence closeness (+0.00)
```

#### EDGE: Unknown Genre (k-pop)

```text
============================================================
  Profile: EDGE: Unknown Genre (k-pop)
------------------------------------------------------------
  genre            : k-pop
  mood             : happy
  energy           : 0.7
  valence          : 0.75
  likes_acoustic   : False
============================================================

#1  Rooftop Lights  -  Indigo Parade
    indie pop / happy   |   Score: 3.50 / 6.00
    Why:
      - mood match (+1.00)
      - energy closeness (+1.20)
      - valence closeness (+0.80)
      - acoustic preference (+0.50)

#2  Sunrise City  -  Neon Echo
    pop / happy   |   Score: 3.10 / 6.00
    Why:
      - mood match (+1.00)
      - energy closeness (+0.90)
      - valence closeness (+0.70)
      - acoustic preference (+0.50)

#3  Sweet Boy  -  Malcolm Todd
    bedroom pop / playful   |   Score: 2.33 / 6.00
    Why:
      - energy closeness (+1.00)
      - valence closeness (+0.83)
      - acoustic preference (+0.50)

#4  Night Drive Loop  -  Neon Echo
    synthwave / moody   |   Score: 1.88 / 6.00
    Why:
      - energy closeness (+1.25)
      - valence closeness (+0.13)
      - acoustic preference (+0.50)

#5  Sky  -  Playboi Carti
    hip-hop / euphoric   |   Score: 1.83 / 6.00
    Why:
      - energy closeness (+1.00)
      - valence closeness (+0.33)
      - acoustic preference (+0.50)
```

#### EDGE: Capitalized 'Pop'

```text
============================================================
  Profile: EDGE: Capitalized 'Pop'
------------------------------------------------------------
  genre            : Pop
  mood             : Happy
  energy           : 0.8
  valence          : 0.8
  likes_acoustic   : False
============================================================

#1  Sunrise City  -  Neon Echo
    pop / happy   |   Score: 2.77 / 6.00
    Why:
      - energy closeness (+1.40)
      - valence closeness (+0.87)
      - acoustic preference (+0.50)

#2  Rooftop Lights  -  Indigo Parade
    indie pop / happy   |   Score: 2.77 / 6.00
    Why:
      - energy closeness (+1.30)
      - valence closeness (+0.97)
      - acoustic preference (+0.50)

#3  Gym Hero  -  Max Pulse
    pop / intense   |   Score: 2.25 / 6.00
    Why:
      - energy closeness (+0.85)
      - valence closeness (+0.90)
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


---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
