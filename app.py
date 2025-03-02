import streamlit as st
import datetime
import json
import os

# File to store notes
NOTES_FILE = "notes.json"

# Ensure the notes file exists
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, "w") as f:
        json.dump({}, f)

st.title("Note Taking App")
note_text = st.text_area("Enter your note:")

def delete_json_item(filepath, key_to_delete):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)

        if key_to_delete in data:
            del data[key_to_delete]
            with open(filepath, "w") as f:
                json.dump(data, f, indent=4)
            return True
        else:
            return False

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error: {e}")
        return False

# Load notes from file
def load_notes():
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save notes to file
def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f)

# Initialize notes
if "notes" not in st.session_state:
    st.session_state.notes = load_notes()

if st.session_state.notes:
    st.subheader("Your Notes:")
    for timestamp, note in st.session_state.notes.items():
        st.write(f"**{timestamp}:**")  # Display timestamp in bold
        st.write(note)

        # Button to delete note
        if st.button(f"Delete note from {timestamp}"):  # More specific button label
            del st.session_state.notes[timestamp]
            delete_json_item(NOTES_FILE, timestamp)
            st.rerun()  # Refresh the app to reflect the deletion

# Optional: Clear all notes button
if st.button("Clear All Notes"):
    st.session_state.notes = {}
    with open(NOTES_FILE, "w") as f:
        json.dump({}, f)
    st.rerun()  # Refresh after clearing

# Save notes on changes
def save_on_change():
    save_notes(st.session_state.notes)

# Add note button
if st.button("Add Note"):
    if note_text:  # Check if the note text is not empty
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.notes[timestamp] = note_text
        st.success("Note added!")  # Display a success message
        
    else:
        st.warning("Please enter some text for your note.")  # Display a warning if the note is empty
    save_on_change()
    st.rerun()

# Optional: Save notes on shutdown (requires Streamlit 1.12.0+)
try:  # Use a try block to avoid errors if on_shutdown isn't available
    def on_shutdown():
        save_notes(st.session_state.notes)

    st.session_state.on_shutdown = on_shutdown
except AttributeError:  # Handle AttributeError if using older Streamlit
    raise "upgrade streamlit to version 1.12.0+"  # Or add a warning to upgrade Streamlit
