from scrap import *
import streamlit as st
from groq import Groq
from audio_recorder_streamlit import audio_recorder
from elevenlabs.client import ElevenLabs
from langchain.chains import RetrievalQA
from streamlit_chat import message

model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-001", api_key=GEMINI_API_KEY)
# Constants
TEMP_AUDIO_PATH = "temp_audio_1.mp3"
AUDIO_FORMAT = "audio/mp3"

# Load environment variables from .env file and return the keys
ELEVEN_API_KEY = os.getenv('ELEVEN_API_KEY')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def load_embeddings_and_database(active_loop_data_set_path):
    db = DeepLake(
        dataset_path=active_loop_data_set_path,
        read_only=True,
        embedding_function=embeddings
    )
    return db

# Transcribe audio using OpenAI Whisper API
def transcribe_audio(audio_file_path, GROQ_API_KEY):
    try:
      # Initialize the Groq client
        client = Groq()

# Specify the path to the audio file
        filename = audio_file_path # Replace with your audio file!
        
        # Open the audio file
        with open(filename, "rb") as file:
            # Create a transcription of the audio file
            transcription = client.audio.transcriptions.create(
            file=(filename, file.read()), # Required audio file
            model="distil-whisper-large-v3-en", # Required model to use for transcription
            response_format="json",  # Optional
            temperature=0.0  # Optional
            )
            # Print the transcription text
            return transcription.text
    except Exception as e:
        print(f"Error calling Whisper API: {str(e)}")
        return None

# Record audio using audio_recorder and transcribe using transcribe_audio
def record_and_transcribe_audio():
    audio_bytes = audio_recorder()
    transcription = None
    if audio_bytes:
        st.audio(audio_bytes, format=AUDIO_FORMAT)

        with open(TEMP_AUDIO_PATH, "wb+") as f:
            f.write(audio_bytes) 

        if st.button("Transcribe"):
            transcription = transcribe_audio(TEMP_AUDIO_PATH, GROQ_API_KEY)
            os.remove(TEMP_AUDIO_PATH)
            display_transcription(transcription)

    return transcription

# Display the transcription of the audio on the app
def display_transcription(transcription):
    if transcription:
        st.write(f"Transcription: {transcription}")
        # with open("audio_transcription.txt", "w+") as f:
        #     f.write(transcription)
    else:
        st.write("Error transcribing audio.")

# Get user input from Streamlit text input field
def get_user_input(transcription):
    return st.text_input("", value=transcription if transcription else "", key="input")

# Search the database for a response based on the user's query
def search_db(user_input, db):
    print(user_input)
    retriever = db.as_retriever()
    retriever.search_kwargs['distance_metric'] = 'cos'
    retriever.search_kwargs['fetch_k'] = 100
    retriever.search_kwargs['k'] = 4
    qa = RetrievalQA.from_llm(model, retriever=retriever, return_source_documents=True)
    return qa({'query': user_input})

# Display conversation history using Streamlit messages
def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i],key=str(i))
        #Voice using Eleven API
        text= history["generated"][i]

        client = ElevenLabs(
            api_key=ELEVEN_API_KEY,  # Defaults to ELEVEN_API_KEY
        )

        voice = client.voices.get_all()

        audio = client.generate(text=text, voice=voice.voices[0])
        # st.audio(audio, format='audio/mp3')
        audio_bytes = b"".join(audio)

        # Save bytes to a file and display
        with open("temp_audio.mp3", "wb") as f:
            f.write(audio_bytes)

        st.audio("temp_audio.mp3", format='audio/mp3')
        os.remove("temp_audio.mp3")

# Main function to run the app
def main():
    # Initialize Streamlit app with a title
    st.write("# Voice Assistant 🧙")

    # Load embeddings and the DeepLake database
    db = load_embeddings_and_database(dataset_path)

    # Record and transcribe audio
    transcription = record_and_transcribe_audio()

    # Get user input from text input or audio transcription
    user_input = get_user_input(transcription)

    # Initialize session state for generated responses and past messages
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["I am ready to help you"]
    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey there!"]

    # Search the database for a response based on user input and update the session state
    if user_input:
        output = search_db(user_input, db)
        print(output['source_documents'])
        st.session_state.past.append(user_input)
        response = str(output["result"])
        st.session_state.generated.append(response)

    # Display conversation history using Streamlit messages
    if st.session_state["generated"]:
        display_conversation(st.session_state)


# Run the main function when the script is executed
if __name__ == "__main__":
    main()
