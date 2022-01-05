# Wordle solver

# Interactive Usage
This will always tell you to guess "AROSE" as the first word. It then asks you for feedback.

If a letter didn't match, at all enter a period, if it matched in the wrong position, enter it as a lower case letter, and if it matched in the correct position enter it as an uppercase letter. For example, if our word is TRUSS a session would look like

```
Guess AROSE
.R.S.
Guess WRIST, 22 candidates remaining
.R.St
🔮🔮🔮 TRUSS 🔮🔮🔮
```

When we guessed AROSE we matched the R and the S in the correct position. Next wrist matched the T in the wronge position (and continued to get R and S correctly). This meant we could guess TRUSS with certainty.