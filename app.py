import streamlit as st
import serpapi
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# -------------------------------
# LOAD ENV FILE
load_dotenv()

API_KEY = os.getenv("SERP_API_KEY")

# -------------------------------
st.set_page_config(
    layout="wide",
    page_title="Price Compare",
    page_icon="💊"
)

# -------------------------------
# API FUNCTION

def compare(name):

    params = {
        "engine": "google_shopping",
        "q": name,
        "api_key": API_KEY,
        "gl": "in"
    }

    search = serpapi.GoogleSearch(params)
    results = search.get_dict()

    if "shopping_results" not in results:
        st.error("No shopping results found")
        st.stop()

    return results["shopping_results"]


# -------------------------------
# HEADER

col1, col2 = st.columns([1,3])

with col1:
    st.image("e_pharmacy.png", width=150)

with col2:
    st.title("💊 E-Pharmacy Price Comparison System")
    st.write(
        "Compare medicine prices across online pharmacies and find the **best deal instantly**."
    )

st.divider()

# -------------------------------
# SIDEBAR

st.sidebar.header("🔍 Search Medicine")

medicine_name = st.sidebar.text_input("Enter Medicine Name")

number = st.sidebar.slider("Number of Options",1,10,5)

med_name = []
med_price = []

# -------------------------------

if medicine_name:

    if st.sidebar.button("Compare Price"):

        inline_shopping_results = compare(medicine_name)

        st.sidebar.image(inline_shopping_results[0].get("thumbnail"))

        lowest_price = float(inline_shopping_results[0].get("price")[1:])
        lowest_price_index = 0

        st.subheader("Available Options")

        for i in range(number):

            col1, col2, col3 = st.columns([1,3,2])

            current_price = float(inline_shopping_results[i].get("price")[1:])

            med_name.append(inline_shopping_results[i].get("source"))
            med_price.append(current_price)

            if current_price <= lowest_price:
                lowest_price = current_price
                lowest_price_index = i

            with col1:
                st.image(inline_shopping_results[i].get("thumbnail"), width=100)

            with col2:
                st.markdown(
                    f"### {inline_shopping_results[i].get('title')[0:50]}"
                )
                st.write(
                    "**Company:**",
                    inline_shopping_results[i].get("source")
                )

            with col3:
                st.success(inline_shopping_results[i].get("price"))

                url = inline_shopping_results[i].get("link")

                if url:
                    st.link_button("Buy Now", url)
                else:
                    st.write("Link not available")

            st.divider()

        # -------------------------------
        # BEST OPTION

        st.subheader("🏆 Best Price Option")

        best = inline_shopping_results[lowest_price_index]

        col1, col2 = st.columns([1,3])

        with col1:
            st.image(best.get("thumbnail"), width=150)

        with col2:

            st.metric(
                label="Best Price",
                value=best.get("price")
            )

            st.write("**Company:**", best.get("source"))

            url = best.get("link")

            if url:
                st.link_button("Buy From Here", url)

        st.divider()

        # -------------------------------
        # CHART

        st.subheader("📊 Price Comparison")

        df = pd.DataFrame({
            "Store": med_name,
            "Price": med_price
        })

        st.bar_chart(df.set_index("Store"))

        col1, col2 = st.columns(2)

        with col1:

            fig, ax = plt.subplots()

            ax.pie(
                med_price,
                labels=med_name,
                autopct='%1.1f%%',
                startangle=90
            )

            ax.axis("equal")

            st.pyplot(fig)

        with col2:

            st.dataframe(df)