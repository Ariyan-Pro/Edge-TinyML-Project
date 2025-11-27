"""
Notes Tool Plugin
Manage personal notes and reminders
"""

__description__ = "Take and manage personal notes and reminders"
__safety_level__ = "safe"
__version__ = "1.0"
__author__ = "System"

import json
import os
from datetime import datetime

class NotesTool:
    def __init__(self, storage_file="notes.json"):
        self.storage_file = storage_file
        self.notes = self._load_notes()
    
    def _load_notes(self) -> list:
        """Load notes from storage"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []
    
    def _save_notes(self):
        """Save notes to storage"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.notes, f, indent=2)
            return True
        except:
            return False
    
    def add_note(self, content: str, category: str = "general") -> dict:
        """Add a new note"""
        note = {
            "id": len(self.notes) + 1,
            "content": content,
            "category": category,
            "created": datetime.now().isoformat(),
            "completed": False
        }
        self.notes.append(note)
        success = self._save_notes()
        return {"success": success, "note": note}
    
    def list_notes(self, category: str = None) -> dict:
        """List all notes, optionally filtered by category"""
        if category:
            filtered = [note for note in self.notes if note["category"] == category]
            return {"success": True, "notes": filtered}
        return {"success": True, "notes": self.notes}
    
    def delete_note(self, note_id: int) -> dict:
        """Delete a note by ID"""
        initial_count = len(self.notes)
        self.notes = [note for note in self.notes if note["id"] != note_id]
        
        if len(self.notes) < initial_count:
            success = self._save_notes()
            return {"success": success, "deleted": True}
        return {"success": False, "error": "Note not found"}

# Plugin interface function
def execute(command: str, parameters: dict) -> dict:
    """Main plugin execution function"""
    tool = NotesTool()
    
    if command == "add_note":
        return tool.add_note(
            parameters.get("content", ""),
            parameters.get("category", "general")
        )
    elif command == "list_notes":
        return tool.list_notes(parameters.get("category"))
    elif command == "delete_note":
        return tool.delete_note(parameters.get("note_id"))
    else:
        return {"success": False, "error": f"Unknown command: {command}"}
