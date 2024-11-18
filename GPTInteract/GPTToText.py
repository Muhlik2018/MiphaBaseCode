from openai import OpenAI
def speechToText(audio_filepath,key=''):
  client=OpenAI(api_key=key)

  audio_file= open(audio_filepath, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
  )
  audio_file.close()
  print(transcription.text)
  return transcription.text
