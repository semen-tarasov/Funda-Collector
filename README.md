# Funda Collector

![Example Screenshot](images/example.png)

This script searches for new houses on Funda and sends the data to a specified Notion database. It utilizes the FundaScraper library for scraping house listings and integrates with the Google Maps API for additional data processing.

[Example Notion Database](https://wakeful-nutmeg-ccd.notion.site/14b9a5808bc24271b2444c19a0334965?v=45e4359626cc4a74b65262cfd195d4c2&pvs=4)

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. **Clone the repository**:
    ```sh
    git clone git@github.com:semen-tarasov/Funda-Collector.git
    cd house-searcher
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python3 -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r app/requirements.txt
    ```

## Configuration
A template `.env` file has been created and added to the `app` directory. You need to update this file with your relevant data.

### Google API

This script uses the Google API for collecting ZIP codes from addresses and calculating travel times to selected addresses (OFFICE_S and OFFICE_V variables). 
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
    - Copy the API key and add it to your `.env` file as `GOOGLE_API_KEY`.

### Notion Database

This script interacts with a Notion database to store and manage information about houses. To enable this functionality, you'll need to configure environment variables and set up the database in Notion.

1. **Copy a Notion Database**:
    Instead of manually creating a database, you can copy a database from the following public example: [Example Notion Database](https://wakeful-nutmeg-ccd.notion.site/14b9a5808bc24271b2444c19a0334965?v=45e4359626cc4a74b65262cfd195d4c2&pvs=4).

    1. **Open the Example Database**: Open the public example database link provided above.
    2. **Duplicate the Database**:
        - Click on the three dots in the top right corner of the database.
        - Select "Duplicate" to add a copy of the database to your own Notion workspace.

2. **Get information from Notion**:
    - **Notion Secret**: You can obtain your Notion Integration token (secret) by creating an integration in Notion:
      1. Go to [Notion Integrations](https://www.notion.so/my-integrations).
      2. Click on "New Integration" and follow the instructions to create a new integration.
      3. Copy the "Internal Integration Token" and add it to your `.env` file as `NOTION_SECRET`.
      4. Add connection to your integration from DB: 3 dots in the left upper corner -> Connect to -> Your created integration

    - **Notion Database ID**: You can find your database ID by opening the database in Notion and copying the part of the URL that comes after `notion.so/` and before the `?` (if present). For example, in the URL `https://www.notion.so/8c3b832c81884c67966db9098ac188d7`, the database ID is `8c3b832c81884c67966db9098ac188d7`. Add this to your `.env` file as `NOTION_DATABASE_ID`.

3. **Set up environment variables**:
    Add the following environment variables to your `.env` file:
    ```env
    NOTION_SECRET=your_notion_secret
    NOTION_DATABASE_ID=your_notion_database_id
    ```

### Funda Search

To set search parameters, you need to define values in the `.env` file:

- `CITIES`: Cities or locations from Funda search: better to take them from the Funda search link.

- `FUNDA_SEARCH_TYPE`: Can be "buy" or "rent".
- `FUNDA_SEARCH_MIN_PRICE`: The minimum price for the search.
- `FUNDA_SEARCH_MAX_PRICE`: The maximum price for the search.
- `FUNDA_SEARCH_DAYS_SINCE`: The number of days since the houses were listed.
- `FUNDA_SEARCH_PROPERTY_TYPE`: The type of property to search for.

### Life Level Scores

As the source of information for the current life level score, the script uses data from the Dutch government. The latest version of the file with scores is already included in the `data` folder as of the time of writing this script. By default, no additional actions are required. However, if you want to update the scores, you can follow these instructions:

1. **Download the CSV with information about scores**:
    You can download the CSV with information about scores for different addresses from this link: [Leefbaarometer Opendata](https://www.leefbaarometer.nl/page/Opendata#scores).

2. **Prepare the CSV file**:
    In the downloaded archive, you need the file `Leefbaarometer-scores PC4 {years}.csv`. This file should contain `PC4` and `afw` columns. 

3. **Replace the existing file**:
    Rename this file to `scores.csv` and place it in the `data` folder, replacing the existing file.

## Usage

**Run the script**:
    ```
    python ./app/collector.py
    ```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or bug fixes.

1. **Fork the repository**.
2. **Create a new branch**:
    ```sh
    git checkout -b feature/your-feature-name
    ```
3. **Commit your changes**:
    ```sh
    git commit -m "Add some feature"
    ```
4. **Push to the branch**:
    ```sh
    git push origin feature/your-feature-name
    ```
5. **Open a pull request**.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
