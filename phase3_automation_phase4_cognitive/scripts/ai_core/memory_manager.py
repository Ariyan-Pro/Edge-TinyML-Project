#!/usr/bin/env python3
"""
PHASE 4: MEMORY MANAGER
SQLite database for cognitive memory and command logging
"""

import sqlite3
import json
import time
from pathlib import Path

# Database path
DB_PATH = Path(__file__).resolve().parent.parent / "db" / "cognitive_memory.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class MemoryManager:
    def __init__(self):
        self.init_db()
        print("🗃️ MEMORY MANAGER INITIALIZED")
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Memory table for general cognitive memory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                memory_type TEXT NOT NULL,
                content TEXT NOT NULL,
                vector_id INTEGER
            )
        """)
        
        # Conversations table for dialog history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                timestamp INTEGER NOT NULL,
                user_text TEXT NOT NULL,
                assistant_text TEXT NOT NULL
            )
        """)
        
        # Commands log table for command execution history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS commands_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                command_text TEXT NOT NULL,
                confidence REAL,
                executed INTEGER DEFAULT 0
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database tables initialized")
    
    def store_memory(self, memory_type, content):
        """Store a memory entry"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO memory (timestamp, memory_type, content) VALUES (?, ?, ?)",
            (int(time.time()), memory_type, json.dumps(content))
        )
        
        conn.commit()
        conn.close()
        print(f"💾 Stored memory: {memory_type}")
    
    def log_conversation(self, session_id, user_text, assistant_text):
        """Log a conversation exchange"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO conversations (session_id, timestamp, user_text, assistant_text) VALUES (?, ?, ?, ?)",
            (session_id, int(time.time()), user_text, assistant_text)
        )
        
        conn.commit()
        conn.close()
        print(f"💬 Logged conversation: {user_text[:50]}...")
    
    def log_command(self, command_text, confidence=1.0, executed=True):
        """Log command execution"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO commands_log (timestamp, command_text, confidence, executed) VALUES (?, ?, ?, ?)",
            (int(time.time()), command_text, confidence, int(executed))
        )
        
        conn.commit()
        conn.close()
        print(f"📝 Logged command: {command_text}")
    
    def get_recent_memories(self, limit=10):
        """Get recent memories"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT timestamp, memory_type, content FROM memory ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                'timestamp': row[0],
                'type': row[1],
                'content': json.loads(row[2])
            })
        
        conn.close()
        return memories
    
    def get_command_history(self, limit=20):
        """Get command execution history"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT timestamp, command_text, confidence, executed FROM commands_log ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        )
        
        commands = []
        for row in cursor.fetchall():
            commands.append({
                'timestamp': row[0],
                'command': row[1],
                'confidence': row[2],
                'executed': bool(row[3])
            })
        
        conn.close()
        return commands

def main():
    """Test the memory manager"""
    memory = MemoryManager()
    
    # Test data
    memory.store_memory("user_preference", {"likes_coffee": True, "preferred_voice": "female"})
    memory.log_conversation("test_session", "Hello there", "Hi! How can I help you?")
    memory.log_command("open browser", 0.95, True)
    
    # Display recent data
    print("\n📊 RECENT MEMORIES:")
    for mem in memory.get_recent_memories(5):
        print(f"   - {mem['type']}: {mem['content']}")
    
    print("\n📋 COMMAND HISTORY:")
    for cmd in memory.get_command_history(5):
        status = "✅" if cmd['executed'] else "❌"
        print(f"   {status} {cmd['command']} (conf: {cmd['confidence']})")

if __name__ == "__main__":
    main()
