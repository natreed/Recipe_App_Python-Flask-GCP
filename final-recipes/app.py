from flask import Flask, render_template, request, redirect, url_for
import gbmodel
from flask_gtts import gtts
from google.cloud import texttospeech
from google.cloud import storage
from google.cloud import translate
import six
from gtts import gTTS
from gtts import gTTSError
import io
from io import BytesIO
import os
from collections import OrderedDict


app = Flask(__name__, template_folder="templates")
gtts(app)
CLOUD_STORAGE_BUCKET = 'cs510c-natreed'


@app.route('/')
@app.route('/index')
def index():
    return render_template('/index.html')


@app.route('/recipes', methods=['POST'])
def get_recipes():
    """Prints all of the recipes in database.""" 
   
    model = gbmodel.get_model()
    entries = [OrderedDict(title=row[0],
                           author=row[1],
                           ingredients=row[2],
                           instructions=(row[3]))
               for row in model.select()]

    return render_template('/recipes.html', entries=entries)


@app.route('/recipes_spanish', methods=['POST'])
def get_recipes_spanish():
    """
    Prints all of the recipes in database. Renders recipe page in spanish.
    :return:
    """
    model = gbmodel.get_model()

    entries = []

    for row in model.select():
        title_sp = translate_text('es', "title")
        aut_sp = translate_text('es', "author")
        ing_sp = translate_text('es', "ingredients")
        inst_sp = translate_text('es', "instructions")

        d = OrderedDict()
        d[title_sp] = translate_text('es', row[0])
        d[aut_sp] = translate_text('es', row[1])
        d[ing_sp] = translate_text('es', row[2])
        d[inst_sp] = translate_text('es', row[3])

        entries.append(d)

    return render_template('/recipes_spanish.html', entries=entries)


@app.route('/last_recipe_audio', methods=['POST', 'GET'])
def recipe_audio():
    """Redirects user to recipe submission audio page.
    Entry is not yet stored because there is no backend.
    :return renders recipe submission form"""
    return render_template('/last_entry_audio.html')


@app.route('/recipe_submission', methods=['POST'])
def submit_recipes():
    """Redirects user to recipe submission page.
    Entry is not yet stored because there is no backend.
    :return renders recipe submission form"""
    return render_template('/recipe_submission.html')


# https://www.tutorialspoint.com/flask/flask_sqlite.htm
@app.route('/add_recipe', methods=['POST', 'GET'])
def add_recipe():
    """Adds recipe to database. Uploads recipe text as sound to gcs bucket.
    :return after recipe entry, takes user back to landing page"""
    model = gbmodel.get_model()
    model.insert(request.form['title'],
                 request.form['author'],
                 request.form['ingredients'],
                 request.form['instructions'])

    audio_records = {"title": synthesize_text(request.form['title']),
                     "author": synthesize_text(request.form['author']),
                     "ingredients": synthesize_text(request.form['ingredients']),
                     "instructions": synthesize_text(request.form['instructions'])
                     }

    audio_urls = {}

    """This is where """
    for filename, record in audio_records.items():
        url = upload_mp3_to_bucket(record, filename + '.mp3')
        audio_urls[filename] = url

    return render_template('/index.html')


"""GOOGLE TEXT TO SPEECH API
Source = https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/texttospeech/cloud-client/synthesize_text.py
"""
def synthesize_text(text):
    """
    Uses google text to speech API to synthesize a text string and stores in mp3 format.
    :param text:
    :return mp3 audio content:
    """
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.types.SynthesisInput(text=text)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(input_text, voice, audio_config)

    return response.audio_content


"""CLOUD STORAGE API
Source = https://cloud.google.com/appengine/docs/flexible/python/using-cloud-storage
"""
def upload_mp3_to_bucket(mp3_data, filename):
    """
    Uploads mp3 data to file in google storage bucket. Uses google cloud storage
    API for python.
    :param mp3_data:
    :param filename:
    :return: returns the public_url of the gcs file
    """
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(filename)

    blob.upload_from_string(
        mp3_data,
        content_type="audio/mpeg"
    )

    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url


"""GOOGLE TRANSLATE API
Source = https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/translate/cloud-client/snippets.py
"""
def translate_text(target, text):
    """
    Translates text to target language
    :param target:
    :param text:
    :return:
    """
    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

        # Text can also be a sequence of strings, in which case this method
        # will return a sequence of results for each text.
    result = translate_client.translate(
        text, target_language=target)

    return result['translatedText']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
