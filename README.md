# ⚽ FootLens Analytics
### Player Injuries & Team Performance Dashboard

## 📌 About the Project

**FootLens Analytics** is an interactive football analytics dashboard developed using Python and Streamlit. It analyses player injury records, recovery duration, player performance, and team-level trends through interactive charts and visualisations.

The main goal of this project is to transform football data into meaningful insights that can help users explore injury patterns and understand their possible relationship with player and team performance.

## ✨ Features

- 📊 **Executive Dashboard:** Displays key metrics and an overview of the available football data.
- 🏥 **Injury Intelligence:** Analyses injury categories, recovery periods, and injury trends.
- 👤 **Player Analysis:** Explores individual player records and performance trends when the required data is available.
- 🏆 **Team Analysis:** Compares injury records and available team performance indicators.
- 📈 **Interactive Visualisations:** Uses charts, graphs, heatmaps, and scatter plots to present data.
- 🔍 **Interactive Filters:** Filter records by team, player, injury type, and available date ranges.
- 📅 **Monthly Trends:** Examines how injury records change over time.
- 📥 **CSV Export:** Allows users to download filtered data for further analysis.
- 🎨 **Modern Interface:** Features a professional dark sports-technology design.
- 🧹 **Data Cleaning:** Standardises recognised column names and prepares data for analysis.

*The available charts and insights depend on the columns present in the dataset.*

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming and data analysis |
| Streamlit | Interactive web application |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical operations |
| Plotly Express | Interactive data visualisation |
| OpenPyXL | Reading Excel datasets |
| GitHub | Version control and project hosting |
| Streamlit Community Cloud | Online deployment |

## 📂 Project Structure

```text
football-analytics/
│
├── app.py
├── requirements.txt
├── football_data.csv
└── README.md
```

**Note:** The dataset filename shown above is an example. Use a supported filename recognised by the application, or update the data-loading code if your dataset uses another name.

## 🚀 Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Move into the project folder:

```bash
cd YOUR-REPOSITORY
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your actual GitHub details.

### Step 2: Install Dependencies

Ensure that your `requirements.txt` contains:

```text
streamlit
pandas
numpy
plotly
openpyxl
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

### Step 3: Add the Dataset

Place your football dataset in the same folder as `app.py`.

The application supports recognised CSV and Excel filenames. The dataset should contain relevant football information, such as player names, teams, injury types, injury dates, recovery duration, match dates, or player ratings, depending on the analysis you want to perform.

### Step 4: Run the Application

Execute the following command:

```bash
streamlit run app.py
```

The dashboard will open in your browser using the local address provided by Streamlit.

## ☁️ Deployment on Streamlit Community Cloud

1. Upload `app.py`, `requirements.txt`, the dataset you are permitted to share, and `README.md` to your GitHub repository.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in using your GitHub account.
4. Create a new application and select your repository.
5. Select the correct branch.
6. Set the main file path to `app.py`, or use your actual Python filename.
7. Click **Deploy**.
8. Once deployment is complete, open the application URL and test the dashboard.

### Common Deployment Errors

- If `ModuleNotFoundError: No module named 'plotly'` appears, check that `plotly` is listed in `requirements.txt`.
- Ensure that `requirements.txt` is in the repository root.
- Check that the main file path matches the exact filename in GitHub.
- Confirm that the dataset has been uploaded and uses a supported filename.
- Review the application logs if deployment fails.

## 📊 Data Analysis Workflow

The project follows these main stages:

1. **Data Collection:** Load the available football dataset.
2. **Data Cleaning:** Standardise recognised column names and prepare dates, numerical values, and missing text fields.
3. **Feature Engineering:** Derive additional fields, such as injury duration and month or year, when the necessary data is available.
4. **Exploratory Data Analysis:** Investigate patterns and relationships within the dataset.
5. **Data Visualisation:** Present the results using interactive charts and graphs.
6. **Dashboard Development:** Combine the analysis into a user-friendly Streamlit application.
7. **Interpretation:** Use the visualisations to explore possible insights into player injuries and team performance.

## ❓ Business Questions

FootLens Analytics is designed to investigate questions such as:

