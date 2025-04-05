import os
import queue
import sounddevice as sd
import vosk
import json
import time
from datetime import datetime
import subprocess

model = vosk.Model("vosk-model")
q = queue.Queue()

commands = [
    "youtube", "help", "hello", "exit", "hanuman", "call daughter", "news",
    "camera", "screenshot", "files", "photos", "alarm", "time", "battery",
    "brightness", "volume", "gita", "fall", "religious", "wellness", "information",
    "shopping", "weather"
]

grammar = json.dumps(commands)

# Kill previous foreground app gracefully
def kill_foreground_app():
    try:
        pkg = subprocess.check_output(
            "adb shell dumpsys window windows | grep -E 'mCurrentFocus'",
            shell=True, text=True
        ).strip().split("/")[0].split()[-1]
        if pkg:
            print(f"Killing package: {pkg}")
            os.system(f"adb shell am force-stop {pkg}")
    except Exception as e:
        print(f"[!] Error while killing previous app: {e}")

# Callback for Vosk input
def callback(indata, frames, time, status):
    q.put(bytes(indata))

# Start listening loop
with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                       channels=1, callback=callback):
    print("🎤 Listening... elder-friendly mode ON 🧓")
    rec = vosk.KaldiRecognizer(model, 16000, grammar)

    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "").strip()
            print("You said:", text)

            kill_foreground_app()  # Clean stack before launching new task

            if text == "youtube":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://www.youtube.com")

            elif text == "gita":
                os.system('adb shell am start -a android.intent.action.VIEW -d "https://www.youtube.com/watch?v=gah3M_XW1XE&list=PL4yzYPLUTztgZjbt6WoPYukQap9i44dwU"')

            elif text == "help":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://sahayak-omega.vercel.app/")

            elif text == "religious":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://sahayak-omega.vercel.app/chat/religious")

            elif text == "wellness":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://sahayak-omega.vercel.app/chat/wellness")

            elif text == "information":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://sahayak-omega.vercel.app/chat/information")

            elif text == "shopping":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://sahayak-omega.vercel.app/chat/shopping")

            elif text == "hanuman":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://www.youtube.com/watch?v=Jzb_Nv_ecJ0")

            elif text == "call daughter":
                os.system("adb shell am start -a android.intent.action.DIAL")

            elif text == "news":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://news.google.com/topstories")

            elif text == "weather":
                os.system("adb shell am start -a android.intent.action.VIEW -d https://www.accuweather.com/")

            elif text == "camera":
                os.system("adb shell am start -a android.media.action.IMAGE_CAPTURE")

            elif text == "screenshot":
                os.system("adb shell screencap -p /sdcard/Download/screenshot.png")

            elif text == "files":
                os.system("adb shell monkey -p com.google.android.apps.nbu.files -c android.intent.category.LAUNCHER 1")

            elif text == "photos":
                os.system("adb shell monkey -p com.google.android.apps.photos -c android.intent.category.LAUNCHER 1")

            elif text == "alarm":
                os.system("adb shell monkey -p com.google.android.deskclock -c android.intent.category.LAUNCHER 1")

            elif text == "time":
                current_time = datetime.now().strftime("%I:%M %p")
                print(f"The current time is {current_time}")

            elif text == "battery":
                try:
                    output = subprocess.check_output("adb shell dumpsys battery", shell=True, text=True)
                    for line in output.splitlines():
                        if "level" in line.lower():
                            level = line.strip().split(":")[-1].strip()
                            print(f"Battery is at {level} percent")
                except Exception as e:
                    print(f"Could not check battery: {e}")

            elif text == "brightness":
                os.system("adb shell settings put system screen_brightness 255")

            elif text == "volume":
                os.system("adb shell media volume --stream 3 --set 15")

            elif text == "fall":
                print("Fall detected! Triggering siren and emergency dial...")
                os.system("adb shell am start -a android.intent.action.VIEW -d https://www.youtube.com/watch?v=UMQbfvvXqNw")
                time.sleep(3)
                os.system("adb shell am start -a android.intent.action.DIAL -d tel:112")

            elif text == "hello":
                print("Hello, I’m listening!")

            elif text == "exit":
                print("Goodbye!")
                break

