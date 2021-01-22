import os.path


def html_audio_source_type(path):
    result = ''
    if path:
        filename, extension = os.path.splitext(path)
        if extension.lower().lstrip('.') == 'wav':
            return 'audio/wav'
        if extension.lower().lstrip('.') == 'mp3':
            return 'audio/mpeg'
        if extension.lower().lstrip('.') == 'ogg':
            return 'audio/ogg'

    # if we have to guess, then audio/mpeg is returned
    return 'audio/mpeg'


audio_type = html_audio_source_type('ce171495-c395-40bb-95f8-3c51e7da224c.wav')
print(audio_type)


