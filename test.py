import os
import sys
import time
import hmac
import hashlib
import random

# -------------------- UTILITIES -------------------- #
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# -------------------- PROVABLY FAIR CRASH -------------------- #
def generate_crash_point(server_seed: str, client_seed: str, nonce: int) -> float:
    message = f"{client_seed}-{nonce}".encode()
    hmac_hash = hmac.new(server_seed.encode(), message, hashlib.sha256).hexdigest()
    h = int(hmac_hash[:13], 16)
    e = (2 ** 52) / (h / (2 ** 52))
    if (h % 33) == 0:
        return 1.00
    crash = (100 * e) / (100 - 1)
    return round(max(1.00, crash / 100), 2)

# -------------------- BOT STRATEGY -------------------- #
def bot_strategy(balance):
    """
    Bot decides bet amount and target multiplier.
    You can customize strategy here.
    """
    bet = min(10, balance)       # bet $10 or whatever is left
    target = random.uniform(1.5, 3.5)  # cash out between 1.5x and 3.5x
    return bet, target

# -------------------- MAIN GAME LOOP -------------------- #
def aviator_bot_game(balance, server_seed, client_seed, nonce):
    bet, bot_target = bot_strategy(balance)
    balance -= bet
    crash_point = generate_crash_point(server_seed, client_seed, nonce)
    multiplier = 1.0
    growth_rate = 0.1
    cashed_out = False

    while multiplier < crash_point:
        multiplier += growth_rate + random.uniform(0.05, 0.12)
        growth_rate += 0.015
        time.sleep(0.05)  # fast simulation

        if multiplier >= bot_target:
            winnings = bet * multiplier
            balance += winnings
            cashed_out = True
            break

    if cashed_out:
        return balance, crash_point, multiplier, True
    else:
        return balance, crash_point, multiplier, False

# -------------------- SIMULATION MANAGER -------------------- #
def main():
    balance = 1000.0
    server_seed = "super_secret_server_seed_123"
    client_seed = "bot_demo_seed"
    nonce = 0
    history = []

    rounds_to_play = 50  # run 50 rounds automatically

    for _ in range(rounds_to_play):
        balance, crash_point, cashed_at, won = aviator_bot_game(balance, server_seed, client_seed, nonce)
        nonce += 1

        history.append({
            "round": nonce,
            "crash_point": crash_point,
            "cashed_at": round(cashed_at, 2),
            "result": "Win" if won else "Loss",
            "balance": round(balance, 2)
        })

    # -------------------- RESULTS -------------------- #
    clear()
    print("🤖 Bot Simulation Completed!\n")
    for h in history:
        color = "\033[92m" if h["result"] == "Win" else "\033[91m"
        print(f"Round {h['round']}: Crash @ {h['crash_point']}x → Cashed @ {h['cashed_at']}x → {color}{h['result']}\033[0m | Balance: ${h['balance']}")

    print(f"\n💰 Final Balance: ${balance:.2f}")
    wins = sum(1 for h in history if h["result"] == "Win")
    print(f"🏆 Total Wins: {wins} / {rounds_to_play}")
    print(f"💸 Total Losses: {rounds_to_play - wins}")

if __name__ == "__main__":
    main()
