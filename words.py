"""
Word banks for Hangman game organized by difficulty and language
"""

WORD_BANKS = {
    "English": {
        "Easy": [
            "cat", "dog", "fish", "bird", "tree", "book", "cake", "ball",
            "sun", "moon", "star", "rain", "snow", "wind", "love", "hope",
            "gift", "play", "jump", "swim", "sing", "dance", "sleep", "eat"
        ],
        "Medium": [
            "python", "computer", "keyboard", "monitor", "science", "mathematics",
            "history", "geography", "elephant", "giraffe", "butterfly", "mountain",
            "ocean", "river", "forest", "desert", "volcano", "planet", "galaxy",
            "rainbow", "thunder", "lightning", "awesome", "wonderful", "beautiful"
        ],
        "Hard": [
            "algorithm", "encryption", "repository", "chromosome", "metamorphosis",
            "photosynthesis", "extraordinary", "circumstantial", "acknowledge",
            "pharmaceutical", "czechoslovakia", "xylophone", "kaleidoscope",
            "onomatopoeia", "simultaneously", "labyrinth", "phenomenon", "equilibrium",
            "protagonist", "anonymous", "sophisticated", "enthusiastic", "revolutionary"
        ]
    },
    "Spanish": {
        "Easy": [
            "casa", "perro", "gato", "sol", "luna", "amor", "agua", "libro",
            "mesa", "silla", "vida", "noche", "dia", "luz", "paz"
        ],
        "Medium": [
            "computadora", "biblioteca", "universidad", "hospital", "restaurante",
            "automovil", "telefono", "television", "musica", "cultura",
            "naturaleza", "montana", "oceano", "planeta"
        ],
        "Hard": [
            "extraordinario", "internacional", "revolucionario", "arquitectura",
            "comunicacion", "tecnologia", "filosofia", "democracia",
            "responsabilidad", "caracteristicas", "investigacion"
        ]
    },
    "French": {
        "Easy": [
            "chat", "chien", "maison", "livre", "soleil", "lune", "eau",
            "pain", "fromage", "amour", "vie", "nuit", "jour"
        ],
        "Medium": [
            "ordinateur", "bibliotheque", "universite", "restaurant",
            "telephone", "musique", "montagne", "nature", "culture",
            "histoire", "geographie", "science"
        ],
        "Hard": [
            "extraordinaire", "internationale", "revolutionnaire",
            "architecture", "communication", "technologie", "philosophie",
            "responsabilite", "caracteristiques", "developpement"
        ]
    },
    "German": {
        "Easy": [
            "katze", "hund", "haus", "buch", "sonne", "mond", "wasser",
            "brot", "liebe", "leben", "nacht", "tag", "licht"
        ],
        "Medium": [
            "computer", "bibliothek", "universitat", "restaurant",
            "telefon", "musik", "berg", "natur", "kultur",
            "geschichte", "wissenschaft", "geographie"
        ],
        "Hard": [
            "aussergewohnlich", "international", "revolutionar",
            "architektur", "kommunikation", "technologie", "philosophie",
            "verantwortung", "eigenschaften", "entwicklung"
        ]
    }
}

def get_words(language="English", difficulty="Medium"):
    """Get word list for specified language and difficulty"""
    return WORD_BANKS.get(language, WORD_BANKS["English"]).get(difficulty, WORD_BANKS["English"]["Medium"])
