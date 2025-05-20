import time
import os

DETECTED_FILE = "detected_tags.txt"
INJECT_FILE = "inject_tags.txt"
SEEN_TAGS_FILE = "seen_tags.txt"

def load_seen_tags():
    if not os.path.exists(SEEN_TAGS_FILE):
        return set()
    with open(SEEN_TAGS_FILE, 'r') as f:
        return set(line.strip() for line in f.readlines())

def save_seen_tag(tag):
    with open(SEEN_TAGS_FILE, 'a') as f:
        f.write(tag + '\n')

def append_to_inject(tag):
    with open(INJECT_FILE, 'a') as f:
        f.write(tag + '\n')

def is_valid_exec_tag(tag):
    return tag.startswith("!exec:") and tag.endswith("!")

def watch_for_new_tags():
    print("[Listener] Watching for new tags...")
    seen_tags = load_seen_tags()

    while True:
        if not os.path.exists(DETECTED_FILE):
            time.sleep(1)
            continue

        with open(DETECTED_FILE, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        print(f"[Listener] Contents of detected_tags.txt: {lines}")

        for tag in lines:
            if is_valid_exec_tag(tag) and tag not in seen_tags:
                print(f"[Listener] New exec tag detected: {tag}")
                append_to_inject(tag)
                save_seen_tag(tag)
                seen_tags.add(tag)

        time.sleep(1)

if __name__ == "__main__":
    watch_for_new_tags()
