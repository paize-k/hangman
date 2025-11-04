"""
Interactive Hangman Game with GUI
Features: Difficulty levels, Leaderboard, Sound effects, Text-to-speech, Hints
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import json
import os
from words import get_words, WORD_BANKS

# Try to import optional libraries
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("pygame not available - sound effects disabled")

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("pyttsx3 not available - text-to-speech disabled")


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.root.geometry("900x700")
        self.root.configure(bg="#2C3E50")
        
        # Initialize text-to-speech
        self.tts_engine = None
        if TTS_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
            except:
                print("Text-to-speech initialization failed")
        
        # Initialize pygame for sound effects
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                # Create simple sound effects
                self.create_sound_effects()
            except:
                print("Sound effects initialization failed")
        
        # Game state
        self.word = ""
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.max_wrong_guesses = 6
        self.game_active = False
        self.hints_remaining = 3
        self.difficulty = "Medium"
        self.language = "English"
        self.custom_word_mode = False
        
        # Load leaderboard
        self.load_leaderboard()
        
        # Create UI
        self.create_widgets()
        
    def create_sound_effects(self):
        """Create simple sound effects using pygame"""
        try:
            # We'll use simple beep sounds since we can't load external files
            self.sound_correct = None
            self.sound_wrong = None
            self.sound_win = None
            self.sound_lose = None
        except:
            pass
    
    def speak(self, text):
        """Text-to-speech function"""
        if self.tts_engine:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except:
                pass
    
    def play_sound(self, sound_type):
        """Play sound effect"""
        if not PYGAME_AVAILABLE:
            return
        # Placeholder for sound effects
        # In a full implementation, you would load actual sound files here
    
    def load_leaderboard(self):
        """Load leaderboard from JSON file"""
        try:
            with open('leaderboard.json', 'r') as f:
                self.leaderboard = json.load(f)
        except FileNotFoundError:
            self.leaderboard = {'games_won': 0, 'games_lost': 0, 'total_games': 0}
            self.save_leaderboard()
    
    def save_leaderboard(self):
        """Save leaderboard to JSON file"""
        with open('leaderboard.json', 'w') as f:
            json.dump(self.leaderboard, f, indent=4)
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Title
        title_label = tk.Label(
            self.root, 
            text="🎮 HANGMAN GAME 🎮", 
            font=("Arial", 28, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        )
        title_label.pack(pady=20)
        
        # Main game frame
        game_frame = tk.Frame(self.root, bg="#2C3E50")
        game_frame.pack(pady=10)
        
        # Left side - Hangman drawing
        self.canvas = tk.Canvas(
            game_frame,
            width=300,
            height=350,
            bg="#34495E",
            highlightthickness=2,
            highlightbackground="#ECF0F1"
        )
        self.canvas.grid(row=0, column=0, padx=20)
        
        # Right side - Game info
        info_frame = tk.Frame(game_frame, bg="#2C3E50")
        info_frame.grid(row=0, column=1, padx=20, sticky="n")
        
        # Word display
        self.word_label = tk.Label(
            info_frame,
            text="_ _ _ _ _",
            font=("Courier", 32, "bold"),
            bg="#2C3E50",
            fg="#3498DB"
        )
        self.word_label.pack(pady=20)
        
        # Stats display
        self.stats_label = tk.Label(
            info_frame,
            text="Wrong Guesses: 0/6\nHints Remaining: 3",
            font=("Arial", 14),
            bg="#2C3E50",
            fg="#ECF0F1",
            justify="left"
        )
        self.stats_label.pack(pady=10)
        
        # Guessed letters display
        self.guessed_label = tk.Label(
            info_frame,
            text="Guessed: ",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#95A5A6"
        )
        self.guessed_label.pack(pady=10)
        
        # Letter buttons frame
        self.buttons_frame = tk.Frame(info_frame, bg="#2C3E50")
        self.buttons_frame.pack(pady=20)
        
        self.letter_buttons = {}
        self.create_letter_buttons()
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg="#2C3E50")
        control_frame.pack(pady=20)
        
        self.hint_button = tk.Button(
            control_frame,
            text="💡 Use Hint",
            command=self.use_hint,
            font=("Arial", 12, "bold"),
            bg="#F39C12",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        self.hint_button.grid(row=0, column=0, padx=5)
        
        new_game_button = tk.Button(
            control_frame,
            text="🎯 New Game",
            command=self.show_game_setup,
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        new_game_button.grid(row=0, column=1, padx=5)
        
        leaderboard_button = tk.Button(
            control_frame,
            text="🏆 Leaderboard",
            command=self.show_leaderboard,
            font=("Arial", 12, "bold"),
            bg="#9B59B6",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        leaderboard_button.grid(row=0, column=2, padx=5)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="Click 'New Game' to start!",
            font=("Arial", 11),
            bg="#34495E",
            fg="#ECF0F1",
            pady=10
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_letter_buttons(self):
        """Create A-Z letter buttons"""
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i, letter in enumerate(letters):
            row = i // 9
            col = i % 9
            btn = tk.Button(
                self.buttons_frame,
                text=letter,
                width=3,
                height=1,
                font=("Arial", 10, "bold"),
                bg="#3498DB",
                fg="white",
                command=lambda l=letter: self.guess_letter(l),
                cursor="hand2"
            )
            btn.grid(row=row, column=col, padx=2, pady=2)
            self.letter_buttons[letter] = btn
    
    def show_game_setup(self):
        """Show game setup dialog"""
        setup_window = tk.Toplevel(self.root)
        setup_window.title("New Game Setup")
        setup_window.geometry("400x350")
        setup_window.configure(bg="#2C3E50")
        setup_window.transient(self.root)
        setup_window.grab_set()
        
        tk.Label(
            setup_window,
            text="Game Setup",
            font=("Arial", 18, "bold"),
            bg="#2C3E50",
            fg="#ECF0F1"
        ).pack(pady=20)
        
        # Language selection
        tk.Label(
            setup_window,
            text="Select Language:",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#ECF0F1"
        ).pack(pady=5)
        
        language_var = tk.StringVar(value=self.language)
        languages = list(WORD_BANKS.keys())
        language_combo = ttk.Combobox(
            setup_window,
            textvariable=language_var,
            values=languages,
            state="readonly",
            font=("Arial", 11)
        )
        language_combo.pack(pady=5)
        
        # Difficulty selection
        tk.Label(
            setup_window,
            text="Select Difficulty:",
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#ECF0F1"
        ).pack(pady=5)
        
        difficulty_var = tk.StringVar(value=self.difficulty)
        difficulties = ["Easy", "Medium", "Hard"]
        for diff in difficulties:
            tk.Radiobutton(
                setup_window,
                text=diff,
                variable=difficulty_var,
                value=diff,
                font=("Arial", 11),
                bg="#2C3E50",
                fg="#ECF0F1",
                selectcolor="#34495E"
            ).pack()
        
        # Custom word option
        custom_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            setup_window,
            text="Enter Custom Word",
            variable=custom_var,
            font=("Arial", 11),
            bg="#2C3E50",
            fg="#ECF0F1",
            selectcolor="#34495E"
        ).pack(pady=10)
        
        def start_game():
            self.language = language_var.get()
            self.difficulty = difficulty_var.get()
            self.custom_word_mode = custom_var.get()
            
            if self.custom_word_mode:
                custom_word = simpledialog.askstring(
                    "Custom Word",
                    "Enter a word for your opponent to guess:",
                    parent=setup_window
                )
                if custom_word and custom_word.isalpha():
                    self.word = custom_word.upper()
                    setup_window.destroy()
                    self.start_new_game()
                else:
                    messagebox.showerror("Error", "Please enter a valid word (letters only)")
            else:
                setup_window.destroy()
                self.start_new_game()
        
        tk.Button(
            setup_window,
            text="Start Game",
            command=start_game,
            font=("Arial", 12, "bold"),
            bg="#27AE60",
            fg="white",
            padx=20,
            pady=10
        ).pack(pady=20)
    
    def start_new_game(self):
        """Start a new game"""
        # Select word if not custom
        if not self.custom_word_mode:
            words = get_words(self.language, self.difficulty)
            self.word = random.choice(words).upper()
        
        # Reset game state
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.hints_remaining = 3
        self.game_active = True
        
        # Reset UI
        self.update_word_display()
        self.update_stats()
        self.draw_hangman()
        self.guessed_label.config(text="Guessed: ")
        
        # Enable all letter buttons
        for btn in self.letter_buttons.values():
            btn.config(state=tk.NORMAL, bg="#3498DB")
        
        self.hint_button.config(state=tk.NORMAL)
        self.status_label.config(text=f"Game started! Difficulty: {self.difficulty} | Language: {self.language}")
        
        if self.tts_engine:
            self.speak(f"New game started. Difficulty: {self.difficulty}")
    
    def guess_letter(self, letter):
        """Handle letter guess"""
        if not self.game_active:
            messagebox.showinfo("Info", "Please start a new game first!")
            return
        
        if letter in self.guessed_letters:
            return
        
        self.guessed_letters.add(letter)
        self.letter_buttons[letter].config(state=tk.DISABLED, bg="#7F8C8D")
        
        if letter in self.word:
            # Correct guess
            self.letter_buttons[letter].config(bg="#27AE60")
            self.status_label.config(text=f"✓ Great! '{letter}' is in the word!", fg="#2ECC71")
            self.play_sound("correct")
            if self.tts_engine:
                self.speak(f"Correct! {letter}")
        else:
            # Wrong guess
            self.wrong_guesses += 1
            self.letter_buttons[letter].config(bg="#E74C3C")
            self.status_label.config(text=f"✗ Sorry, '{letter}' is not in the word.", fg="#E74C3C")
            self.play_sound("wrong")
            if self.tts_engine:
                self.speak(f"Wrong! {letter}")
        
        self.update_word_display()
        self.update_stats()
        self.update_guessed_letters()
        self.draw_hangman()
        self.check_game_over()
    
    def use_hint(self):
        """Use a hint to reveal a random letter"""
        if not self.game_active:
            return
        
        if self.hints_remaining <= 0:
            messagebox.showinfo("No Hints", "You have no hints remaining!")
            return
        
        # Find unguessed letters in the word
        unguessed = [l for l in set(self.word) if l not in self.guessed_letters]
        
        if not unguessed:
            messagebox.showinfo("Hint", "You've already guessed all the letters!")
            return
        
        # Reveal a random unguessed letter
        hint_letter = random.choice(unguessed)
        self.hints_remaining -= 1
        self.guess_letter(hint_letter)
        
        if self.tts_engine:
            self.speak(f"Hint used. The letter {hint_letter} is in the word.")
    
    def update_word_display(self):
        """Update the word display with guessed letters"""
        display = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])
        self.word_label.config(text=display)
    
    def update_stats(self):
        """Update stats display"""
        self.stats_label.config(
            text=f"Wrong Guesses: {self.wrong_guesses}/{self.max_wrong_guesses}\nHints Remaining: {self.hints_remaining}"
        )
        
        if self.hints_remaining <= 0:
            self.hint_button.config(state=tk.DISABLED)
    
    def update_guessed_letters(self):
        """Update guessed letters display"""
        guessed_sorted = sorted(list(self.guessed_letters))
        self.guessed_label.config(text=f"Guessed: {', '.join(guessed_sorted)}")
    
    def draw_hangman(self):
        """Draw hangman based on wrong guesses"""
        self.canvas.delete("all")
        
        # Draw gallows
        self.canvas.create_line(50, 330, 250, 330, width=3, fill="#ECF0F1")  # Base
        self.canvas.create_line(100, 330, 100, 50, width=3, fill="#ECF0F1")  # Pole
        self.canvas.create_line(100, 50, 200, 50, width=3, fill="#ECF0F1")  # Top
        self.canvas.create_line(200, 50, 200, 80, width=3, fill="#ECF0F1")  # Rope
        
        # Draw hangman parts based on wrong guesses
        if self.wrong_guesses >= 1:
            # Head
            self.canvas.create_oval(175, 80, 225, 130, width=3, outline="#E74C3C")
        
        if self.wrong_guesses >= 2:
            # Body
            self.canvas.create_line(200, 130, 200, 200, width=3, fill="#E74C3C")
        
        if self.wrong_guesses >= 3:
            # Left arm
            self.canvas.create_line(200, 150, 170, 180, width=3, fill="#E74C3C")
        
        if self.wrong_guesses >= 4:
            # Right arm
            self.canvas.create_line(200, 150, 230, 180, width=3, fill="#E74C3C")
        
        if self.wrong_guesses >= 5:
            # Left leg
            self.canvas.create_line(200, 200, 170, 250, width=3, fill="#E74C3C")
        
        if self.wrong_guesses >= 6:
            # Right leg
            self.canvas.create_line(200, 200, 230, 250, width=3, fill="#E74C3C")
    
    def check_game_over(self):
        """Check if game is won or lost"""
        # Check win
        if all(letter in self.guessed_letters for letter in self.word):
            self.game_active = False
            self.leaderboard['games_won'] += 1
            self.leaderboard['total_games'] += 1
            self.save_leaderboard()
            
            self.status_label.config(text=f"🎉 YOU WIN! The word was: {self.word}", fg="#2ECC71")
            self.word_label.config(fg="#2ECC71")
            self.play_sound("win")
            
            if self.tts_engine:
                self.speak(f"Congratulations! You won! The word was {self.word}")
            
            messagebox.showinfo("Winner!", f"🎉 Congratulations! You won!\n\nThe word was: {self.word}\n\nGames Won: {self.leaderboard['games_won']}\nGames Lost: {self.leaderboard['games_lost']}")
            return
        
        # Check loss
        if self.wrong_guesses >= self.max_wrong_guesses:
            self.game_active = False
            self.leaderboard['games_lost'] += 1
            self.leaderboard['total_games'] += 1
            self.save_leaderboard()
            
            self.status_label.config(text=f"💀 GAME OVER! The word was: {self.word}", fg="#E74C3C")
            self.word_label.config(text=" ".join(self.word), fg="#E74C3C")
            self.play_sound("lose")
            
            if self.tts_engine:
                self.speak(f"Game over! The word was {self.word}")
            
            # Disable all buttons
            for btn in self.letter_buttons.values():
                btn.config(state=tk.DISABLED)
            
            messagebox.showinfo("Game Over", f"💀 Game Over!\n\nThe word was: {self.word}\n\nGames Won: {self.leaderboard['games_won']}\nGames Lost: {self.leaderboard['games_lost']}")
    
    def show_leaderboard(self):
        """Show leaderboard window"""
        lb_window = tk.Toplevel(self.root)
        lb_window.title("Leaderboard")
        lb_window.geometry("350x250")
        lb_window.configure(bg="#2C3E50")
        lb_window.transient(self.root)
        
        tk.Label(
            lb_window,
            text="🏆 LEADERBOARD 🏆",
            font=("Arial", 18, "bold"),
            bg="#2C3E50",
            fg="#F39C12"
        ).pack(pady=20)
        
        stats_text = f"""
        Total Games Played: {self.leaderboard['total_games']}
        
        Games Won: {self.leaderboard['games_won']}
        Games Lost: {self.leaderboard['games_lost']}
        
        Win Rate: {(self.leaderboard['games_won'] / max(1, self.leaderboard['total_games']) * 100):.1f}%
        """
        
        tk.Label(
            lb_window,
            text=stats_text,
            font=("Arial", 12),
            bg="#2C3E50",
            fg="#ECF0F1",
            justify="left"
        ).pack(pady=10)
        
        tk.Button(
            lb_window,
            text="Close",
            command=lb_window.destroy,
            font=("Arial", 11, "bold"),
            bg="#E74C3C",
            fg="white",
            padx=20,
            pady=5
        ).pack(pady=10)


def main():
    root = tk.Tk()
    app = HangmanGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
