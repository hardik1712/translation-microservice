import random

class MockGoogleTranslate:
    def __init__(self):
        self.translations = {
            "en": {
                "hello": {"hi": "नमस्ते", "ta": "வணக்கம்", "kn": "ನಮಸ್ಕಾರ", "bn": "নমস্কার"},
                "goodbye": {"hi": "अलविदा", "ta": "பிரியாவிடை", "kn": "ವಿದಾಯ", "bn": "বিদায়"},
                "thank you": {"hi": "धन्यवाद", "ta": "நன்றி", "kn": "ಧನ್ಯವಾದಗಳು", "bn": "ধন্যবাদ"},
                "good morning": {"hi": "शुभ प्रभात", "ta": "காலை வணக்கம்", "kn": "ಶುಭೋದಯ", "bn": "সুপ্রভাত"},
                "good night": {"hi": "शुभ रात्रि", "ta": "இனிய இரவு", "kn": "ಶುಭ ರಾತ್ರಿ", "bn": "শুভ রাত্রি"},
                "how are you": {"hi": "आप कैसे हैं", "ta": "நீங்கள் எப்படி இருக்கிறீர்கள்", "kn": "ನೀವು ಹೇಗಿದ್ದೀರಿ", "bn": "আপনি কেমন আছেন"},
                "please": {"hi": "कृपया", "ta": "தயவு செய்து", "kn": "ದಯವಿಟ್ಟು", "bn": "দয়া করে"},
                "sorry": {"hi": "माफ़ कीजिये", "ta": "மன்னிக்கவும்", "kn": "ಕ್ಷಮಿಸಿ", "bn": "ক্ষমা করুন"},
                "yes": {"hi": "हाँ", "ta": "ஆம்", "kn": "ಹೌದು", "bn": "হ্যাঁ"},
                "no": {"hi": "नहीं", "ta": "இல்லை", "kn": "ಇಲ್ಲ", "bn": "না"},
                "i": {"hi": "मैं", "ta": "நான்", "kn": "ನಾನು", "bn": "আমি"},
                "you": {"hi": "आप", "ta": "நீங்கள்", "kn": "ನೀವು", "bn": "আপনি"},
                "am": {"hi": "हूँ", "ta": "இருக்கிறேன்", "kn": "ಇದ್ದೇನೆ", "bn": "আছি"},
                "is": {"hi": "है", "ta": "இருக்கிறது", "kn": "ಇದೆ", "bn": "আছে"},
                "are": {"hi": "हैं", "ta": "இருக்கிறீர்கள்", "kn": "ಇದ್ದೀರಿ", "bn": "আছেন"},
                "good": {"hi": "अच्छा", "ta": "நல்ல", "kn": "ಒಳ್ಳೆಯ", "bn": "ভাল"},
                "fine": {"hi": "ठीक", "ta": "நன்றாக", "kn": "ಚೆನ್ನಾಗಿ", "bn": "ভাল"},
                "happy": {"hi": "खुश", "ta": "மகிழ்ச்சி", "kn": "ಸಂತೋಷ", "bn": "খুশি"},
                "sad": {"hi": "दुखी", "ta": "சோகம்", "kn": "ದುಃಖ", "bn": "দুঃখী"},
                "today": {"hi": "आज", "ta": "இன்று", "kn": "ಇಂದು", "bn": "আজ"},
                "tomorrow": {"hi": "कल", "ta": "நாளை", "kn": "ನಾಳೆ", "bn": "আগামীকাল"},
                "friend": {"hi": "दोस्त", "ta": "நண்பர்", "kn": "ಸ್ನೇಹಿತ", "bn": "বন্ধু"},
                "family": {"hi": "परिवार", "ta": "குடும்பம்", "kn": "ಕುಟುಂಬ", "bn": "পরিবার"},
                "food": {"hi": "खाना", "ta": "உணவு", "kn": "ಆಹಾರ", "bn": "খাবার"},
                "water": {"hi": "पानी", "ta": "தண்ணீர்", "kn": "ನೀರು", "bn": "পানি"}
            },
            "hi": {
                "नमस्ते": "hello",
                "अलविदा": "goodbye",
                "धन्यवाद": "thank you",
                "शुभ प्रभात": "good morning",
                "शुभ रात्रि": "good night",
                "आप कैसे हैं": "how are you",
                "कृपया": "please",
                "माफ़ कीजिये": "sorry",
                "हाँ": "yes",
                "नहीं": "no",
                "मैं": "i",
                "आप": "you",
                "हूँ": "am",
                "है": "is",
                "हैं": "are",
                "अच्छा": "good",
                "ठीक": "fine",
                "खुश": "happy",
                "दुखी": "sad",
                "आज": "today",
                "कल": "tomorrow",
                "दोस्त": "friend",
                "परिवार": "family",
                "खाना": "food",
                "पानी": "water"
            },
            "ta": {
                "வணக்கம்": "hello",
                "பிரியாவிடை": "goodbye",
                "நன்றி": "thank you",
                "காலை வணக்கம்": "good morning",
                "இனிய இரவு": "good night",
                "நீங்கள் எப்படி இருக்கிறீர்கள்": "how are you",
                "தயவு செய்து": "please",
                "மன்னிக்கவும்": "sorry",
                "ஆம்": "yes",
                "இல்லை": "no",
                "நான்": "i",
                "நீங்கள்": "you",
                "இருக்கிறேன்": "am",
                "இருக்கிறது": "is",
                "இருக்கிறீர்கள்": "are",
                "நல்ல": "good",
                "நன்றாக": "fine",
                "மகிழ்ச்சி": "happy",
                "சோகம்": "sad",
                "இன்று": "today",
                "நாளை": "tomorrow",
                "நண்பர்": "friend",
                "குடும்பம்": "family",
                "உணவு": "food",
                "தண்ணீர்": "water"
            },
            "kn": {
                "ನಮಸ್ಕಾರ": "hello",
                "ವಿದಾಯ": "goodbye",
                "ಧನ್ಯವಾದಗಳು": "thank you",
                "ಶುಭೋದಯ": "good morning",
                "ಶುಭ ರಾತ್ರಿ": "good night",
                "ನೀವು ಹೇಗಿದ್ದೀರಿ": "how are you",
                "ದಯವಿಟ್ಟು": "please",
                "ಕ್ಷಮಿಸಿ": "sorry",
                "ಹೌದು": "yes",
                "ಇಲ್ಲ": "no",
                "ನಾನು": "i",
                "ನೀವು": "you",
                "ಇದ್ದೇನೆ": "am",
                "ಇದೆ": "is",
                "ಇದ್ದೀರಿ": "are",
                "ಒಳ್ಳೆಯ": "good",
                "ಚೆನ್ನಾಗಿ": "fine",
                "ಸಂತೋಷ": "happy",
                "ದುಃಖ": "sad",
                "ಇಂದು": "today",
                "ನಾಳೆ": "tomorrow",
                "ಸ್ನೇಹಿತ": "friend",
                "ಕುಟುಂಬ": "family",
                "ಆಹಾರ": "food",
                "ನೀರು": "water"
            },
            "bn": {
                "নমস্কার": "hello",
                "বিদায়": "goodbye",
                "ধন্যবাদ": "thank you",
                "সুপ্রভাত": "good morning",
                "শুভ রাত্রি": "good night",
                "আপনি কেমন আছেন": "how are you",
                "দয়া করে": "please",
                "ক্ষমা করুন": "sorry",
                "হ্যাঁ": "yes",
                "না": "no",
                "আমি": "i",
                "আপনি": "you",
                "আছি": "am",
                "আছে": "is",
                "আছেন": "are",
                "ভাল": "good",
                "ভাল": "fine",
                "খুশি": "happy",
                "দুঃখী": "sad",
                "আজ": "today",
                "আগামীকাল": "tomorrow",
                "বন্ধু": "friend",
                "পরিবার": "family",
                "খাবার": "food",
                "পানি": "water"
            }
        }

    def translate(self, text, target_language):
        # If the text is a single word or phrase that exists in our dictionary
        text = text.lower().strip()
        
        # Direct translation if available
        if text in self.translations["en"]:
            if target_language in ["hi", "ta", "kn", "bn"]:
                return self.translations["en"][text][target_language]
        
        for lang in ["hi", "ta", "kn", "bn"]:
            if text in self.translations[lang]:
                if target_language == "en":
                    return self.translations[lang][text]
                elif target_language in ["hi", "ta", "kn", "bn"]:
                    # Translate through English
                    eng = self.translations[lang][text]
                    if eng in self.translations["en"]:
                        return self.translations["en"][eng][target_language]
        
        # If the text is a sentence, try to translate word by word
        words = text.split()
        if len(words) > 1:
            translated_words = []
            for word in words:
                translated_word = self.translate(word, target_language)
                if translated_word != "Translation not available":
                    translated_words.append(translated_word)
                else:
                    # Keep original word if translation is not available
                    translated_words.append(word)
            return " ".join(translated_words)
        
        return "Translation not available"


mock_translator = MockGoogleTranslate()
