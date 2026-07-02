import streamlit as st
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences

# -------------------------------
# Load Model
# -------------------------------
model = load_model("imdb_rnn_model.keras")

VOCAB_SIZE = 10000
MAX_LENGTH = 200

word_index = imdb.get_word_index()

# Reverse dictionary
word_to_id = {k: (v + 3) for k, v in word_index.items()}
word_to_id["<PAD>"] = 0
word_to_id["<START>"] = 1
word_to_id["<UNK>"] = 2
word_to_id["<UNUSED>"] = 3


# -------------------------------
# Encode Text
# -------------------------------
def encode_review(text):

    words = text.lower().split()

    encoded = [1]

    for word in words:
        encoded.append(word_to_id.get(word, 2))

    encoded = pad_sequences(
        [encoded],
        maxlen=MAX_LENGTH,
        padding="post",
        truncating="post"
    )

    return encoded


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(
    page_title="IMDb Sentiment Analysis",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 IMDb Movie Review Sentiment Analysis")

st.write(
    "Enter a movie review and the trained **Recurrent Neural Network (RNN)** "
    "will predict whether it is **Positive** or **Negative**."
)

review = st.text_area(
    "Movie Review",
    height=200,
    placeholder="Example: This movie was absolutely fantastic..."
)

if st.button("Predict Sentiment"):

    if review.strip() == "":
        st.warning("Please enter a movie review.")
    else:

        review_encoded = encode_review(review)

        prediction = model.predict(review_encoded)[0][0]

        if prediction >= 0.5:

            st.success("😊 Positive Review")

            st.metric(
                "Confidence",
                f"{prediction*100:.2f}%"
            )

        else:

            st.error("😞 Negative Review")

            st.metric(
                "Confidence",
                f"{(1-prediction)*100:.2f}%"
            )

st.divider()

st.markdown(
"""
### Example Reviews

**Positive**
> This movie was amazing with excellent acting and a wonderful storyline.

**Negative**
> I hated this movie. It was boring, slow, and a complete waste of time.
"""
)