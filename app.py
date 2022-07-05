import streamlit as st
from PIL import Image
import cv2 as cv
import numpy as np
from random import randint
import threading

# style.py
import style

# utils.py
from utils import *

# tab customization
st.set_page_config(page_title="Animefy", page_icon="images/animefy_logo.png")


# SOME HELPER FUNCTIONS
# image resolution checking
def imageResCheck (image):
    # load and preprocess input image as a NumPy array
    image = np.asarray(load_input_image(image))

    image_height, image_width = image.shape[:2]

    if (image_height <= 2160 and image_width <= 2160):
        return True
    else:
        return False

# callback when user wants to try another image
def tryNewImage ():
    # to ensure that the new id is unique
    # -> to ensure that the file uploader will reset
    while True:
        # randomizer. work around for resetting file uploader
        rand_id = str(randint(1000, 100000000))

        if rand_id is not st.session_state['uploader_key']:
            page_container.empty()
            st.session_state['uploader_key'] = rand_id
            break

# callback when user wants to try another style
def tryNewStyle ():
    # if another_style_btn:
    page_container.empty()

# SOME INITIAL SETUP
# To hide some default streamlit components and to add some customizations
hide_streamlit = """
<style>
    #MainMenu {
        visibility: hidden;
    }
    footer {
        visibility: hidden;
    }
    header {
        visibility: hidden;
    }
    button[title='View fullscreen'] {
        visibility: hidden;
    }
    .appview-container {
        background-image: url("https://drive.google.com/uc?export=view&id=1HbgExEyTd8r6kWhe7JYgihnsXXtZ0Lmm");
        background-size: cover;
    }
</style>
"""
st.markdown(hide_streamlit, unsafe_allow_html=True)

# randomizer. a workaround for clearing the contents of the file_uploader
if 'uploader_key' not in st.session_state:
    st.session_state['uploader_key'] = str(randint(1000, 100000000))

# FRONTEND PROPER
# home page title and caption
st.markdown("""
    # ✨ Animefy ✨

    Convert your photos into **anime** with _ease_ using **AnimeGAN**.
""")

st.markdown('---')

# main container of the page
page_container = st.empty()

# store home page contents inside page_container
home_page = page_container.container()

# STEP #1
home_page.markdown("""
    ### Step #1: Upload the photo that you would like to process!
""")

# just some notes for the user in uploading images
with home_page.expander("📣 Here are some things to take note of...", expanded=True):
    st.write("""    
        * Do note that AnimeGAN works best with images containing **sceneries without people**. 
        * For best results, use images that **do not** contain human subjects.
        * Due to performance concerns, please upload images that would not exceed a **2160x2160** resolution.
        * Fore more information on AnimeGAN, click [here](https://github.com/TachibanaYoshino/AnimeGAN).
    """)

# upload image functionality
uploaded_image = home_page.file_uploader(
        "If you're ready, you can now upload your image here:", type=['png','jpg','jpeg'], key=st.session_state['uploader_key']
    )

# some checking if the image resolution is valid
# being done only for performance purposes.
if uploaded_image is not None:
    isValidImage = imageResCheck(uploaded_image)
else:
    isValidImage = False

# warning if uploaded image has an invalid resolution
if uploaded_image is not None and not isValidImage:
    st.caption("**Warning:** For better performance, please upload an image that will not exceed a resolution of **2160x2160**.")

# if there is an uploaded image, show next steps
if isValidImage:
    # just a preview of the uploaded image
    home_page.markdown("""
        #### Uploaded Image

        Here's your photo! Just upload another one if you would like to change it 😉
    """)
    home_page.image(Image.open(uploaded_image))

    home_page.write("---")

    # STEP #2
    home_page.markdown("""
        ### Step #2: Now, select your preferred animation style!
    """)

    # drop down list for anime style to be applied to image
    anime_style = home_page.selectbox (
            'Your preferred animation style:',
            ('Paprika', 'Shinkai', 'Hayao')
        )

    # just some more notes for the user regarding the animation styles
    with home_page.expander("🤔 What are these animation styles?", expanded=False):
        st.markdown("""
            These styles were derived from the works of various directors! Some of these might be familiar to you:   
            * Satoshi Kon: **Paprika**
            * Makoto **Shinkai**: Your Name, 5 Centimeters per Second, Weathering with You
            * **Hayao** Miyazaki: Spirited Away, My Neighbor Totoro, Princess Mononoke
        """)
        st.write("---")

        # example images
        st.markdown("""
            🔍 Here are some sample images for you:
        """)

        st.image(Image.open('images/sample.png'), caption="Image from https://github.com/TachibanaYoshino/AnimeGAN")

    home_page.write("---")
    
    # stylize image
    home_page.markdown("If you're all set, then let's proceed! 😄")
    
    stylize_btn = home_page.button("Stylize!")

    # if "stylize" button is clicked,
    if stylize_btn:
        # remove processing page contents
        page_container.empty()

        # spinner (while processing image)
        with st.spinner('Hold on... Processing your image...'):
            # stylize input image and produce output
            output_image = style.stylize(anime_style, uploaded_image)

        # step #3
        st.markdown("""
            ### Step #3: Download your image!
        """)

        # display original and output images
        st.markdown("""
            Here's a before and after!
        """)

        # prepare output image for downloading
        imageRGB = cv.cvtColor(output_image, cv.COLOR_BGR2RGB)
        img_encode = cv.imencode('.jpg', imageRGB)[1]
        data_encode = np.array(img_encode)
        byte_encode = data_encode.tobytes()

        before_col, after_col = st.columns(2)
        with before_col:
            # clamp and channels are used since OpenCV was used in processing the image
            st.image(uploaded_image, clamp=True, channels='RGB')

        with after_col:
            # clamp and channels are used since OpenCV was used in processing the image
            st.image(output_image, clamp=True, channels='RGB')

        col1, col2, col3, col4 = st.columns([1, 3, 3, 3])

        with col1:
            pass
        with col2:
            # try another image
            retry_btn = st.button("New Image", on_click=tryNewImage)

        with col3:
            # try another style button
            another_style_btn = st.button("Change Style", on_click=tryNewStyle)

        with col4:
            # download button
            st.download_button('Download Image!', byte_encode, 'output.jpg', 'jpg')

        st.write("---")