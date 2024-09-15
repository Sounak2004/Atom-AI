from datetime import datetime
import pyttsx3 as p  # type: ignore
import speech_recognition as sr  # type: ignore
import geocoder #type:ignore

# Initialize pyttsx3 engine
engine = p.init()

# Set speech rate and voice
rate = engine.getProperty('rate')
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to make the engine speak
def speak(text):
    print(f"Assistant says: {text}")  # Debugging output
    engine.say(text)
    engine.runAndWait()

# Function to get the current time
def get_current_time():
    now = datetime.now()
    return now.strftime("%H:%M")

# Function to get the current date
def get_current_date():
    today = datetime.now()
    return today.strftime("%d:%m:%Y")

def get_location():
     g = geocoder.ip('me')  # 'me' gets the IP-based location of the device
     return {
                'city': g.city,
                'state': g.state,
                'country': g.country,
                'latlng': g.latlng  # Latitude and longitude
            }


# Initialize speech recognizer
r = sr.Recognizer()

# Wake-up function to listen for the wake word
def wake_up():
    wake_word = "hello atom"  # Define your wake word
    

    while True:
        
         with sr.Microphone() as source:
            
            r.adjust_for_ambient_noise(source)
            print("Listening for wake word...")

            try:
                audio = r.listen(source)
                text = r.recognize_google(audio).lower()  # Recognize the speech and convert to lowercase
                print(f"You said: {text}")

                if wake_word in text:  # If the wake word is detected
                    speak("Hello, I am ATOM AI. How can I assist you?")
                    assistant_active()  # type: ignore # Activate the assistant to take commands
                    break  # Break the loop and go to active listening mode
              
         
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
#Function to stop excecute the chatbot
def stop():
    stop_word="bye"
    print("OK GOOD BYE!!")
    exit()


# Function to respond based on recognized commands
def assistant_active():
    global stop_word
    stop_word="take care"
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        print("Listening for commands...")

        try:
            audio = r.listen(source)
            text = r.recognize_google(audio).lower()
            print(f"You said: {text}")

            # Respond based on recognized speech
            if "hi" in text or "hello" in text:
                speak("Hello! How can I assist you?")
            elif "how are you" in text:
                speak("I am good, thank you for asking!")
            elif "what is the time" in text:
                current_time = get_current_time()
                speak(f"The current time is {current_time}.")
            elif "what is the date" in text:
                current_date = get_current_date()
                speak(f"Today's date is {current_date}.")
                print(current_date)
            elif"what is my current location" in text:
                current_location=get_location()
                speak(f"Your current location is {current_location}.")
                print(current_location)
            elif stop_word  in text:
                stop()

            else:
                speak("Sorry, I didn't catch that. Could you please repeat?")
                
        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said.")
        except sr.RequestError as e:
            speak(f"Could not request results from the Google Speech Recognition service; {e}")
        except Exception as e:
            speak(f"An unexpected error occurred: {e}")

    # After completing the command, return to passive listening mode
    wake_up()

# Start the assistant by listening for the wake word
if __name__ == "__main__":
    wake_up()
