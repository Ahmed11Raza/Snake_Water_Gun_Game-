import random
import time
from collections import Counter
import tkinter as tk
from tkinter import messagebox

# Initialize global variables
player_score = 0
computer_score = 0
player_history = []
rounds = 5
current_round = 0
difficulty = 'Medium'
game_over = False
special_rounds = []

def get_computer_choice(difficulty, player_history):
    """Determine computer's move based on difficulty and player history"""
    choices = ['Snake', 'Water', 'Gun']
    
    if difficulty == 'Easy':
        return random.choice(choices)
    
    elif difficulty == 'Medium' and len(player_history) > 2:
        last_choice = player_history[-1]
        if random.random() < 0.6:  # 60% chance to counter the last move
            return 'Gun' if last_choice == 'Snake' else 'Snake' if last_choice == 'Water' else 'Water'
    
    elif difficulty == 'Hard' and player_history:
        most_common_move = Counter(player_history).most_common(1)[0][0]
        return 'Gun' if most_common_move == 'Snake' else 'Snake' if most_common_move == 'Water' else 'Water'
    
    return random.choice(choices)

def determine_winner(player_choice, computer_choice):
    """Determine the winner based on choices"""
    if player_choice == computer_choice:
        return 'Draw'
    elif (player_choice == 'Snake' and computer_choice == 'Water') or \
         (player_choice == 'Water' and computer_choice == 'Gun') or \
         (player_choice == 'Gun' and computer_choice == 'Snake'):
        return 'Player'
    else:
        return 'Computer'

def on_button_click(choice):
    """Handle player's choice button click"""
    global player_score, computer_score, player_history, current_round, game_over
    
    if game_over or current_round >= rounds:
        return
    
    current_round += 1
    is_special_round = current_round in special_rounds
    
    player_history.append(choice)
    computer_choice = get_computer_choice(difficulty, player_history)
    
    winner = determine_winner(choice, computer_choice)
    
    # Prepare result message
    special_text = "🌟 SPECIAL ROUND! Points are doubled! 🌟" if is_special_round else ""
    result_message = f"<div class='round-result'><div class='round-header'>Round {current_round}</div>{special_text}<div class='choices'>You chose <span class='choice {choice.lower()}'>{choice}</span> · Computer chose <span class='choice {computer_choice.lower()}'>{computer_choice}</span></div>"
    
    if winner == 'Player':
        points = 4 if is_special_round else 2
        player_score += points
        result_message += f"<div class='result win'>You win! <span class='points'>+{points} points</span></div>"
    elif winner == 'Computer':
        points = 4 if is_special_round else 2
        computer_score += points
        result_message += f"<div class='result lose'>Computer wins! <span class='points'>+{points} points</span></div>"
    else:
        player_score += 1
        computer_score += 1
        result_message += "<div class='result draw'>It's a draw! <span class='points'>+1 point each</span></div>"
    
    result_message += "</div>"
    
    # Update UI
    update_scoreboard()
    update_game_history(choice, computer_choice, winner, is_special_round)
    
    if current_round >= rounds:
        end_game()

def update_scoreboard():
    """Update the scoreboard and round display"""
    global scoreboard, round_display
    round_display.value = f"<div class='round-tracker'>Round {current_round} of {rounds}</div>"
    progress_pct = (current_round / rounds) * 100
    scoreboard.value = f"<div class='scoreboard'><div class='score-title'>Scoreboard</div><div class='scores'><div class='player-score'><span class='score-label'>Player</span><span class='score-value'>{player_score}</span></div><div class='score-divider'>vs</div><div class='computer-score'><span class='score-label'>Computer</span><span class='score-value'>{computer_score}</span></div></div><div class='progress-bar'><div class='progress' style='width: {progress_pct}%'></div></div></div>"

def update_game_history(player_choice, computer_choice, winner, is_special):
    """Update the game history display"""
    global game_history
    history_item = f"<div class='history-item {winner.lower()}'><div class='history-round'>Round {current_round}{' 🌟' if is_special else ''}</div><div class='history-choices'><span class='choice {player_choice.lower()}'>{player_choice}</span> vs <span class='choice {computer_choice.lower()}'>{computer_choice}</span></div><div class='history-result'>{winner}</div></div>"
    game_history.value = history_item + game_history.value

