import streamlit as st
from PIL import Image
import cv2 as cv
import numpy as np
from random import randint
import threading

# style.py
import style

st.set_page_config(page_title="Animefy", page_icon="images/animefy_logo.png")

model_lock = threading.Lock()

# remove "Made with Streamlit" footer text
# uncomment "#MainMenu {visibility: hidden;}" to also remove the default Streamlit hamburger menu
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
</style>
"""
st.markdown(hide_streamlit, unsafe_allow_html=True)

# randomizer. a workaround for clearing the contents of the file_uploader
if 'uploader_key' not in st.session_state:
    st.session_state['uploader_key'] = str(randint(1000, 100000000))

# home page title and caption
st.markdown("""
    # 📸 Animefy

    Convert your photos into **anime** with _ease_ using **AnimeGAN**.
""")

st.markdown('---')

# main container of the page
page_container = st.empty()

# store home page contents inside page_container
home_page = page_container.container()

# step #1
home_page.markdown("""
    ### Step #1: Upload the photo that you would like to process!
""")

# just some notes for the user
with home_page.expander("📣 Here are some things to take note of...", expanded=True):
    st.write("""    
        * Do note that AnimeGAN works best with images containing **sceneries without people**. 
        * For best results, use images that **do not** contain human subjects.
        * Due to server hardware limitations, only upload images with **at most** a resolution of **1980x1080**.
        * Fore more information on AnimeGAN, click [here](https://github.com/TonyLianLong/AnimeGAN.js).
    """)

# upload image functionality
uploaded_image = home_page.file_uploader(
        "If you're ready, you can now upload your image here:", type=['png','jpg','jpeg'], key=st.session_state['uploader_key']
    )

# if there is an uploaded image, show next steps
if uploaded_image is not None:
    # just a preview of the uploaded image
    home_page.markdown("""
        #### Uploaded Image

        Here's your photo! Just upload another one if you would like to change it 😉
    """)
    home_page.image(Image.open(uploaded_image))

    home_page.write("---")

    # step #2
    home_page.markdown("""
        ### Step #2: Now, select your preferred animation style!
    """)

    # drop down list for anime style to be applied to image
    anime_style = home_page.selectbox (
            'Your preferred animation style:',
            ('Paprika', 'Shinkai', 'Hayao')
        )

    # just some more notes for the user
    with home_page.expander("🤔 What are these animation styles?", expanded=False):
        st.write("""
            These styles were derived from the works of various directors! Some of these might be familiar to you:   
            * Satoshi Kon: **Paprika**
            * Makoto **Shinkai**: Your Name, 5 Centimeters per Second, Weathering with You
            * **Hayao** Miyazaki: Spirited Away, My Neighbor Totoro, Princess Mononoke
        """)

    home_page.write("---")
    
    # stylize image
    home_page.markdown("If you're all set, then let's proceed! 😄")
    stylize_btn = home_page.button("Stylize!")

    # if "stylize" button is clicked,
    if stylize_btn:
        # remove processing page contents
        page_container.empty()

        with st.spinner('Hold on... Please do not close this tab....'):
            model_lock.acquire()

        # spinner (while processing image)
        with st.spinner('Hold on... Processing your image...'):
            # stylize input image and produce output
            output_image = style.stylize(anime_style, uploaded_image)
            model_lock.release()

        # step #3
        st.markdown("""
            ### Step #3: Download your image!
        """)

        # display original and output images
        st.markdown("""
            Here's a before and after!
        """)
        before_col, after_col = st.columns(2)
        with before_col:
            # clamp and channels are used since OpenCV was used in processing the image
            st.image(uploaded_image, clamp=True, channels='RGB')
        with after_col:
            # clamp and channels are used since OpenCV was used in processing the image
            st.image(output_image, clamp=True, channels='RGB')

        st.write("---")

        # prepare output image for downloading
        img_encode = cv.imencode('.jpg', output_image)[1]
        data_encode = np.array(img_encode)
        byte_encode = data_encode.tobytes()

        # some instruction for downloading
        st.write("Finally, just click this to download your _anime-fied_ image!")
        # download button
        st.download_button('Download Image', byte_encode, 'output.jpg', 'jpg')

        st.write("---")

        # retry message
        st.markdown('Not satisfied? Click this to retry!')
        # retry button
        retry_btn = st.button("Retry!")
        
        # randomizer. just another workaround.
        st.session_state['uploader_key'] = str(randint(1000, 100000000))

        if retry_btn:
            page_container.empty()