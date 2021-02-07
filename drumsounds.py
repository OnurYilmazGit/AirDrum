import simpleaudio as sa
import time


#drum audio

snare1 = sa.WaveObject.from_wave_file("drum_audio/Snare2.wav")
snare2 = sa.WaveObject.from_wave_file("drum_audio/Snare2.wav")
snare3 = sa.WaveObject.from_wave_file("drum_audio/Snare3.wav")
snare4 = sa.WaveObject.from_wave_file("drum_audio/Snare4.wav")
snare5 = sa.WaveObject.from_wave_file("drum_audio/Snare5.wav")
Hat1 = sa.WaveObject.from_wave_file("drum_audio/Hat2.wav")
Hat2 = sa.WaveObject.from_wave_file("drum_audio/Hat2.wav")
Hat3 = sa.WaveObject.from_wave_file("drum_audio/Hat3.wav")
Hat4 = sa.WaveObject.from_wave_file("drum_audio/Hat4.wav")
Hat5 = sa.WaveObject.from_wave_file("drum_audio/Hat5.wav")
Kick1 = sa.WaveObject.from_wave_file("drum_audio/Kick2.wav")
Kick2 = sa.WaveObject.from_wave_file("drum_audio/Kick2.wav")
Kick3 = sa.WaveObject.from_wave_file("drum_audio/Kick3.wav")
Kick4 = sa.WaveObject.from_wave_file("drum_audio/Kick4.wav")
Kick5 = sa.WaveObject.from_wave_file("drum_audio/Kick5.wav")
Kick6 = sa.WaveObject.from_wave_file("drum_audio/Kick6.wav")
Crash = sa.WaveObject.from_wave_file("drum_audio/crash.wav")
Tom1 = sa.WaveObject.from_wave_file("drum_audio/Tom1.wav")

#random audio
#elephant = sa.WaveObject.from_wave_file("random_audio/elephant.wav")

#clave = sa.WaveObject.from_wave_file("random_audio/clave.wav")
#cowbell = sa.WaveObject.from_wave_file("random_audio/cowbell.wav")
#dasani = sa.WaveObject.from_wave_file("random_audio/dasani.wav")
#moomba = sa.WaveObject.from_wave_file("random_audio/moomba.wav")

list_snare = [snare3,snare3,snare4,snare4,snare5]
list_hat = [Hat1,Hat2,Hat3,Hat4,Hat5]
list_kick = [Kick1,Kick2,Kick3,Kick4,Kick5,Kick6]
list_crash = [Crash]
list_ride = [Hat5]
list_tom = [Tom1]

def play_hi_hat(num):
    play_obj = list_hat[num].play()
    
def play_snare(num):
    play_obj = list_snare[num].play()
    
def play_kick(num):
    play_obj = list_kick[num].play()

def play_crash(num):
    play_obj = list_crash[0].play()

def play_nothing():
    play_obj = list_kick[5].play()

def play_ride(num):
    play_obj = list_ride[0].play()
  
def play_tom(num):
    play_obj = list_tom[0].play()

'''      
def play_mid_tom():
    play_obj = midtom.play()
    
def play_elephant():
    play_obj = elephant.play()
    
def play_clave():
    play_obj = clave.play()
    
def play_cowbell():
    play_obj = cowbell.play()

def play_dasani():
    play_obj = dasani.play()
    
def play_moomba():
    play_obj = moomba.play()

'''
