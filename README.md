# Rotom's Seed Search Bot

Welcome to Rotom's Seed Search Bot! This bot helps you search for Pokémon seeds across different maps in the Scarlet and Violet games.

## Features

- **Search Seeds by Pokémon Name**: Find specific Pokémon seeds by specifying the game, map, and Pokémon name.
- **Browse Seeds by Rewards**: Search for Pokémon seeds based on the rewards they provide.
- **Random Shiny Search**: Get a random shiny Pokémon seed from the specified game and map.

## How-To

There are multiple commands you can use to search for seeds:

### `!rewards`
The bot will DM you asking for the game, map, and "Reward" type, then display a browsable embed for you to look through the matching seeds.

### `!search`
The bot will DM you asking for the game, map, and Pokémon name, then display a browsable embed for you to look through the matching seeds.

### `!randomshiny`
The bot will DM you asking for the game and map, then display a random shiny Pokémon seed.

### `!invite`
Provides an invite link to add the bot to another server.

### `!info`
Provides information about what the bot does and a link to the GitHub repository.

## Installation

### Prerequisites

- Python 3.8 or higher
- Discord Bot Token

### Step-by-Step Guide

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo-url.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd your-repo-url
    ```

3. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

4. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Create a `.env` file in the project directory and add your bot token:**
    ```env
    DISCORD_TOKEN=your_discord_token
    ```

6. **Create the JSON files for raid seeds:**

    The bot requires JSON files for each map (Paldea, Kitakami, Blueberry) with the raid seed information. Each JSON file should be structured as follows:

    ```json
    [
        {
            "Pokemon": "Pikachu",
            "Tera": "Electric",
            "IsShiny": "yes",
            "HP": 35,
            "Atk": 55,
            "Def": 40,
            "SpA": 50,
            "SpD": 50,
            "Spe": 90,
            "Ability": "Static",
            "Nature": "Jolly",
            "Gender": "Male",
            "Height": "0.4 m",
            "Weight": "6.0 kg",
            "Scale": "1.0",
            "Seed": "12345678",
            "Rewards": "Thunder Stone",
            "Difficulty": "3 Stars"
        },
        ...
    ]
    ```

    Create directories for each game (`Scarlet` and `Violet`) and place the corresponding JSON files in those directories. For example:

    ```
    Scarlet/
    ├── paldea.json
    ├── kitakami.json
    └── blueberry.json
    Violet/
    ├── paldea.json
    ├── kitakami.json
    └── blueberry.json
    ```

    Each JSON file should contain an array of Pokémon objects with the attributes shown above.

7. **Run the bot:**
    ```bash
    python bot.py
    ```

## Usage

Invite the bot to your server using the invite link provided by the `!invite` command. Once the bot is in your server, you can use the commands listed above to search for Pokémon seeds.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## GitHub Repository

[Source Code]([https://github.com/your-repo-url](https://github.com/Boneless0019/Raid-Seed-Search-Bot))
