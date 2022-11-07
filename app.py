"""
# Labelisation App for La Douane

"""

import streamlit as st
import pandas as pd
from PIL import Image
import os
import time

images = os.listdir("./images/")

st.title("VitiViz Labelisation App")

st.markdown("Objectif: ...")

#df = pd.DataFrame(columns=['Image','Label','Timestamp'])
#df.to_csv("./labelisation_responses.csv",index=False)
df = pd.read_csv("./labelisation_responses.csv")

index = st.number_input("Image", min_value=0, max_value=2, step=1)

(
    col1,
    col2,
) = st.columns([4, 1])

with col1:
    # Read images in folder
    image = Image.open("./images/" + images[index])
    st.image(image, use_column_width=True)

with col2:
    form = st.form(key="match")
    with form:
        boolean = st.selectbox("Choose label", ("Good", "Bad"))
        timestamp = time.time()
        submit = st.form_submit_button("Submit")
        if submit:
            response = {"Image": index, "Label": boolean, "Timestamp": timestamp}
            df = df.append(response, ignore_index=True)
            df.to_csv("./labelisation_responses.csv", index=False)
            st.success("Done", icon="✅")

st.markdown("### Labelisation response summary")

# Present results
# Take last responses based on submission timestamp
idx = df.groupby(["Image"])["Timestamp"].transform(max) == df["Timestamp"]
df = df[idx]
# Sort images by Image index
df = df[["Image", "Label"]].sort_values(by=["Image"], ascending=True)
st.dataframe(df, use_container_width=True)
