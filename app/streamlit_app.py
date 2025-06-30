import streamlit as st
import json

from collector import App
from funda import FundaService
from location import LocationService
from life_level import LifeLevelScoreService
from notion_uploader import NotionUploaderService

uploaded_file = st.file_uploader("Upload Parameters From JSON File", type="json")
if uploaded_file:
    content = uploaded_file.getvalue()
    params = json.loads(content)
else:
    params = {}

st.header("Funda Parameters")
funda_search_type = st.selectbox("Search Type", ["Buy", "Rent"], index=0 if "funda_search_type" not in params else ["Buy", "Rent"].index(params["funda_search_type"]))
funda_search_min_price = st.number_input("Min Price", 350000 if "funda_search_min_price" not in params else params["funda_search_min_price"])
funda_search_max_price = st.number_input("Max Price", 450000 if "funda_search_max_price" not in params else params["funda_search_max_price"])
funda_search_days_since = st.number_input("Days Since", 5 if "funda_search_days_since" not in params else params["funda_search_days_since"])
funda_search_property_type = st.selectbox("Property Type", ["House", "Apartment"], index=0 if "funda_search_property_type" not in params else ["House", "Apartment"].index(params["funda_search_property_type"]))

st.header("Location Parameters")
cities = st.text_input("Cities", "Amstelveen,Bussum,Den Haag,Hilversum" if "cities" not in params else params["cities"])
office_s = st.text_input("Office One Address", "Gustav Mahlerlaan 308, Amsterdam, Netherlands" if "office_s" not in params else params["office_s"])
office_v = st.text_input("Office Two Address", "Stationsplein 15, Amsterdam, Netherlands" if "office_v" not in params else params["office_v"])

st.header("Script Parameters")
st.subheader("Google")
with st.expander("Where to get Google API Key?"):
    st.write("""
    This script uses the Google API for collecting ZIP codes from addresses and calculating travel times to selected addresses (Office One Address and Office two Address params). 
    Follow these steps to set up the Google API:

    1. **Create a Google Cloud Project**:
        - Go to the [Google Cloud Console](https://console.cloud.google.com/).
        - Click on the project drop-down and select "New Project".
        - Enter a name for your project and click "Create".

    2. **Enable the Necessary APIs**:
        - In the Google Cloud Console, go to the **API & Services** > **Library**.
        - Enable the following APIs:
            - **Geocoding API**
            - **Distance Matrix API**

    3. **Create API Key**:
        - In the Google Cloud Console, go to **API & Services** > **Credentials**.
        - Click on **Create Credentials** and select **API Key**.
        - Copy the API key and add it to the field Google API Key in this form.
    """)
google_api_key = st.text_input("Google API Key", "" if "google_api_key" not in params else params["google_api_key"], type="password")
st.subheader("Notion")
with st.expander("Where to get Notion params?"):
    st.write("""
    This script interacts with a Notion database to store and manage information about houses. To enable this functionality, you'll need to configure parameters and set up the database in Notion.

    **Copy a Notion Database:**
    Instead of manually creating a database, you can copy a database from the following public example: [Example Notion Database](https://wakeful-nutmeg-ccd.notion.site/14b9a5808bc24271b2444c19a0334965?v=45e4359626cc4a74b65262cfd195d4c2&pvs=4)

    **Open the Example Database:**
    Open the public example database link provided above.

    **Duplicate the Database:**
    - Click on the three dots in the top right corner of the database.
    - Select "Duplicate" to add a copy of the database to your own Notion workspace.

    **Get information from Notion**

    **Notion Secret:**
    You can obtain your Notion Integration secret by creating an integration in Notion:
    - Go to [Notion Integrations](https://www.notion.so/my-integrations)
    - Click on "New Integration" and follow the instructions to create a new integration.
    - Copy the "Internal Integration Secret" and add it to this form in field "Notion Secret".
    - Add connection to your integration from DB: 3 dots in the left upper corner -> Connect to -> Your created integration

    **Notion Database ID:**
    You can find your database ID by opening the database in Notion and copying the part of the URL that comes after notion.so/ and before the ? (if present). For example, in the URL `https://www.notion.so/8c3b832c81884c67966db9098ac188d7`, the database ID is `8c3b832c81884c67966db9098ac188d7`. Add this to the field Notion Database ID.
    """)
notion_database_id = st.text_input("Notion Database ID", "" if "notion_database_id" not in params else params["notion_database_id"])
notion_secret = st.text_input("Notion Secret", "" if "notion_secret" not in params else params["notion_secret"], type="password")

search_availible = google_api_key and notion_database_id and notion_secret

if st.button("Search", type="primary", disabled=not search_availible):
    with st.spinner('Working on it...'):
        app = App(
            notion_uploader_service=NotionUploaderService(notion_secret, notion_database_id),
            life_level_service=LifeLevelScoreService(),
            location_service=LocationService(google_api_key),
            funda_service=FundaService(cities, funda_search_type, funda_search_min_price, funda_search_max_price, funda_search_days_since, funda_search_property_type),
            office_s=office_s,
            office_v=office_v,
        )

        funda_houses = app.run_search_and_upload()
    st.success(f"Found {len(funda_houses)} houses.")

st.download_button(
    label="Save Parameters To JSON File",
    data=json.dumps({
        "funda_search_type": funda_search_type,
        "funda_search_min_price": funda_search_min_price,
        "funda_search_max_price": funda_search_max_price,
        "funda_search_days_since": funda_search_days_since,
        "funda_search_property_type": funda_search_property_type,
        "cities": cities,
        "office_s": office_s,
        "office_v": office_v,
        "google_api_key": google_api_key,
        "notion_database_id": notion_database_id,
        "notion_secret": notion_secret,
    }),
    file_name="funda_search_params.json",
    mime="application/json",
)