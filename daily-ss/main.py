import os
import random
import datetime
import sqlite3

# Paths (wiki 7フォルダ構成 2026-08-05)
WIKI_JOURNAL = "wiki/journal"
WIKI_NOVEL = "wiki/creative/novel"
WIKI_IDEAS = "wiki/journal/ideas"
DB_PATH = "wiki/db/ss_data.db"

def get_random_md_file(folder):
    """Return the full path of a random .md file from the given folder."""
    try:
        files = [f for f in os.listdir(folder) if f.lower().endswith(".md")]
        if not files:
            raise FileNotFoundError(f"No .md files in {folder}")
        chosen = random.choice(files)
        return os.path.join(folder, chosen)
    except Exception as e:
        raise RuntimeError(f"Error picking random file from {folder}: {e}")

def read_head_500(filepath):
    """Read the first 500 characters from a file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()[:500]

def load_prompts():
    """Load prompt templates from references/prompts/ directory."""
    prompts_dir = os.path.join(os.path.dirname(__file__), "references", "prompts")
    prompt_files = [f for f in os.listdir(prompts_dir) if f.endswith(".txt")]
    prompts = {}
    for fname in prompt_files:
        with open(os.path.join(prompts_dir, fname), "r", encoding="utf-8") as f:
            prompts[fname] = f.read().strip()
    return prompts

def generate_story(prompt_template, source_snippet, max_chars=500):
    """
    Generate a short story using a prompt template and source snippet.
    The result is truncated to max_chars characters.
    """
    # Simple style instruction
    style_instruction = "Write a 星新一風ショートショート in under 500 characters, surprising and concise."
    # Build the full prompt
    full_prompt = f"{style_instruction}\nPrompt template:\n{prompt_template}\nSource material:\n{source_snippet}"
    # Very naive generation: repeat a base sentence until length reached
    base_sentence = "One unexpected evening, a door appeared, and everything changed."
    story = ""
    while len(story) < max_chars:
        story += base_sentence
    return story[:max_chars]

def ensure_db(db_path):
    """Create the stories table if it does not exist."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_story(db_path, title, content):
    """Insert a story into the database."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("INSERT INTO stories (title, content, created_at) VALUES (?, ?, ?)", 
                (title, content, datetime.datetime.now().isoformat()))
    conn.commit()
    conn.close()

def main():
    # 1. Acquire random source snippets (one from each folder)
    snippets = []
    for folder in [WIKI_JOURNAL, WIKI_NOVEL, WIKI_IDEAS]:
        src_path = get_random_md_file(folder)
        snippet = read_head_500(src_path)
        snippets.append(snippet)

    # 2. Load prompt templates
    prompts = load_prompts()
    # Assuming we have at least three prompt files; take the first three
    prompt_keys = list(prompts.keys())[:3]

    # 3. Generate three stories
    stories = []
    today_str = datetime.datetime.now().strftime("%Y%m%d")
    for i, (prompt_key) in enumerate(prompt_keys, start=1):
        title = f"{today_str}_Story_{i}"
        prompt_template = prompts[prompt_key]
        story = generate_story(prompt_template, snippets[i-1])
        stories.append((title, story))

    # 4. Ensure DB exists and insert stories
    ensure_db(DB_PATH)
    for title, content in stories:
        insert_story(DB_PATH, title, content)
        print(f"Saved: {title} ({len(content)} chars)")

if __name__ == "__main__":
    main()