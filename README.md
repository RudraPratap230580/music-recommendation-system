# 🎶 Music Recommendation System

<div align="center">

&#x20;<!-- TODO: Add an actual project logo/banner, perhaps a visualization or icon related to music and AI -->

[!\[GitHub stars](https://img.shields.io/github/stars/RudraPratap230580/music-recommendation-system?style=for-the-badge)](https://github.com/RudraPratap230580/music-recommendation-system/stargazers)

[!\[GitHub forks](https://img.shields.io/github/forks/RudraPratap230580/music-recommendation-system?style=for-the-badge)](https://github.com/RudraPratap230580/music-recommendation-system/network)

[!\[GitHub issues](https://img.shields.io/github/issues/RudraPratap230580/music-recommendation-system?style=for-the-badge)](https://github.com/RudraPratap230580/music-recommendation-system/issues)

[!\[GitHub license](https://img.shields.io/github/license/RudraPratap230580/music-recommendation-system?style=for-the-badge)](LICENSE)

**A content-based music recommendation engine built with Python, utilizing cosine similarity and Streamlit to suggest tracks based on audio features.**

[Live Demo](https://share.streamlit.io/RudraPratap230580/music-recommendation-system/app.py) <!-- TODO: Verify or add a live Streamlit Cloud deployment link -->

</div>

## 📖 Overview

This project implements a content-based music recommendation system that suggests songs to users based on the audio characteristics of a selected track. By analyzing various audio features such as danceability, energy, valence, and tempo, the system leverages cosine similarity to find songs that are acoustically similar, offering a personalized discovery experience.

The application features an interactive web interface built with Streamlit, allowing users to easily select a song and receive instant recommendations. The underlying data is sourced from Spotify, with a dedicated script for fetching and processing track information and their corresponding audio features. This makes it a robust tool for exploring music based on sonic profiles rather than collaborative filtering.

## ✨ Features

* 🎯 **Content-Based Recommendations**: Suggests tracks based on their intrinsic audio features, providing a deeper level of personalization.
* 🎼 **Audio Feature Analysis**: Utilizes a comprehensive set of audio features (e.g., danceability, energy, acousticness, instrumentalness, tempo, loudness, speechiness, liveness, valence, duration\_ms) to determine similarity.
* 📐 **Cosine Similarity Algorithm**: Employs cosine similarity for robust and efficient calculation of similarity scores between tracks.
* 🚀 **Interactive Web Interface**: A user-friendly front-end developed with Streamlit for easy song selection and recommendation display.
* 🎶 **Dynamic Dataset Generation**: Includes a script to fetch and process Spotify track data and audio features, enabling dataset updates.
* 🔍 **Search \& Select**: Allows users to select a song from a pre-loaded list to get recommendations.

## 🖥️ Screenshots

<!-- TODO: Add actual screenshots of the Streamlit application interface.
Example:

!\[Screenshot of Main Interface](images/screenshot-main.png)

!\[Screenshot of Recommendations](images/screenshot-recs.png)

Currently, no screenshots are available. Please run the application locally to view the interface.

## 🛠️ Tech Stack

**Backend \& Data Science:**

[!\[Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)

[!\[Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)](https://streamlit.io/)

[!\[Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)](https://pandas.pydata.org/)

[!\[NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge\&logo=numpy\&logoColor=white)](https://numpy.org/)

[!\[Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge\&logo=scikit-learn\&logoColor=white)](https://scikit-learn.org/stable/)

[!\[Spotipy](https://img.shields.io/badge/Spotipy-1DB954?style=for-the-badge\&logo=spotify\&logoColor=white)](https://spotipy.readthedocs.io/)

**Data Storage:**

[!\[CSV](https://img.shields.io/badge/CSV-000000?style=for-the-badge\&logo=apache-airflow\&logoColor=white)](https://en.wikipedia.org/wiki/Comma-separated_values)

## 🚀 Quick Start

Follow these steps to get the Music Recommendation System up and running on your local machine.

### Prerequisites

* Python 3.x
* `pip` (Python package installer)

### Installation

1. **Clone the repository**

&#x20;   ```bash
    git clone https://github.com/RudraPratap230580/music-recommendation-system.git
    cd music-recommendation-system
    ```

2. **Install dependencies**
All required Python packages are listed in `requirements.txt`.

&#x20;   ```bash
    pip install -r requirements.txt
    ```

3. **Environment setup (for dataset generation)**
The `generate\_dataset.py` script uses the Spotify Web API. You'll need Spotify Developer credentials.

   * Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   * Log in and create a new application to get your `Client ID` and `Client Secret`.
   * Create a `.env` file in the project root directory and add your credentials:

```ini
        SPOTIPY\_CLIENT\_ID="your\_spotify\_client\_id"
        SPOTIPY\_CLIENT\_SECRET="your\_spotify\_client\_secret"
        ```

   * *Note*: The main `app.py` directly uses the pre-existing `spotify\_tracks.csv`, so Spotify API keys are only strictly necessary if you wish to run `generate\_dataset.py` yourself to update or create the dataset.
4. **Data preparation (optional, if you want to regenerate `spotify\_tracks.csv`)**
The project comes with a `spotify\_tracks.csv` file. If you wish to regenerate it with fresh data or different parameters, run:

&#x20;   ```bash
    python generate\_dataset.py
    ```

   This script will fetch data from Spotify based on the `SPOTIPY\_CLIENT\_ID` and `SPOTIPY\_CLIENT\_SECRET` configured in your `.env` file.

5. **Start development server**
The application runs using Streamlit.

   &#x20;   ```bash
    streamlit run app.py
    ```

6. **Open your browser**
Streamlit will typically open the application in your default web browser at `http://localhost:8501`. If it doesn't, visit the URL provided in your terminal.

   ## 📁 Project Structure

   ```
music-recommendation-system/
├── \_\_pycache\_\_/             # Python bytecode cache
├── app.py                   # Main Streamlit application file
├── generate\_dataset.py      # Script to generate/update the spotify\_tracks.csv dataset
├── recommender.py           # Core recommendation logic (e.g., similarity calculation)
├── requirements.txt         # List of Python dependencies
├── spotify\_tracks.csv       # Dataset containing Spotify track information and audio features
└── .env                     # Environment variables for Spotify API credentials (add manually)
```

   ## ⚙️ Configuration

   ### Environment Variables

   For the `generate\_dataset.py` script to function, the following environment variables are required:

   | Variable              | Description                                   | Default | Required |

   |-----------------------|-----------------------------------------------|---------|----------|

   | `SPOTIPY\_CLIENT\_ID`   | Your Client ID from Spotify Developer Dashboard | None    | Yes      |

   | `SPOTIPY\_CLIENT\_SECRET` | Your Client Secret from Spotify Developer Dashboard | None    | Yes      |

   These should be placed in a `.env` file in the root directory or set as system environment variables.

   ### Configuration Files

* `requirements.txt`: Defines all Python package dependencies.
* `.env`: (User-created) Stores sensitive API keys.

  ## 🔧 Development

  ### Available Scripts

* `python generate\_dataset.py`: Executes the script to fetch Spotify data and generate/update `spotify\_tracks.csv`. Requires Spotify API credentials.
* `streamlit run app.py`: Starts the Streamlit web application locally.

  ### Development Workflow

1. Set up your Spotify API credentials in a `.env` file if you plan to modify or regenerate the dataset.
2. Run `generate\_dataset.py` to ensure you have an up-to-date `spotify\_tracks.csv`.
3. Modify `recommender.py` to adjust the recommendation logic (e.g., feature weighting, different similarity metrics).
4. Update `app.py` to change the UI, display additional information, or integrate new features.
5. Test changes by running `streamlit run app.py` and interacting with the local application.

   ## 🧪 Testing

   &#x20;Testing primarily involves:

* **Manual UI Testing**: Interacting with the Streamlit application to ensure recommendations are displayed correctly and the interface is responsive.
* **Logic Validation**: Verifying the output of `recommender.py` functions by inspecting similarity scores and recommended tracks for known inputs.
* **Data Integrity**: Checking the `spotify\_tracks.csv` generated by `generate\_dataset.py` for completeness and correctness.

  ## 🚀 Deployment

  Deployed on streamlit:
Deploymed Link -> https://music-recommendation-system-n7ttzmqy3pz8ddopofmugn.streamlit.app

  ### Streamlit Community Cloud

1. Ensure your `requirements.txt` is up-to-date.
2. Make sure your Spotify API keys are configured as Streamlit secrets if you intend to run `generate\_dataset.py` on the cloud or if your `app.py` directly uses the API (which it currently doesn't for the main recommendation flow).
3. Connect your GitHub repository to Streamlit Community Cloud and deploy the `app.py` file.

   ## 🤝 Contributing

   We welcome contributions! Please feel free to open issues or submit pull requests.

   ### Development Setup for Contributors

   The development setup is the same as the Quick Start guide. Ensure all prerequisites are met and dependencies are installed.

   ## 📄 License

   This project is licensed under the [MIT License](LICENSE) - see the [LICENSE](LICENSE) file for details.

   ## 🙏 Acknowledgments

* **Spotify Web API**: For providing access to a vast catalog of music and audio features, essential for this recommendation system.
* **Streamlit**: For simplifying the creation of interactive data applications in Python.
* **Scikit-learn**: For robust machine learning tools, particularly cosine similarity.
* **Pandas \& NumPy**: For efficient data manipulation and numerical operations.

  ## 📞 Support \& Contact

* 🐛 Issues: [GitHub Issues](https://github.com/RudraPratap230580/music-recommendation-system/issues)

  \---

  <div align="center">

  **⭐ Star this repo if you find it helpful!**

  Made with ❤️ by [RudraPratap230580](https://github.com/RudraPratap230580)

  </div>

