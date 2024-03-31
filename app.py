from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio']
    language = request.form.get('language')

    # Création d'un objet recognizer
    recognizer = sr.Recognizer()

    # Lecture de l'audio
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    # Transcription de l'audio en texte
    try:
        if language == 'en':
            transcript = recognizer.recognize_google(audio_data, language="en-US")
        elif language == 'fr':
            transcript = recognizer.recognize_google(audio_data, language="fr-FR")
        else:
            return jsonify({'error': 'Invalid language selected'})

        # Envoyer la réponse avec le texte transcrit
        return jsonify({'transcript': transcript})
    except sr.UnknownValueError:
        return jsonify({'error': 'Unable to transcribe the audio'})


if __name__ == '__main__':
    app.run(debug=True)
