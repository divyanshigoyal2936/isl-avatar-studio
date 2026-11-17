import re
from typing import List, Tuple, Optional, Dict
from app.models.schemas import SemanticEntity, TranslateResponse

# Lexical mapping for Indian languages to English semantics
INDIAN_LEXICON = {
    # Hindi
    "नमस्ते": "hello", "नमस्कार": "hello", "प्रणाम": "hello",
    "धन्यवाद": "thank you", "शुक्रिया": "thank you",
    "स्वागत": "welcome", "स्वागतम": "welcome",
    "कृपया": "please",
    "नाम": "name", "मेरा": "my", "आपका": "your", "आप": "you", "मैं": "me", "मुझे": "me",
    "क्या": "what", "कहाँ": "where", "कहा": "where", "किधर": "where", "कैसे": "how", "कब": "when",
    "पानी": "water", "जल": "water",
    "खाना": "food", "भोजन": "food",
    "मदद": "help", "सहायता": "help",
    "अस्पताल": "hospital",
    "डॉक्टर": "doctor", "चिकित्सक": "doctor",
    "समय": "time", "वक्त": "time",
    "आज": "today", "सुबह": "morning",
    "अच्छा": "good", "बहुत": "very",
    "हाँ": "yes", "जी": "yes",
    "नहीं": "no", "मत": "no",
    "भारत": "india", "हिंदुस्तान": "india",
    "मिलकर": "meet", "मिलना": "meet",
    
    # Tamil
    "வணக்கம்": "hello", "நன்றி": "thank you", "தயவுசெய்து": "please",
    "பெயர்": "name", "நீங்கள்": "you", "நான்": "me", "எனக்கு": "me",
    "என்ன": "what", "எங்கே": "where", "எப்படி": "how", "எப்போது": "when",
    "தண்ணீர்": "water", "உணவு": "food", "உதவி": "help",
    "மருத்துவமனை": "hospital", "மருத்துவர்": "doctor",
    "இன்று": "today", "காலை": "morning", "நல்ல": "good", "இல்லை": "no",
    "இந்தியா": "india",

    # Telugu
    "నమస్కారం": "hello", "ధన్యవాదాలు": "thank you", "దయచేసి": "please",
    "పేరు": "name", "మీరు": "you", "నేను": "me", "నాకు": "me",
    "ఏమిటి": "what", "ఎక్కడ": "where", "ఎలా": "how", "ఎప్పుడు": "when",
    "నీరు": "water", "భోజనం": "food", "సహాయం": "help",
    "ఆసుపత్రి": "hospital", "వైద్యుడు": "doctor",
    "ఈరోజు": "today", "ఉదయం": "morning", "మంచి": "good", "లేదు": "no",
    "భారతదేశం": "india",

    # Bengali
    "নমস্কার": "hello", "ধন্যবাদ": "thank you", "দয়া করে": "please",
    "নাম": "name", "আপনি": "you", "আমি": "me", "আমাকে": "me",
    "কী": "what", "কোথায়": "where", "কেমন": "how",
    "জল": "water", "খাবার": "food", "সাহায্য": "help",
    "হাসপাতাল": "hospital", "ডাক্তার": "doctor",
    "আজ": "today", "সকাল": "morning", "ভালো": "good", "না": "no",
    "ভারত": "india",

    # Marathi
    "नमस्कार": "hello", "धन्यवाद": "thank you", "कृपया": "please",
    "नाव": "name", "तुम्ही": "you", "मी": "me", "मला": "me",
    "काय": "what", "कुठे": "where", "कसे": "how",
    "पाणी": "water", "जेवण": "food", "मदत": "help",
    "रुग्णालय": "hospital", "डॉक्टर": "doctor",
    "आज": "today", "सकाळ": "morning", "चांगले": "good", "नाही": "no",
    "भारत": "india"
}

SUPPORTED_LANGUAGES_CATALOG = [
    {"code": "en", "name": "English", "native_name": "English", "stt_status": "verified", "translation_status": "native"},
    {"code": "hi", "name": "Hindi", "native_name": "हिन्दी", "stt_status": "verified", "translation_status": "verified"},
    {"code": "ta", "name": "Tamil", "native_name": "தமிழ்", "stt_status": "supported", "translation_status": "supported"},
    {"code": "te", "name": "Telugu", "native_name": "తెలుగు", "stt_status": "supported", "translation_status": "supported"},
    {"code": "bn", "name": "Bengali", "native_name": "বাংলা", "stt_status": "supported", "translation_status": "supported"},
    {"code": "mr", "name": "Marathi", "native_name": "मराठी", "stt_status": "supported", "translation_status": "supported"},
    {"code": "gu", "name": "Gujarati", "native_name": "ગુજરાતી", "stt_status": "supported", "translation_status": "supported"},
    {"code": "kn", "name": "Kannada", "native_name": "ಕನ್ನಡ", "stt_status": "supported", "translation_status": "supported"},
    {"code": "ml", "name": "Malayalam", "native_name": "മലയാളം", "stt_status": "supported", "translation_status": "supported"},
    {"code": "pa", "name": "Punjabi", "native_name": "ਪੰਜਾਬੀ", "stt_status": "supported", "translation_status": "supported"}
]

