import subprocess
import platform
from gtts import gTTS
from pydub import AudioSegment
def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"
    os_name = platform.system()
    try:
        audioobj = gTTS(text=input_text, lang=language, slow=False)
        audioobj.save(output_filepath) 
        output_filepath_wav = output_filepath.replace(".mp3", ".wav")
        AudioSegment.from_mp3(output_filepath).export(output_filepath_wav, format="wav")
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath_wav])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath_wav}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['ffplay','-nodisp', '-autoexit', output_filepath_wav])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
        return output_filepath
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")
        return None


#input_text="Hi this is Sandip Roy, autoplay testing!"
#text_to_speech_with_gtts(input_text=input_text, output_filepath="generated/gtts_testing_autoplay.mp3")