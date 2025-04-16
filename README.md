# Gemini_Sql_query_and_table_generator

A tool that automatically generates SQL queries from natural language prompts. This project creates an SQLite database using Python, describes the database structure to Gemini via an initial prompt, and then uses natural language queries to generate and execute SQL code that retrieves data from the database.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)
- [Acknowledgements](#acknowledgements)

## Overview

Gemini_Sql_query_and_table_generator is an innovative project that bridges natural language processing (NLP) with relational database management. Using Python's SQLite module, the project programmatically creates and populates a database. An initial prompt describes the database schema to Gemini, enabling it to understand available tables and columns. Users then interact with the system by providing natural language prompts that are converted into SQL queries, automatically executed against the database to retrieve the requested data.

## Features

- **Automated Database Creation:** Leverages Python's SQLite module to create and set up the database.
- **Schema Description Prompt:** The database schema is described to Gemini via a well-defined initial prompt.
- **Natural Language to SQL Conversion:** Users can input data retrieval queries in plain language, which are then translated into SQL statements.
- **Automated Query Execution:** Generated SQL queries are injected into the database automatically to fetch and return data.
- **User-Friendly Data Access:** Simplifies data exploration for users with limited SQL knowledge.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/Srinivas23132/Gemini_Sql_query_and_table_generator.git
    cd Gemini_Sql_query_and_table_generator
    ```

2. **Create a Virtual Environment (Optional but Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Application:**

    ```bash
    python main.py
    ```

2. **Interact with Gemini:**

    - The application first describes the SQLite database schema via an initial prompt.
    - Enter your natural language query when prompted.
    - The system generates the corresponding SQL code and executes it to retrieve the desired data.
    - The results are then displayed in an accessible format.

## Project Structure

Gemini_Sql_query_and_table_generator/ ├── README.md ├── main.py ├── requirements.txt ├── database/ │ └── setup.py ├── prompts/ │ └── initial_prompt.txt └── utils/ └── sql_generator.py


## Contributing

Contributions are welcome! To contribute:

1. **Fork the Repository.**
2. **Create a New Branch** for your feature or bug fix.
3. **Commit Your Changes.**
4. **Open a Pull Request** with a clear description of your modifications.

## License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contact

- **Name:** Srinivas D
- **GitHub:** [Srinivas23132](https://github.com/Srinivas23132)
- **Email:** your.email@example.com

## Acknowledgements

- Special thanks to all contributors and the community for valuable feedback.
- Inspired by similar projects and tutorials demonstrating the integration of NLP with databases.
