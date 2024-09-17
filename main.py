import tkinter as tk
from PIL import Image, ImageTk
import edge_tts
import threading
import wave
import pyaudio

def submit_text():
    text = text_entry.get()
    if text:
        submit_button["state"] = tk.DISABLED
        wait_label.config(text="Processing...")
        thread = threading.Thread(target=synthesize_speech, args=(text,))
        thread.start()

def synthesize_speech(text):
    try:
        output_file = "output.wav"
        tts = edge_tts.TTS(voice="en-US", rate=120)
        tts.speak(text, output_file)
        submit_button["state"] = tk.NORMAL
        wait_label.config(text="Speech synthesized!")
        voice_button["state"] = tk.NORMAL
        save_button["state"] = tk.NORMAL
    except Exception as e:
        print(f"Error: {e}")
        submit_button["state"] = tk.NORMAL
        wait_label.config(text="Error occurred. Please try again.")

def play_audio():
    try:
        with wave.open("output.wav", "rb") as wf:
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            data = wf.readframes(1024)
            while data:
                stream.write(data)
                data = wf.readframes(1024)
            stream.stop_stream()
            stream.close()
            p.terminate()
    except Exception as e:
        print(f"Error: {e}")

def save_audio():
    # Implement saving logic (e.g., using filedialog)
    pass

# Create the GUI window
root = tk.Tk()
root.title("Text-to-Speech")
root.geometry("400x300")

# Load the logo image
logo_image = Image.open("download.jpeg")
logo_image_tk = ImageTk.PhotoImage(logo_image)

# Create GUI elements
logo_label = tk.Label(root, image=logo_image_tk)
logo_label.pack()

text_label = tk.Label(root, text="Enter text:")
text_label.pack()

text_entry = tk.Entry(root)
text_entry.pack()

submit_button = tk.Button(root, text="Submit", command=submit_text)
submit_button.pack()

wait_label = tk.Label(root, text="")
wait_label.pack()

voice_button = tk.Button(root, text="Listen", command=play_audio, state=tk.DISABLED)
voice_button.pack()

save_button = tk.Button(root, text="Save", command=save_audio, state=tk.DISABLED)
save_button.pack()

root.mainloop()
