# disabled ffmpeg not installed warning
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

from pydub import AudioSegment 
from pydub.generators import Sine , WhiteNoise, Square
from pydub.playback import play
import numpy as np
import pyaudio

from . import common

__all__ = [ 
            '正弦波', '播放聲音', '方波', '白噪音', '開啟wav檔', '多維陣列轉換', '設置聲音擷取', '擷取聲音',
             'play', '播放', '聲音轉陣列'
            ]

# init
#common.speaker = win32com.client.Dispatch("SAPI.SpVoice")


# patch AudioSegment chinese methods
AudioSegment.淡出 = AudioSegment.fade_out
AudioSegment.淡入 = AudioSegment.fade_in
AudioSegment.反轉 = AudioSegment.reverse

def 串接(self, seg, 交叉淡化=100):
    return self.append(seg, crossfade=交叉淡化)
AudioSegment.串接 = 串接


def 儲存wav檔(self, filename):
    self.export(filename, format='wav')
AudioSegment.儲存wav檔 = 儲存wav檔

# patch AudioSegment chinese attributes
@property
def 取樣率(self):
    return self.frame_rate
AudioSegment.取樣率 = 取樣率

@property
def 位元深度(self):
    return self.frame_width
AudioSegment.位元深度 = 位元深度

@property
def 秒數(self):
    return self.duration_seconds
AudioSegment.秒數 = 秒數

@property
def 取樣總數(self):
    return self.frame_count()
AudioSegment.取樣總數 = 取樣總數

@property
def 聲道數(self):
    return self.channels
AudioSegment.聲道數 = 聲道數


# def 淡出(self, 持續時間):
#     return self.fade(to_gain=-120, duration=duration, end=float('inf'))

# def 淡入(self, 持續時間):
#     return self.fade(from_gain=-120, duration=duration, start=0)



class 正弦波(Sine):
    def __init__(self, 頻率, 取樣率=44100, 位元深度=16):
        Sine.__init__(self, 頻率, sample_rate=取樣率, bit_depth=位元深度)

    def 轉成聲音(self, 持續時間=1000.0, 音量=-5.0):
        return self.to_audio_segment(duration=持續時間, volume=音量)

class 方波(Square):
    def __init__(self, 頻率, 取樣率=44100, 位元深度=16):
        Square.__init__(self, 頻率, sample_rate=取樣率, bit_depth=位元深度)

    def 轉成聲音(self, 持續時間=1000.0, 音量=-10.0):
        return self.to_audio_segment(duration=持續時間, volume=音量)

class 白噪音(WhiteNoise):
    def __init__(self, 取樣率=44100, 位元深度=16):
        WhiteNoise.__init__(self, sample_rate=取樣率, bit_depth=位元深度)

    def 轉成聲音(self, 持續時間=1000.0, 音量=-10.0):
        return self.to_audio_segment(duration=持續時間, volume=音量)


def 播放聲音(audio_segment):
    play(audio_segment)

def 播放(audio_segment):
    play(audio_segment)

def 開啟wav檔(檔名):
    return AudioSegment.from_wav(檔名)

def 多維陣列轉換(tone):
    return  np.asarray(tone.get_array_of_samples() )

def 聲音轉陣列(tone):
    return  np.asarray(tone.get_array_of_samples() )

# microphone

def 設置聲音擷取(read_chunk,取樣率=22050):
    common.read_chunk = read_chunk
    pa = pyaudio.PyAudio()
    return pa.open(format=pyaudio.paInt16, channels=1,
                 rate=取樣率, input=True, output=False,
                 frames_per_buffer=read_chunk)

def 擷取聲音(stream):
    if not common.read_chunk:
        return
    data = stream.read(common.read_chunk)
    return np.frombuffer(data, np.int16)


if __name__ == '__main__' :
    pass
    
