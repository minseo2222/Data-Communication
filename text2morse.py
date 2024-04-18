import sys
import math
import wave
import struct
import statistics

INTMAX = 2**(32-1)-1

english = {'A':'.-'   , 'B':'-...' , 'C':'-.-.' , 
           'D':'-..'  , 'E':'.'    , 'F':'..-.' , 
           'G':'--.'  , 'H':'....' , 'I':'..'   , 
           'J':'.---' , 'K':'-.-'  , 'L':'.-..' , 
           'M':'--'   , 'N':'-.'   , 'O':'---'  , 
           'P':'.--.' , 'Q':'--.-' , 'R':'.-.'  , 
           'S':'...'  , 'T':'-'    , 'U':'..-'  , 
           'V':'...-' , 'W':'.--'  , 'X':'-..-_', 
           'Y':'-.--' , 'Z':'--..'  }

number = { '1':'.----', '2':'..---', '3':'...--', 
           '4':'....-', '5':'.....', '6':'-....', 
           '7':'--...', '8':'---..', '9':'----.', 
           '0':'-----'}

morsecode = {
    '. -': 'A', '- . . .': 'B', '- . - .': 'C', '- . .': 'D', '.': 'E',
    '. . - .': 'F', '- - .': 'G', '. . . .': 'H', '. .': 'I', '. - - -': 'J',
    '- . -': 'K', '. - . .': 'L', '- -': 'M', '- .': 'N', '- - -': 'O',
    '. - - .': 'P', '- - . -': 'Q', '. - .': 'R', '. . .': 'S', '-': 'T',
    '. . -': 'U', '. . . -': 'V', '. - -': 'W', '- . . -': 'X', '- - . -': 'Y',
    '- - . .': 'Z',
    '. - - - -': '1', '. . - - -': '2', '. . . - -': '3', '. . . . -': '4', '. . . . .': '5',
    '- . . . .': '6', '- - . . .': '7', '- - - . .': '8', '- - - - .': '9', '- - - - -': '0'
}


def text2morse(text):
    text = text.upper()
    morse = ''

    for t in text:
        if (t==' ') :
            morse = morse + "$"
            continue
        for key, value in english.items():
            if t == key:
                morse = morse + value
        for key, value in number.items():
            if t == key:
                morse = morse + value
        morse = morse + "/" #문자사이 / 추가
    print(morse)
    return morse


def morse2audio(morse):
    t = 0.1
    fs = 48000
    f = 523.251
    audio = []
    for m in morse:
        if m == '.':
            for i in range(int(t*fs*1)):
                audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))
        elif m == '-':
            for i in range(int(t*fs*3)):
                audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))
        elif m == '/': #글자 사이일 경우
            for i in range(int(t*fs*1)):
                audio.append(int(0)) #1유닛 추가 (총 3유닛)
        elif m == '$': #단어 사이일 경우
            for i in range(int(t*fs*3)):
                audio.append(int(0)) #5유닛 추가 (총 7유닛)
        for i in range(int(t*fs*1)): #dits와 dash사이 1unit
            audio.append(int(0))

    return audio


def audio2file(audio, filename):
    with wave.open(filename, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(4)
        w.setframerate(48000)
        for a in audio:
            w.writeframes(struct.pack('<l', a))



def file2morse(filename):
    with wave.open(filename, 'rb') as w:
        audio = []
        framerate = w.getframerate()
        frames = w.getnframes()
        for i in range(frames):
            frame = w.readframes(1)
            audio.append(struct.unpack('<i', frame)[0])
        morse = ''
        unit = int(0.1 * 48000)
        for i in range(1, math.ceil(len(audio)/unit)+1):
            stdev = statistics.stdev(audio[(i-1)*unit:i*unit])
            if stdev > 10000:
                morse = morse + '.'
            else:
                morse = morse + ' '
        morse = morse.replace('...', '-')
    return morse

def morse2text(morse): #7유닛을 띄어쓰기로 3유닛을 글자 사이로 구분 필요
    morse = morse.rstrip()
    text = ""
    replaced_morse = morse.replace("       ","/ /")
    replaced_morse = replaced_morse.replace("   ","/")
    replaced_morse = replaced_morse.split("/")
    for i in replaced_morse :
        if i in morsecode:
            text += morsecode[i]
        elif i == ' ':
            # 단어 사이의 공백을 유지하기 위함
            text += ' '
    return text


password = "9702 202002493 3963 FREEDOM 1787 COMPUTER DIFFICULT 4391"
audio2file(morse2audio(text2morse(password)),"202002493-박민서.wav")



#print(text2morse("hello"))
#print(file2morse("test.wav"))
#print(morse2text(file2morse("202002493.wav")))


'''
INTMAX = 2**(32-1)-1
t = 1.0
fs = 48000
f = 523.251 # C4
audio = []
for i in range(int(t*fs)):
    audio.append(int(INTMAX*math.sin(2*math.pi*f*(i/fs))))

filename = 't.wav'
with wave.open(filename, 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(4)
    w.setframerate(48000)
    for a in audio:
        w.writeframes(struct.pack('<l', a))
'''
