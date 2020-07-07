
def ConvertMp3ToWav(inname, outname):

    from pydub import AudioSegment

    sound = AudioSegment.from_mp3(inname)

    sound.export(outname, format='wav')

    return outname