def start_game(b):
    """Initialize and start a new game"""
    global rounds, difficulty, special_rounds, game_over, current_round
    global player_score, computer_score, player_history
    
    player_score = 0
    computer_score = 0
    player_history = []
    current_round = 0
    game_over = False
    
    difficulty = difficulty_dropdown.value
    try:
        rounds = int(rounds_input.value)
        if rounds <= 0:
            rounds = 5
    except ValueError:
        rounds = 5
    
    num_special = max(1, round(rounds * 0.2))
    special_rounds = random.sample(range(1, rounds + 1), min(num_special, rounds))
    
    setup_box.layout.display = 'none'
    choices_box.layout.display = 'flex'
    round_display.layout.display = 'block'
    scoreboard.layout.display = 'block'
    message_area.layout.display = 'block'
    game_history.layout.display = 'block'
    game_history.value = ""
    
    message_area.value = f"<div class='game-start'><h3>Game Started!</h3><p>Difficulty: <strong>{difficulty}</strong> | Rounds: <strong>{rounds}</strong></p><p>Special rounds: {', '.join(map(str, special_rounds))}</p><p>Make your first move!</p></div>"
    update_scoreboard()

def end_game():
    """End the game and display final results"""
    global game_over, analysis_output, final_result
    game_over = True
    
    if player_score > computer_score:
        result_class = "player-wins"
        winner_text = "Congratulations! You won the game!"
    elif player_score < computer_score:
        result_class = "computer-wins"
        winner_text = "Computer wins the game! Better luck next time."
    else:
        result_class = "draw-game"
        winner_text = "The game is a draw!"
    
    score_diff = abs(player_score - computer_score)
    result = f"<div class='game-over {result_class}'><h2>Game Over!</h2><div class='final-scores'><div class='player-final'><div class='score-label'>Player</div><div class='score-value'>{player_score}</div></div><div class='score-difference'><div class='diff-value'>{score_diff}</div><div class='diff-label'>difference</div></div><div class='computer-final'><div class='score-label'>Computer</div><div class='score-value'>{computer_score}</div></div></div><div class='winner-announcement'>{winner_text}</div></div>"
    
    final_result.value = result
    final_result.layout.display = 'block'
    analysis_output.value = analyze_player_behavior()
    analysis_output.layout.display = 'block'
    restart_button.layout.display = 'block'
    choices_box.layout.display = 'none'

def analyze_player_behavior():
    """Analyze and display player's move patterns"""
    if not player_history:
        return "<p>No moves played yet!</p>"
    
    move_counts = Counter(player_history)
    total_moves = len(player_history)
    
    snake_pct = (move_counts.get('Snake', 0) / total_moves) * 100
    water_pct = (move_counts.get('Water', 0) / total_moves) * 100
    gun_pct = (move_counts.get('Gun', 0) / total_moves) * 100
    
    analysis = f"""
    <div class='analysis'>
        <h3>Player Move Analysis</h3>
        <div class='move-bars'>
            <div class='move-bar'>
                <div class='move-label'>Snake</div>
                <div class='bar-container'>
                    <div class='bar snake' style='width: {snake_pct}%;'></div>
                </div>
                <div class='move-stats'>{move_counts.get('Snake', 0)} ({snake_pct:.1f}%)</div>
            </div>
            <div class='move-bar'>
                <div class='move-label'>Water</div>
                <div class='bar-container'>
                    <div class='bar water' style='width: {water_pct}%;'></div>
                </div>
                <div class='move-stats'>{move_counts.get('Water', 0)} ({water_pct:.1f}%)</div>
            </div>
            <div class='move-bar'>
                <div class='move-label'>Gun</div>
                <div class='bar-container'>
                    <div class='bar gun' style='width: {gun_pct}%;'></div>
                </div>
                <div class='move-stats'>{move_counts.get('Gun', 0)} ({gun_pct:.1f}%)</div>
            </div>
        </div>
    </div>
    """
    
    return analysis

def setup_ui():
    """Setup the user interface for the game"""
    window = tk.Tk()
    window.title("Snake Water Gun Game")

    tk.Label(window, text="Choose Difficulty:").pack()
    difficulty_var = tk.StringVar(value='Medium')
    tk.OptionMenu(window, difficulty_var, 'Easy', 'Medium', 'Hard').pack()

    tk.Label(window, text="Enter Number of Rounds:").pack()
    rounds_entry = tk.Entry(window)
    rounds_entry.pack()

    tk.Label(window, text="Welcome to the Snake Water Gun Game!").pack()
    tk.Label(window, text="Choose your move:").pack()

    tk.Button(window, text="Snake", command=lambda: on_button_click("Snake")).pack()
    tk.Button(window, text="Water", command=lambda: on_button_click("Water")).pack()
    tk.Button(window, text="Gun", command=lambda: on_button_click("Gun")).pack()

    tk.Button(window, text="Start Game", command=start_game).pack()

    window.mainloop()

if __name__ == "__main__":
    setup_ui()
