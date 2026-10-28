# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

CartiFinder 1.0: a content-based music recommender that scores songs by genre, mood, energy, valence, and acoustic sound
---

## 2. Intended Use  

Goal: Suggest the top 5 songs from a small catalog that best match a user’s stated taste (favorite genre, mood, energy, valence, acoustic preference, and optional favorite artists), and explain why each song was picked.

Intended use: A classroom simulation to learn how recommenders turn data into rankings, and where bias comes from. It assumes the user can describe their taste in a few words and numbers.

Not intended for: Real users or a real music app. It has only 22 songs, no listening history, and AI-estimated song data. It should not be used to decide which artists get promoted.

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

The catalog has 22 songs. The starter file had 10 (pop, lofi, rock, ambient, jazz, synthwave, indie pop). I added 12 songs from Playboi Carti (hip-hop), Malcolm Todd (bedroom pop), Mac DeMarco (indie rock), and Dean Blunt (experimental). That added moods like hype, angry, romantic, nostalgic, melancholy, and dreamy, plus much sadder songs (valence down to 0.20). Each song has genre, mood, energy, tempo, valence, danceability, and acousticness.

Limits: The numbers for the songs I added are AI estimates, not real measurements. Most genres have only 1–3 songs (only one rock song). The data has nothing about lyrics, language, vocals, or who listens to what, so it can’t capture the “same audience” connections that real taste depends on.

---

## 5. Strengths  

Works well when the user’s genre has several songs: Chill Lofi gets three lofi tracks scoring above 5, and the Carti fan gets all three Carti songs on top.
Clearly separates opposite tastes: pop and lofi results have zero overlap.
Handles unknown genres gracefully: the k-pop user still gets bright, upbeat songs by falling back on mood and energy. 

---

## 6. Limitations and Bias 

The system only understands features, not context. My recommender judges songs purely by genre, mood, energy, valence, and acousticness, so it has no idea which artists share an audience. For the Playboi Carti fan profile, the #4 and #5 picks were a synthwave song and a rock song that have nothing to do with rage or hip-hop; they only ranked high because they are loud and electronic. Meanwhile, Dean Blunt, who many Carti listeners also play, scored under 1.0 because his songs are quiet and sad “on paper.” This creates a filter bubble based on sound instead of taste: users only get songs that measure similar, not songs that people like them actually enjoy.

---

## 7. Evaluation  

### How I tested

I ran the recommender on **7 user profiles** and looked at the top 5 songs for each, including the "Why" reasons, to check whether each pick made sense.

- **Normal listeners:** High-Energy Pop, Chill Lofi, Deep Intense Rock, and Hip-Hop Hype (a Playboi Carti fan, with the favorite-artist shuffle turned on)
- **Edge cases meant to trick the scoring:** Hyped but Sad (energy 0.9 but valence 0.2), Unknown Genre (k-pop, which is not in the catalog), and Capitalized "Pop" (same as the pop fan, but typed "Pop" / "Happy")

I also ran one weight experiment (below) and the two starter unit tests with `pytest`. The comparisons in this section use the final weights (genre 2.0, mood 1.5, energy 2.0).

### What I looked for

- Does the #1 song match everything the user asked for?
- When the user's genre runs out, are the fallback songs reasonable?
- Does any song show up in almost every list?

### Profile comparisons

