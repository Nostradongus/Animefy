import streamlit as st
from PIL import Image

# style.py
import style 

# page title
st.title('AnimeGANv2: Implementation Test')

# TODO: implement feature for user to upload own image to be stylized
# TEMPORARY: images to choose from
image = st.sidebar.selectbox(
    'Select image',
    ('bosco.jpg', 'br.jpg', 'bridge.jpg', 'cat.jpg', 'cdbs.jpg', 
     'chapel.jpg', 'city.jpg', 'dlsu.jpg', 'dog.jpg', 'japan.jpg', 
     'sakura.jpg', 'walking.jpg')
)

# anime styles to choose from based from AnimeGANv2
anime_style = st.sidebar.selectbox(
    'Select Anime Style',
    ('Paprika', 'Shinkai', 'Hayao')
)

# TEMPORARY: image chosen by user
input_image = "images/" + image

st.write("### Input Image:")
st.image(Image.open(input_image), width=1000)

# stylize image button
stylize_btn = st.button('Stylize!')
if stylize_btn:
    # stylize input image and produce output
    output_image = style.stylize(anime_style, input_image)
    
    # display output
    st.write('### Output Image:')
    # clamp and channels are used since OpenCV was used in processing the image
    st.image(output_image, clamp=True, channels='RGB', width=1000) 
