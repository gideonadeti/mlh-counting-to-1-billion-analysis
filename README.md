# MLH Counting to 1 Billion Analysis

A Streamlit web application for analyzing counting progress data from the MLH Discord channel where members are collectively counting up to 1 billion. Upload your CSV data and get comprehensive insights, metrics, and visualizations of your counting progress.

**Live Demo:** [MLH Counting to 1 Billion Analysis](https://mlh-counting-to-1-billion-analysis.streamlit.app)

## Table of Contents

- [MLH Counting to 1 Billion Analysis](#mlh-counting-to-1-billion-analysis)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Running Locally](#running-locally)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Application](#running-the-application)
    - [CSV Format](#csv-format)
  - [Deployment](#deployment)
    - [Streamlit Community Cloud](#streamlit-community-cloud)
  - [Contributing](#contributing)

## Features

- **CSV File Upload & Validation**
  - Validates required columns (date, from, to, count)
  - Validates data types and format
  - Checks for date duplicates and chronological ordering
  - Validates business logic rules (to >= from, count = to - from + 1)

- **Key Metrics Dashboard**
  - Current Standing: Highest number reached so far
  - Completion Percentage: Progress toward 1 billion
  - Daily Throughput: Average numbers counted per day
  - Peak Performance: Maximum count in a single day (with date)
  - Estimated Completion Time: Projected time to reach 1 billion (in years)

- **Data Visualizations**
  - Progress Over Time: Cumulative line chart showing counting progress
  - Daily Activity: Bar chart displaying daily counting activity patterns

- **Data Preview**: View your uploaded data in an interactive table

## Technologies Used

- **Python 3.x**
- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Altair** - Statistical data visualization
- **Arrow** - Human-friendly date formatting

## Running Locally

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/gideonadeti/mlh-counting-to-1-billion-analysis.git
cd mlh-counting-to-1-billion-analysis
```

1. Create a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### CSV Format

Your CSV file should contain the following columns:

- `date` - Date of the counting entry (any parseable date format)
- `from` - Starting number for that day
- `to` - Ending number for that day
- `count` - Total count for that day (should equal to - from + 1)

## Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Set the main file path to `app.py`
7. Deploy!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
