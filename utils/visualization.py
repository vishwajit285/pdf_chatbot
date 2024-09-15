# utils/visualization.py
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from utils.chroma_manager import get_chroma_client

def generate_word_cloud():
    client = get_chroma_client()
    collection = client.get_or_create_collection('pdf_embeddings')
    documents = collection.get()['documents']
    full_text = " ".join(documents)
    wordcloud = WordCloud(width=800, height=400).generate(full_text)
    fig, ax = plt.subplots(figsize=(15, 7.5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)
    return fig