- **High-Energy Pop vs. Chill Lofi:** complete opposites with zero overlap. Pop gets loud, bright, electronic songs (Sunrise City, Rooftop Lights), while lofi shifts to quiet, acoustic study tracks (Library Rain, Midnight Coding). This makes sense because energy and acousticness point in opposite directions for these two users.
- **High-Energy Pop vs. Deep Intense Rock:** both want high energy, so they share Gym Hero, Sky, and Night Drive Loop. The difference is the feeling: pop puts the *happy* Rooftop Lights at #2, while rock puts the *intense* Gym Hero at #2. Same energy, different mood.
- **Chill Lofi vs. Deep Intense Rock:** no overlap at all. Lofi has plenty of matches (three lofi songs score above 5), while rock has only one rock song (Storm Runner) and then falls back to pop and hip-hop. The rock fan is underserved because of the catalog, not the math.
- **Deep Intense Rock vs. Hip-Hop Hype:** both like loud songs, so Stop Breathing and Night Drive Loop appear in both. The hip-hop fan gets three real genre matches at the top, while the rock fan gets only one, which shows how much genre drives the top of the list.
- **High-Energy Pop vs. Capitalized "Pop":** the same person, but typing "Pop" instead of "pop" dropped Sunrise City from 6.73 to 3.23 and let Sky move up to #3. The system treats capital letters as a different genre. This is a real bug that an edge case caught.
- **High-Energy Pop vs. Unknown Genre (k-pop):** with no k-pop in the catalog, nobody gets genre points, so the system falls back on mood and energy. It still gives sensible bright, upbeat songs (Rooftop Lights, Sunrise City, Sweet Boy), just with lower scores.
- **Hyped but Sad vs. Deep Intense Rock:** both want energy around 0.9, but the sad user's #1 is Chamber of Reflection, a quiet song (energy 0.35). It won on genre, mood, and valence even though it got zero energy points. No song in the catalog is both loud *and* sad, so the system has to pick one want and ignore the other.
- **Hip-Hop Hype vs. High-Energy Pop:** both lists end with the same kind of "filler" songs (Night Drive Loop, Sky, or Rooftop Lights). Once the favorite genre runs out, everyone gets the same loud, non-acoustic songs.

### What surprised me

- **Sky and Night Drive Loop show up in 5 of 7 lists.** They are not great matches for anyone, but they are "okay at everything": high energy, middle valence, and not acoustic. Since most profiles don't like acoustic music, they get the +0.5 acoustic bonus almost every time.
- **The shuffle put Sky at #1 for the Carti fan** even though Magnolia scored higher. Variety can hide the best match.
- **The fallback songs for the Carti fan felt wrong to me.** The top 3 Playboi Carti songs were right, but #4 and #5 (a synthwave song and an indie pop song) have nothing to do with rage or hip-hop. They only ranked high because of their scores on features like energy; the code doesn't know the context. As a listener, I would expect Dean Blunt there instead, but his songs are quiet and sad on paper, so they score under 1.0.

### Why does Gym Hero keep showing up for "Happy Pop" fans? (plain English)

Gym Hero is labeled "pop" and is very loud, so for a pop fan it automatically gets the biggest bonus in the system, the genre match, plus most of the energy points. It never gets the "happy" bonus, because it is an *intense* workout song. With my original weights, the genre bonus was so big that Gym Hero beat Rooftop Lights, a happy song that fits better. After I raised the mood and energy weights a little, Rooftop Lights now edges ahead, but Gym Hero still lands at #3. The system trusts the genre label more than the actual feeling of the song.

### Experiment: weight shift

**Question:** Gym Hero (pop, *intense*) kept ranking above Rooftop Lights (indie pop, *happy*) for a happy pop listener, because a genre match (+2.0) was worth twice a mood match (+1.0). What happens if mood and energy count more?

**What I tried.** I tested four sets of weights on all 7 profiles. I focused on two checks: does the happy pop fan get the happy song ahead of Gym Hero, and does the Playboi Carti fan keep all three hip-hop songs at the top?

| Version | Genre / Mood / Energy | Pop fan: Rooftop Lights beats Gym Hero? | Carti fan: top 3 all hip-hop? |
|---|---|---|---|
| Original | 2.0 / 1.0 / 1.5 | No (Gym Hero 4.25 vs. Rooftop 3.77) | Yes |
| Assignment suggestion (half genre, double energy) + double mood | 1.0 / 2.0 / 3.0 | Yes (Rooftop 6.07 vs. Gym Hero 4.10) | **No:** Night Drive Loop (synthwave) passes Stop Breathing, and Rooftop Lights enters the list |
| Half genre, mood and energy +1 | 1.0 / 2.0 / 2.5 | Yes (5.63 vs. 3.82) | **No:** Night Drive Loop jumps to #3 |
| **Final: keep genre, mood and energy +0.5** | **2.0 / 1.5 / 2.0** | **Yes (4.70 vs. 4.53)** | **Yes:** Stop Breathing stays #3, and its lead over Night Drive Loop grows (4.13 vs. 3.37) |

**Results with the final weights (top 5):**

