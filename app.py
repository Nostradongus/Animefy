import streamlit as st
from PIL import Image

import cv2 as cv
import numpy as np

# style.py
import style 

st.set_page_config(page_title="Animefy", page_icon=":art:")

# remove "Made with Streamlit" footer text
# uncomment "#MainMenu {visibility: hidden;}" to also remove the default Streamlit hamburger menu
hide_streamlit = """
<style>
// #MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit, unsafe_allow_html=True) 

# page title and caption
st.header('Animefy')
st.subheader('Real-life sceneries anime-fied in a click.')

# image uploader
uploaded_image = st.file_uploader(
        "First, upload your image here:", type=['png','jpg']
    )

# if there is an uploaded image, reveal other elements
if uploaded_image is not None:
    
    # display input image
    st.subheader("Input Image")
    st.image(Image.open(uploaded_image))

    # drop down list for anime style to be applied to image
    anime_style= st.selectbox (
            'Then, select your preferred animation style!',
            ('Paprika', 'Shinkai', 'Hayao')
        )

    # "stylize" image button
    st.write("Aaaaaaand if you're all set, just click this!")
    stylize_btn = st.button('Stylize!')
    
    # if "stylize" button is clicked,
    if stylize_btn:

        with st.spinner('Image is being processed...'):
            # stylize input image and produce output
            output_image = style.stylize(anime_style, uploaded_image)
        
        # display output
        st.subheader('Output Image')
        # clamp and channels are used since OpenCV was used in processing the image
        st.image(output_image, clamp=True, channels='RGB')
        

        img_encode = cv.imencode('.jpg', output_image)[1]
        data_encode = np.array(img_encode)
        byte_encode = data_encode.tobytes()

        st.write("Finally, just click this to download your anime-fied image!")
        st.download_button('Download Image', byte_encode, 'output.jpg', 'jpg')