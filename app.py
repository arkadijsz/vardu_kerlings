import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Vārdu Kērlings",  # Set the page title here
    page_icon=":crown:",  # You can also set an icon
)

# Load the CSV data with UTF-8 encoding
df = pd.read_csv("names.csv", encoding="utf-8")

st.title("Vārdu Kērlings") 
st.subheader("Ballīšu spēle par to, cik labi Tu un Tavi draugi zina latviešus") 

# Instructions
st.write("""
Uzvar spēlētājs, kura izvēlētā vārda popularitāte ir vistuvāk sākotnējā vārda izplatībai Latvijā.
         
**Instrukcijas:**

1. **Ievadiet sākotnējo vārdu.** Šis vārds kalpos kā atskaites punkts.
2. **Izvēlieties spēlētāju skaitu.**
3. **Nospiediet "Sākt spēli".**
4. **Katrs spēlētājs ievada savu vārdu.**
5. **Nospiediet "Iesniegt", lai redzētu rezultātus.**

""")


# Get the initial name
initial_name = st.text_input("Ievadiet sākotnējo vārdu:") 

# Get the number of players
num_players = st.number_input("Spēlētāju skaits:", min_value=2, step=1) 

# --- Function definitions ---

def calculate_popularity_scores(names):
    # Check if the "Vardi" column exists
    if "Vardi" not in df.columns:
        raise ValueError("Kolonna 'Vardi' nav atrasta CSV failā.") 

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
    st.write(f"Sākotnējais vārds: {initial_name}, Popularitāte: {initial_name_popularity}")  

    # If the initial name is not found, disqualify everyone
    if initial_name_popularity == 0:
        st.write("Nav uzvarētāja - sākotnējais vārds netika atrasts!")  
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
            st.write(f"Spēlētājs {i+1}: {player_name} - Diskvalificēts (vārds nav atrasts)") 
        else:
            all_disqualified = False  # At least one player is not disqualified
            st.write(f"Spēlētājs {i+1}: {player_name}, Popularitāte: {player_popularity}, Starpība: {net_difference}")  

    # Display the winner or "No winner" message
    if all_disqualified:
        st.write("Nav uzvarētāja - visi vārdi tika diskvalificēti!")  
    else:
        winner_name = player_names[winner_index]  # Corrected line position
        st.write(f"Uzvarētājs: {winner_name}") 

# --- Game logic ---

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if st.button("Sākt spēli"): 
    st.session_state.game_started = True

if st.session_state.game_started:
    # Create input fields for each player
    for i in range(num_players):
        st.text_input(f"Spēlētāja {i+1} vārds:", key=f"player_{i}") 

    if st.button("Iesniegt"): 
        # Get the player names from the session state
        player_names = [st.session_state[f"player_{i}"] for i in range(num_players)]

        # Calculate popularity scores and determine the winner
        player_scores, winner_index = calculate_popularity_scores(player_names)

        # Display the results
        display_results(initial_name, player_names, player_scores, winner_index)

# Display the data source
st.write("Dati no PMLP, iegūti izmantojot Atvērto datu portālu. Dati uz 2024. gada 7. jūliju")