1. Which injury categories occur most frequently in the dataset?
2. How does recovery duration vary across different injury categories?
3. How do recorded injuries change across months or seasons?
4. Which players have the highest number of recorded injury cases?
5. Which players have the longest recorded recovery periods?
6. How do team injury records compare with available performance indicators?
7. Where match dates and ratings are available, how do player ratings change over time?
8. Is there a pattern between player age and the project's Injury Impact Index?

The answers depend on the quality and availability of the relevant dataset columns.

## 📈 Visualisations

Depending on the available data, the dashboard may include:

- Injury category comparison charts
- Monthly injury trend charts
- Recovery duration distributions
- Team and month heatmaps
- Player performance timelines
- Player age versus injury indicator scatter plots
- Team injury volume comparisons
- Match-result distributions
- Player and team summary tables

These visualisations help users explore the dataset and identify patterns more easily.

## ⚠️ Data Limitations and Responsible Interpretation

- Results depend on the accuracy and completeness of the dataset.
- Missing or inconsistent values may affect calculations and visualisations.
- A relationship between two variables does not necessarily prove causation.
- Comparisons may be misleading when players or teams have different amounts of recorded data.
- The **Injury Impact Index** is a project-defined analytical indicator, not an official statistic, medical diagnosis, or validated clinical measure.
- Recovery duration should be interpreted according to how it is defined in the source dataset.
- The dashboard is intended for educational and exploratory data analysis, not medical advice or professional selection decisions.

## 🔮 Future Improvements

Possible future developments include:

- Adding more seasons and competitions.
- Including additional player and team performance metrics.
- Improving data validation and missing-value reporting.
- Developing predictive models after collecting and validating suitable data.
- Comparing teams using matches played or other relevant measures.
- Adding more filters and custom reporting features.

## 🎯 Project Objective

The objective of FootLens Analytics is to demonstrate practical skills in Python programming, data cleaning, exploratory data analysis, data visualisation, dashboard development, and application deployment.

By combining football injury records with interactive visualisations, the project provides a structured way to explore data-driven questions about players and teams.

## 👨‍💻 Developed As

A student project for **Mathematics for AI / Artificial Intelligence**, demonstrating the application of data analytics and visualisation to football-related information.

## 📄 License

No license has been specified for this project. Add a `LICENSE` file if you intend to define permissions for using, modifying, or distributing the code.



story board link:https://canva.link/9v7iie7026i551a 

## 📚 References and Citations

The following official documentation and technical resources were used as references for the technologies and methods applied in FootLens Analytics.

1. **Python Software Foundation.** *Python Documentation.*  
   https://docs.python.org/3/

2. **Pandas Development Team.** *Pandas Documentation.*  
   https://pandas.pydata.org/docs/  
   Used as a reference for data cleaning, data manipulation, and tabular data analysis.

3. **NumPy Developers.** *NumPy Documentation.*  
   https://numpy.org/doc/  
   Used as a reference for numerical operations and array-based calculations.

4. **Streamlit, Inc.** *Streamlit Documentation.*  
   https://docs.streamlit.io/  
   Used as a reference for developing interactive dashboards, filters, metrics, and data applications.

5. **Plotly Technologies Inc.** *Plotly Python Graphing Library.*  
   https://plotly.com/python/  
   Used as a reference for creating interactive data visualisations and charts.

6. **OpenPyXL Contributors.** *OpenPyXL Documentation.*  
   https://openpyxl.readthedocs.io/en/stable/  
   Used as a reference for working with Excel spreadsheet files.

7. **Streamlit, Inc.** *Streamlit Community Cloud Documentation.*  
   https://docs.streamlit.io/deploy/streamlit-community-cloud  
   Used as a reference for deploying and sharing the dashboard online.

8. **GitHub, Inc.** *GitHub Documentation.*  
   https://docs.github.com/  
   Used as a reference for repository management, source-code hosting, and project documentation.

### Citation Note

These references provide documentation for the software libraries, data-analysis techniques, visualisation tools, and deployment workflow used in the project. They are technical references rather than sources for football injury statistics. Any findings presented by the dashboard depend on the dataset used for analysis.

If an external football dataset is used, its original source, author or organisation, dataset title, URL, and access date should also be cited here.
