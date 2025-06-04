# Python NBA Database

## Overview

This project is designed to populate and maintain a local SQLite database containing NBA player information and their career accolades. It leverages the **nba\_api** library to retrieve data from official NBA endpoints and stores validated results using **pandera** schemas. To ensure robust data retrieval, the project fetches and validates a list of HTTP proxies to distribute requests and handle rate limits.

## Features

* Fetch all current and historical NBA player IDs.
* Retrieve detailed player information (e.g., name, birthdate, position, team history, career statistics).
* Retrieve player accolades (e.g., awards, honors) and store them as JSON strings.
* Validate data frames against strict schemas before insertion into the database.
* Use concurrent workers (via multiprocessing) to speed up data retrieval.
* Store data in a local SQLite database (`nba_db.db` by default).

## Repository Structure

```
├── src/
│   ├── api/
│   │   ├── nba_api.py         # Functions for retrieving and validating player data and accolades
│   │   └── proxies.py         # Functions for fetching and validating HTTP proxies
│   ├── db/
│   │   ├── connection.py      # Utility for creating a SQLite connection
│   │   ├── models.py          # Pandera DataFrameModel schemas for validation
│   │   └── tables.py          # SQL table creation scripts
│   └── main.py               # Main script to orchestrate fetching proxies and populating the database
├── requirements.txt           # Python dependencies
├── LICENSE                    # GNU GPL v3 license text
└── .gitignore                 # Ignored files and folders (e.g., SQLite output)
```

## Prerequisites

1. **Python 3.8+** (recommended)
2. A working internet connection to access NBA endpoints and proxy lists.
3. **SQLite** installed (the project writes to a local `.db` file).

## Installation

1. **Clone the repository**

   ```bash
   git clone <repository_url>
   cd python-nba-database
   ```

2. **Create and activate a virtual environment** (optional but recommended)

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Adjust configuration (if needed)**

   * The default database file is defined in `src/main.py` as `out/nba_db.db`. You can modify the path by editing the call to `get_db_conn(...)`.
   * Ensure write permissions for the target directory. The script will automatically create the `out/` directory if it does not already exist.

2. **Run the main script**

   ```bash
   python3 src/main.py
   ```

   This will perform the following steps:

   * Create the `out/` directory (if missing).
   * Fetch and validate a list of HTTP proxies.
   * Create the required SQLite tables (`player` and `new_player_accolades`).
   * Retrieve all NBA player IDs and download their personal and career data.
   * Validate and save player information to the `player` table.
   * Retrieve and validate each player’s accolades, then save to `new_player_accolades`.
   * Close the database connection.

3. **Inspect the database**

   * Use any SQLite client (e.g., `sqlite3`, DB Browser for SQLite) to open `out/nba_db.db` and inspect tables.

## Configuration

* **Proxy Sources**: `src/api/proxies.py` fetches from two public GitHub-hosted text lists. You may replace these URLs with your own sources if needed.
* **Concurrency**: Both data-fetching functions use a pool size of 250 workers. Adjust `Pool(250)` to a lower number if you encounter resource constraints.
* **Timeouts and Retries**:

  * Player and accolade retrieval functions retry indefinitely on `RequestException` until a valid response or a `ValueError` (which results in skipping that player).
  * The schema validation step uses **pandera** in strict mode, which will halt on any schema mismatch. Customize in `src/db/models.py` if you need more permissive behavior.

## Data Schemas

* **PlayerSchema** (`src/db/models.py`): Defines all expected columns (e.g., `id`, `first_name`, `last_name`, `birthdate`, `team_history`, etc.) and performs type coercion.
* **PlayerAccoladesSchema**: Ensures each row contains `player_id` (integer) and `accolades_object` (stringified JSON).

## Table Definitions

* **player** (`src/db/tables.py`): Stores all player attributes with `id` as the primary key.
* **new\_player\_accolades**: Stores one-to-one mapping (`player_id`) to a JSON text field of that player’s accolades.

## Troubleshooting

* **No valid proxies found**: If the script prints `No valid proxies could be found, try again.`, verify your internet connection and ensure the proxy URLs are reachable and return plain text lists.
* **Schema validation errors**: If pandera raises schema errors, inspect the printed `failure_cases` and adjust the schema in `src/db/models.py` or update data extraction logic.
* **Timeouts**: Increase `timeout` values in `nba_api.py` if requests are timing out frequently.
* **Database locked**: Ensure no other process is accessing the SQLite DB simultaneously, or consider reducing concurrency.

## Contributing

* Feel free to submit pull requests for bug fixes or new features.
* Please follow the existing code style and ensure all new data fields are reflected in the pandas schemas.

## License

This project is licensed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE) for details.
