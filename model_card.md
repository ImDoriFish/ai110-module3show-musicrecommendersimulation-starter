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