```text
High-Energy Pop:   Sunrise City 6.73, Rooftop Lights 4.70, Gym Hero 4.53, Sky 2.67, Night Drive Loop 2.17
Deep Intense Rock: Storm Runner 6.87, Gym Hero 3.90, Stop Breathing 2.70, Sky 2.67, Night Drive Loop 2.47
Hip-Hop Hype:      Sky 4.83 (shuffled to #1), Magnolia 5.83, Stop Breathing 4.13, Night Drive Loop 3.37, Rooftop Lights 2.43
```

**More accurate, or just different?** Cutting the genre weight made the results *different*, not better. It fixed the pop fan but hurt the hip-hop fan: with genre worth less and energy worth more, any loud electronic song started crowding out real hip-hop. No single set of weights works for every kind of listener. I chose to keep genre as the strongest signal and only nudge mood and energy up. That fixed the Gym Hero problem without losing the hip-hop fan's accuracy, so I kept these weights.

**What weights could not fix.** For the Carti fan, #4 and #5 are still not hip-hop, because the catalog only has three hip-hop songs. That is a data problem, not a weight problem.

### Profile test results (original weights)

Output of `python -m src.main` (22 songs, top 5 per profile, `SEED = 42`) using the **original** weights (genre 2.0, mood 1.0, energy 1.5), before the experiment above.

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

Fix text matching: lowercase genre and mood before comparing, and give partial credit for related genres (pop ↔ indie pop).
More diverse top 5: limit how many filler songs can appear, and add more songs per genre so fans don’t run out of matches.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
My biggest learning moment was testing the Playboi Carti fan profile. The top 3 Carti songs looked right, but #4 and #5 were a synthwave song and an indie pop song that have nothing to do with rage or hip-hop. Meanwhile, Dean Blunt, who a lot of Carti fans actually listen to, scored under 1.0 because his songs are quiet and sad on paper. That’s when it clicked for me that a recommender only knows the features you give it. It doesn’t understand context or culture, and that’s exactly why real apps like Spotify also use collaborative filtering based on what similar listeners play. I also learned that “feature” in machine learning means a piece of data like energy or genre, not something the app can do, which confused me at first.

- How AI helped, and when I had to double-check it
I used an AI assistant to explain concepts, write most of the code, which saved a lot of time. But I had to stay in control of the design decisions. When the AI suggested the assignment’s weight shift (cut genre in half, double energy), I tested it and saw that it fixed the pop fan but made the hip-hop fan worse, so I chose my own weights (genre 2.0, mood 1.5, energy 2.0) that kept genre as the strongest signal. I also questioned things that didn’t make sense to me, like why the starter code had both classes and functions doing the same job, and I had to fix a bug where my main.py got corrupted when VS Code had an unsaved copy open while the file was being edited. AI was fast, but I still had to check every result against my own judgment.
- What surprised me about simple algorithms
was surprised that just adding up five numbers could feel like real recommendations. The Chill Lofi profile got three actual study tracks, and pop and lofi had zero overlap, which is exactly what I’d expect. Showing the reasons, like “genre match (+2.00),” made it feel smart and trustworthy, even though it’s really just basic math. It also surprised me how easily it breaks: typing “Pop” with a capital P cut the top song’s score in half.
- What I’d try next
Next, I’d add a simple form of collaborative filtering, like “people who like Carti also like Dean Blunt,” so the system can learn connections that aren’t in the audio features. I’d also lowercase genres and moods before comparing them, give partial credit for related genres like pop and indie pop, and add more songs per genre so fans of rock or hip-hop don’t run out of real matches.

- Something unexpected or interesting you discovered  
The most unexpected thing was that the songs showing up the most weren’t the best matches for anyone. Sky and Night Drive Loop appeared in 5 of my 7 test profiles, not because they fit, but because they were “okay at everything”: loud, medium happiness, and not acoustic. Since most of my profiles didn’t like acoustic music, they got a small bonus almost every time. A tiny +0.5 rule I barely thought about ended up shaping almost every list. I also found it interesting that my own favorite-artist shuffle put Sky at #1 for the Carti fan even though Magnolia scored higher, so adding variety can quietly hide the best answer.
- How this changed the way you think about music recommendation apps  
I used to think apps like Spotify just “knew” my taste. Now I see that every recommendation is a choice someone made about what counts more: genre or mood, energy or the artist. Changing one weight made my system better for pop fans but worse for hip-hop fans, so there’s no perfect setting, only tradeoffs.