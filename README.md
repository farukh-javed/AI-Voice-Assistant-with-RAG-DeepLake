# AI Voice Assistant 🤖🎤

## Overview
The **AI Voice Assistant** project allows users to interact using **voice** or **text** input, and provides responses in both voice and text formats. It uses a user-provided **knowledge base** for answering questions through a conversational interface.

## Key Features ✨
- **Voice & Text Input**: Supports input through speech and text.
- **Voice & Text Output**: Delivers responses in both formats.
- **Custom Knowledge Base**: Uses information from user-uploaded sources for Q&A.

## How It Works 🛠️
1. **Input**: Users provide input either by speaking or typing.
2. **Processing**: The assistant processes the query and searches the knowledge base.
3. **Response**: The output is given in both text and voice.

## Included Files 📂

### 1. `scrap.py`
- **Function**: Scrapes content from the provided URLs and stores it in a **DeepLake** vector database.
- **Modules Used**: 
  - `GoogleGenerativeAIEmbeddings` for generating embeddings.
  - `DeepLake` for database management.
  - `BeautifulSoup` for web scraping.
- **Main Flow**:
  - Scrapes documentation pages.
  - Processes and stores the data for retrieval.

### 2. `chat.py`
- **Function**: Implements the voice assistant interface using **Streamlit**.
- **Modules Used**: 
  - `Groq API` for transcribing audio.
  - `ElevenLabs API` for voice output.
  - `GoogleGenerativeAI` for generating responses.
  - `DeepLake` for querying the knowledge base.
- **Main Flow**:
  - Handles user input through text or voice.
  - Searches the knowledge base and returns responses.

## Tech Stack 🧑‍💻
- **LangChain**: For text embeddings and document management.
- **GoogleGenerativeAIEmbeddings**: To generate embeddings from the scraped content.
- **DeepLake**: Vector storage for the knowledge base.
- **Streamlit**: Frontend for the assistant.
- **Groq API**: For audio transcription.
- **ElevenLabs API**: To convert text responses to speech.

## Setup and Installation ⚙️
1. Clone the repository:
   ```bash
   git clone https://github.com/farukh-javed/AI-Voice-Assistant with DeepLake.git
   cd AI-Voice-Assistant
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` file with the required API keys:
   ```
   ELEVEN_API_KEY=your_elevenlabs_api_key
   GROQ_API_KEY=your_groq_api_key
   GEMINI_API_KEY=your_google_api_key
   ```

## How to Run ▶️
1. Run `scrap.py` to scrape and store the knowledge base:
   ```bash
   python scrap.py
   ```
2. Start the Streamlit app for the voice assistant:
   ```bash
   streamlit run chat.py
   ```