class TranslationService:
    def detect_language(self, text: str) -> str:
        for char in text:
            cp = ord(char)
            if 0x0900 <= cp <= 0x097F:
                # Devanagari (Hindi / Marathi)
                if any(w in text for w in ["आहे", "मला", "नाव", "करा", "कुठे", "नाही"]):
                    return "mr"
                return "hi"
            elif 0x0B80 <= cp <= 0x0BFF:
                return "ta"
            elif 0x0C00 <= cp <= 0x0C7F:
                return "te"
            elif 0x0980 <= cp <= 0x09FF:
                return "bn"
            elif 0x0A80 <= cp <= 0x0AFF:
                return "gu"
            elif 0x0C80 <= cp <= 0x0CFF:
                return "kn"
            elif 0x0D00 <= cp <= 0x0D7F:
                return "ml"
            elif 0x0A00 <= cp <= 0x0A7F:
                return "pa"
        return "en"

    def normalize_and_analyze(self, text: str, source_language: Optional[str] = "auto") -> TranslateResponse:
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValueError("Input text cannot be empty.")

        # Detect or use hint
        detected_lang = source_language if source_language and source_language != "auto" else self.detect_language(cleaned_text)

        # Tokenize and normalize
        tokens = re.findall(r"[\w]+|[^\s\w]", cleaned_text.lower(), re.UNICODE)
        
        normalized_words = []
        entities: List[SemanticEntity] = []
        has_question = False
        has_negation = False
        time_marker = None

        # Check question punctuation
        if "?" in cleaned_text or any(q in cleaned_text for q in ["क्या", "कहाँ", "कैसे", "कब", "எங்கே", "என்ன", "ఎక్కడ", "ఏమిటి", "কী", "কোথায়", "कुठे", "काय"]):
            has_question = True

        # Check negation keywords directly in text
        if any(neg in cleaned_text for neg in ["नहीं", "नाही", "இல்லை", "లేదు", "না", "no", "not", "never", "cannot"]):
            has_negation = True

        # Punctuation-safe tokenization
        cleaned_punct = re.sub(r"[?!.,;:\"'()[\]{}]", " ", cleaned_text.lower())
        tokens = [w.strip() for w in cleaned_punct.split() if w.strip()]
        for token in tokens:
            word_en = INDIAN_LEXICON.get(token, token)
            
            # Identify time expressions
            if word_en in ["today", "morning", "now", "yesterday", "tomorrow", "time"]:
                time_marker = word_en.upper()
                entities.append(SemanticEntity(entity_type="TIME", text=token, isl_role=f"[TIME: {time_marker}]"))
                normalized_words.append(word_en)
            # Identify question words
            elif word_en in ["what", "where", "how", "when", "who", "why"]:
                has_question = True
                entities.append(SemanticEntity(entity_type="QUESTION", text=token, isl_role=f"[QUESTION: {word_en.upper()}]"))
                normalized_words.append(word_en)
            # Identify negations
            elif word_en in ["no", "not", "never", "cannot", "don't"]:
                has_negation = True
                entities.append(SemanticEntity(entity_type="NEGATION", text=token, isl_role="[NEG: NO]"))
                normalized_words.append(word_en)
            # Identify common entities
            elif word_en in ["hospital", "doctor", "water", "food", "help", "india", "name", "school"]:
                entities.append(SemanticEntity(entity_type="OBJECT", text=token, isl_role=f"[ENTITY: {word_en.upper()}]"))
                normalized_words.append(word_en)
            elif word_en in ["you", "your", "me", "my", "i", "we"]:
                entities.append(SemanticEntity(entity_type="SUBJECT", text=token, isl_role=f"[PERSON: {word_en.upper()}]"))
                normalized_words.append(word_en)
            elif word_en in ["hello", "namaste", "thank you", "thanks", "welcome", "please", "good", "meet"]:
                entities.append(SemanticEntity(entity_type="ACTION", text=token, isl_role=f"[COMM: {word_en.upper()}]"))
                normalized_words.append(word_en)
            elif word_en.isalnum():
                normalized_words.append(word_en)

        normalized_sentence = " ".join(normalized_words) if normalized_words else cleaned_text.lower()
        
        # Clean extra spaces
        normalized_sentence = re.sub(r"\s+", " ", normalized_sentence).strip()

        return TranslateResponse(
            original_text=cleaned_text,
            detected_language=detected_lang,
            normalized_english=normalized_sentence,
            entities=entities,
            has_question=has_question,
            has_negation=has_negation,
            time_marker=time_marker
        )

translation_service = TranslationService()
