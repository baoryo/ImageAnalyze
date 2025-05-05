import streamlit as st
import openai
import base64
from PIL import Image
import io

# Set your OpenAI API key
import os
openai.api_key = os.getenv("YOUR_OPENAI_API_KEY")

st.title("Interior Design Suggestions AI")
st.write("Upload an image of your room, and get AI suggestions to improve it!")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

    if st.button("Get Design Suggestions"):
        with st.spinner("Analyzing..."):
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "This is my room. What can I do to improve its interior design?"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                        ]
                    }
                ],
                max_tokens=800,
            )
            st.success("Done!")
            st.write(response.choices[0].message.content)
