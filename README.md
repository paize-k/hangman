# Hangman Game - Computer Science Homework

## Overview
An interactive Hangman game with a graphical user interface built with Python and Tkinter. Features multiple difficulty levels, leaderboard tracking, sound effects, text-to-speech, hints, and multilingual word support.

## Recent Changes
- 2025-11-04: Initial project setup with Python 3.11
- 2025-11-04: Created complete game implementation with all requested features
- 2025-11-04: Implemented sound effects using pygame and numpy (generates tones programmatically)
- 2025-11-04: Added graceful degradation for optional features (sound, TTS) in headless environments

## Project Architecture
- **main.py**: Main game application with Tkinter GUI (680+ lines)
  - HangmanGame class: Main game logic and UI
  - Sound generation using numpy sine waves
  - Text-to-speech integration with pyttsx3
  - Graceful handling of missing audio hardware
- **words.py**: Word banks organized by difficulty level and language
  - 4 languages: English, Spanish, French, German
  - 3 difficulty levels per language: Easy, Medium, Hard
- **leaderboard.json**: Persistent storage for game statistics (auto-generated)
- **requirements.txt**: Python dependencies

## Features
✓ Interactive GUI with animated hangman drawing (updates with each wrong guess)
✓ Three difficulty levels (Easy, Medium, Hard)
✓ Leaderboard system tracking wins/losses with persistent storage
✓ Colorful UI with themed colors for different game states
✓ Sound effects for game events (correct, wrong, win, lose)
✓ Text-to-speech functionality for enhanced accessibility
✓ Hint system (3 hints per game, reveals random unguessed letters)
✓ Multilingual support (English, Spanish, French, German)
✓ Custom word input option
✓ Win/loss tracking and statistics
✓ Graceful degradation when audio hardware is unavailable

## How to Play
1. Run the game (it starts automatically in VNC mode)
2. Click "New Game" to start
3. Select your preferred language and difficulty level
4. Optionally choose to enter a custom word
5. Click letter buttons to guess
6. Use hints when you're stuck (limited to 3 per game)
7. Win by guessing all letters before running out of attempts (6 wrong guesses allowed)

## Dependencies
- Python 3.11
- Tkinter (built-in) - GUI framework
- pygame 2.5.2 - Sound effects
- pyttsx3 2.90 - Text-to-speech
- numpy 1.26.4 - Sound wave generation

## User Preferences
None documented yet.
