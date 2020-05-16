from gtts import gTTS 
import os 
if not os.path.exists('auds'):
    os.makedirs('auds')
n = 64 
language = 'en'
for i in range(n):
    myobj = gTTS(text=str(i))
    myobj.save('auds/'+str(i)+".mp3")
