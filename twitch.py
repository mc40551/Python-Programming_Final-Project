import os

# checks and stores Twitch ID's
DATA_DIR = './data'
TWITCH_FILE = os.path.join(DATA_DIR, 'twitch_streams.txt')
os.makedirs(DATA_DIR, exist_ok=True)

def load_streams():
    # loads stored Twitch ID's
    if not os.path.exists(TWITCH_FILE):
        return []
    with open(TWITCH_FILE, 'r') as f:
        return [line.strip() for line in f.readlines()]

def save_streams(streams):
    # stores Twitch ID's
    with open(TWITCH_FILE, 'w') as f:
        f.writelines(f"{stream}\n" for stream in streams)

def add_stream(stream):
    # adds ID to the list if it does not exist
    streams = load_streams()
    if stream not in streams:
        streams.append(stream)
        save_streams(streams)
        return True
    return False

def delete_stream(stream):
    # deletes the ID from the list
    streams = load_streams()
    if stream in streams:
        streams.remove(stream)
        save_streams(streams)
        return True
    return False
