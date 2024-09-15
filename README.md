
# PDF Chatbot with Voice Input/Output and ChromaDB Integration

This project is a PDF chatbot that allows users to interact with PDFs through both text and voice inputs. It processes PDFs by generating text embeddings using OpenAI, storing them in ChromaDB for querying, and can respond to questions via voice output. The application also handles duplicate documents and PDFs with the same name by using content-based hashing to ensure uniqueness.

## Key Features

- **Voice Input and Output**: Users can ask questions via voice input, and the chatbot responds in voice, making it more interactive and accessible.
- **PDF Upload and Storage**: Upload PDFs and process them with a unique identifier using MD5 hashing to prevent duplicate content.
- **Text Embeddings with OpenAI**: Extract text from PDFs and generate embeddings for efficient querying and downstream tasks like recommendations and summarization.
- **ChromaDB Integration**: Store embeddings and metadata in ChromaDB for quick and efficient retrieval.
- **Duplicate Document Handling**: Automatically detects and manages duplicate documents by comparing file content using hashing.
- **Document Name Handling**: Handles PDFs with the same name by appending content-based hashes to filenames for uniqueness.
- **Summarization and Recommendations**: Summarizes PDF content and recommends similar documents based on embeddings.

## Folder Structure

```bash
your_project/
├── app.py                     # Main entry point for the Streamlit app
├── data/                      # Stores data used in the project
│   ├── annotations.json        # Metadata annotations for PDFs
│   ├── pdfs/                   # Directory for uploaded PDFs
│   └── chroma/                 # Directory for ChromaDB's persistent data
├── utils/                     # Utility modules for different functionalities
│   ├── __init__.py
│   ├── pdf_handler.py          # Handles PDF processing and embedding
│   ├── chroma_manager.py       # Manages ChromaDB client and embedding storage
│   ├── retrieval.py            # Provides retrieval functionalities for querying PDFs
│   ├── summarization.py        # Summarizes the extracted PDF text
│   ├── annotations.py          # Utilities for handling PDF metadata and annotations
│   ├── recommendations.py      # Recommends documents based on embeddings
│   ├── external_data.py        # Handles fetching and processing of external data
│   └── security.py             # Implements security measures for PDF handling
├── requirements.txt            # Python dependencies required by the project
└── README.md                   # Project documentation
```

## Key Functionalities

1. **Voice Input and Output**:
   - The chatbot accepts voice input for questions and processes the response via voice output using text-to-speech libraries.
   - This feature allows for a more accessible, hands-free interaction.

2. **Duplicate Document Handling**:
   - The system calculates a content-based hash for each uploaded PDF.
   - If a document with the same content already exists in the database, the system will skip the embedding and notify the user that the document has already been processed.
   
3. **Document Name Handling**:
   - For documents with the same name but different content, the filename is automatically appended with a hash of the content to ensure uniqueness.

4. **Text Chunking and Embedding**:
   - Extracts text from uploaded PDFs and chunks it for embedding.
   - Embeddings are stored in ChromaDB for querying and further analysis.

5. **Summarization**:
   - The application summarizes long PDFs, allowing users to quickly grasp the main points.

6. **Recommendations**:
   - Based on text embeddings, the system can recommend similar documents.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/vishwajit285/pdf_chatbot.git
cd pdf_chatbot
```

### 2. Create and Activate a Virtual Environment

To ensure that all dependencies are installed in an isolated environment, create and activate a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

- On macOS and Linux:

    ```bash
    source venv/bin/activate
    ```

- On Windows:

    ```bash
    venv\Scripts\activate
    ```

### 3. Install Dependencies

Install all the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Export Your OpenAI API Key

This project uses OpenAI's API to generate text embeddings. You need to export your OpenAI API key before running the application.

#### Temporarily Set the API Key (for current session):

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

#### Persistently Set the API Key (for future sessions):

For **Bash** (Linux/macOS):

```bash
echo 'export OPENAI_API_KEY="your-openai-api-key"' >> ~/.bashrc
source ~/.bashrc
```

For **Zsh** (macOS with Zsh):

```bash
echo 'export OPENAI_API_KEY="your-openai-api-key"' >> ~/.zshrc
source ~/.zshrc
```

For **Windows** (PowerShell):

```powershell
$env:OPENAI_API_KEY="your-openai-api-key"
```

### 5. Set Up the ChromaDB Directory

Ensure that the directory for ChromaDB's persistent data exists:

```bash
mkdir -p data/chroma
```

### 6. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

### 7. Upload PDFs and Interact

- Upload a PDF through the Streamlit interface.
- The PDF will be processed, and text embeddings will be generated and stored in ChromaDB.
- You can interact with the system through both text and voice inputs. Ask questions about the content of the uploaded PDF, and the system will respond in voice format.


`

## Contributing

Feel free to contribute by opening issues or submitting pull requests. Please ensure that your code adheres to the project's coding guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
