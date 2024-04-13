from flask import Flask, request, jsonify
from gtts import gTTS
from translate import Translator
from io import BytesIO

app = Flask(__name__)

def text_to_speech(text, lang='en'):
    tts = gTTS(text, lang=lang)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

def translate_text(source_lang, target_lang, text):
    translator = Translator(from_lang=source_lang, to_lang=target_lang)
    translation = translator.translate(text)
    return translation


@app.route('/api/translate', methods=['POST'])
def api_translate():
    data = request.json
    
    if data is None:
        return jsonify({'error': 'Failed to decode JSON object'}), 400

    source_lang = data.get('source_lang')
    target_lang = data.get('target_lang')
    text = data.get('text')

    if not all([source_lang, target_lang, text]):
        return jsonify({'error': 'Missing required parameters'}), 400

    translation = translate_text(source_lang, target_lang, text)
    audio_bytes = text_to_speech(translation, lang=target_lang)
    
    return jsonify({'translation': translation, 'audio': audio_bytes.read().decode('latin-1')}), 200

if __name__ == '__main__':
    app.run(debug=True)
