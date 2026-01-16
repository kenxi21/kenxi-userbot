import sqlite3
import os
from datetime import datetime

class LogDatabase:
    def __init__(self, db_path="database/logs.db"):
        self.db_path = db_path
        os.makedirs("database", exist_ok=True)
        self.init_tables()
    
    def init_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS join_leave_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                user_name TEXT,
                user_username TEXT,
                chat_id INTEGER,
                chat_name TEXT,
                chat_username TEXT,
                type TEXT,
                is_self BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mention_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER,
                from_user_name TEXT,
                chat_id INTEGER,
                chat_name TEXT,
                message_text TEXT,
                message_link TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS private_message_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER,
                from_user_name TEXT,
                message_text TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_join_log(self, user_id, user_name, user_username, chat_id, chat_name, chat_username, is_self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO join_leave_logs (user_id, user_name, user_username, chat_id, chat_name, chat_username, type, is_self)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, user_name, user_username, chat_id, chat_name, chat_username, "join", is_self))
        conn.commit()
        conn.close()
    
    def add_leave_log(self, user_id, user_name, user_username, chat_id, chat_name, chat_username, is_self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO join_leave_logs (user_id, user_name, user_username, chat_id, chat_name, chat_username, type, is_self)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, user_name, user_username, chat_id, chat_name, chat_username, "leave", is_self))
        conn.commit()
        conn.close()
    
    def add_mention_log(self, from_user_id, from_user_name, chat_id, chat_name, message_text, message_link):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO mention_logs (from_user_id, from_user_name, chat_id, chat_name, message_text, message_link)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (from_user_id, from_user_name, chat_id, chat_name, message_text, message_link))
        conn.commit()
        conn.close()
    
    def add_private_message_log(self, from_user_id, from_user_name, message_text):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO private_message_logs (from_user_id, from_user_name, message_text)
            VALUES (?, ?, ?)
        """, (from_user_id, from_user_name, message_text))
        conn.commit()
        conn.close()
    
    def get_join_leave_logs(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_name, chat_name, type, is_self, timestamp FROM join_leave_logs
            ORDER BY id DESC LIMIT ?
        """, (limit,))
        logs = cursor.fetchall()
        conn.close()
        
        return [{"user_name": log[0], "chat_name": log[1], "type": log[2], "is_self": log[3], "timestamp": log[4]} for log in logs]
    
    def get_mention_logs(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT from_user_name, chat_name, message_text, timestamp FROM mention_logs
            ORDER BY id DESC LIMIT ?
        """, (limit,))
        logs = cursor.fetchall()
        conn.close()
        
        return [{"from_user_name": log[0], "chat_name": log[1], "message_text": log[2], "timestamp": log[3]} for log in logs]
    
    def get_private_message_logs(self, limit=10):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT from_user_name, message_text, timestamp FROM private_message_logs
            ORDER BY id DESC LIMIT ?
        """, (limit,))
        logs = cursor.fetchall()
        conn.close()
        
        return [{"from_user_name": log[0], "message_text": log[1], "timestamp": log[2]} for log in logs]
    
    def get_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM join_leave_logs WHERE type='join'")
        joins = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM join_leave_logs WHERE type='leave'")
        leaves = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM mention_logs")
        mentions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM private_message_logs")
        pms = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_joins": joins,
            "total_leaves": leaves,
            "total_mentions": mentions,
            "total_private_messages": pms
        }
    
    def clear_all_logs(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM join_leave_logs")
        cursor.execute("DELETE FROM mention_logs")
        cursor.execute("DELETE FROM private_message_logs")
        conn.commit()
        conn.close()