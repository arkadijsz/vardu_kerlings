import streamlit as st
import pandas as pd

# Load the CSV data with UTF-8 encoding
df = pd.read_csv("names.csv", encoding="utf-8")

st.title("Vārdu Kērlings Spēle")  # Translated title
st.subheader("Dati par 2024.07.01")  # Translated subheader

# Get the initial name
initial_name = st.text_input("Ievadiet sākotnējo vārdu:")  # Translated prompt

# Get the number of players
num_players = st.number_input("Spēlētāju skaits:", min_value=2, step=1)  # Translated prompt

# --- Function definitions ---

def calculate_popularity_scores(names):
    # Check if the "Vardi" column exists
    if "Vardi" not in df.columns:
        raise ValueError("Kolonna 'Vardi' nav atrasta CSV failā.")  # Translated error message

    # Get the popularity score for the initial name (convert to lowercase)
    initial_name_lower = initial_name.lower()
    initial_name_popularity_array = df[df["Vardi"].str.lower() == initial_name_lower]["Skaits"].values
    initial_name_popularity = initial_name_popularity_array[0] if len(initial_name_popularity_array) > 0 else 0

    # If the initial name is not found, disqualify everyone
    if initial_name_popularity == 0:
        return [float('inf')] * len(names), 0  # Return infinity for all scores

    # Calculate the popularity scores for the player names (convert to lowercase)
    player_scores = []
    for player_name in names:
        player_name_lower = player_name.lower()
        player_popularity_array = df[df["Vardi"].str.lower() == player_name_lower]["Skaits"].values
        player_popularity = player_popularity_array[0] if len(player_popularity_array) > 0 else 0

        if player_popularity == 0:
            player_score = float('inf')  # Assign infinity if disqualified
        else:
            player_score = abs(player_popularity - initial_name_popularity)

        player_scores.append(player_score)

    # Find the index of the winner (the player with the lowest score)
    winner_index = player_scores.index(min(player_scores))

    return player_scores, winner_index

def display_results(initial_name, player_names, player_scores, winner_index):
    # Get the popularity score for the initial name
    initial_name_lower = initial_name.lower()
    initial_name_popularity_array = df[df["Vardi"].str.lower() == initial_name_lower]["Skaits"].values
    initial_name_popularity = initial_name_popularity_array[0] if len(initial_name_popularity_array) > 0 else 0

    # Display the initial name and its popularity
    st.write(f"Sākotnējais vārds: {initial_name}, Popularitāte: {initial_name_popularity}")  # Translated text

    # If the initial name is not found, disqualify everyone
    if initial_name_popularity == 0:
        st.write("Nav uzvarētāja - sākotnējais vārds netika atrasts!")  # Translated text
        return  # Exit the function early

    # Display the player names, their popularity scores, and how far off they were
    all_disqualified = True  # Flag to track if all players are disqualified
    for i in range(num_players):
        player_name = player_names[i]
        player_score = player_scores[i]
        player_name_lower = player_name.lower()
        player_popularity_array = df[df["Vardi"].str.lower() == player_name_lower]["Skaits"].values
        player_popularity = player_popularity_array[0] if len(player_popularity_array) > 0 else 0
        
        net_difference = player_popularity - initial_name_popularity 

        if player_popularity == 0:
            st.write(f"Spēlētājs {i+1}: {player_name} - Diskvalificēts (vārds nav atrasts)")  # Translated text
        else:
            all_disqualified = False  # At least one player is not disqualified
            st.write(f"Spēlētājs {i+1}: {player_name}, Popularitāte: {player_popularity}, Starpība: {net_difference}")  # Translated text

    # Display the winner or "No winner" message
    if all_disqualified:
        st.write("Nav uzvarētāja - visi vārdi tika diskvalificēti!")  # Translated text
    else:
        winner_name = player_names[winner_index]
        st.write(f"Uzvarētājs: {winner_name}")  # Translated text

# --- Game logic ---

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if st.button("Sākt spēli"):  # Translated button text
    st.session_state.game_started = True

if st.session_state.game_started:
    # Create input fields for each player
    for i in range(num_players):
        st.text_input(f"Spēlētāja {i+1} vārds:", key=f"player_{i}")  # Translated prompt

    if st.button("Iesniegt"):  # Translated button text
        # Get the player names from the session state
        player_names = [st.session_state[f"player_{i}"] for i in range(num_players)]

        # Calculate popularity scores and determine the winner
        player_scores, winner_index = calculate_popularity_scores(player_names)

        # Display the results
        display_results(initial_name, player_names, player_scores, winner_index)


# Display the data source
st.write("Dati no PMLP, iegūti izmantojot Atvērto datu portālu.") 