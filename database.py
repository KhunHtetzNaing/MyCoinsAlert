import sqlite3
import logging
from datetime import datetime
from typing import List, Tuple, Optional
from os import path

class Database:
    def __init__(self, db_name: str = "alerts.db"):
        self.logger = logging.getLogger(__name__)
        # Get the directory where your bot code is located
        base_dir = path.dirname(path.abspath(__file__))
        # Construct the full path for the database file
        self.db_name = path.join(base_dir, db_name)
        self.setup_database()


    def setup_database(self):
        """Initialize database and create tables if they don't exist"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS alerts (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER,
                        coin TEXT,
                        target_price REAL,
                        is_greater_than BOOLEAN,
                        created_at TIMESTAMP,
                        UNIQUE(user_id, coin, target_price, is_greater_than)
                    )
                ''')
        except Exception as e:
            self.logger.error(f"Database setup error: {e}")
            raise

    def add_alert(self, user_id: int, coin: str, target_price: float, is_greater_than: bool) -> bool:
        """Add new alert to database"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute(
                    '''INSERT INTO alerts 
                       (user_id, coin, target_price, is_greater_than, created_at) 
                       VALUES (?, ?, ?, ?, ?)''',
                    (user_id, coin.lower(), target_price, is_greater_than, datetime.now())
                )
                return True
        except sqlite3.IntegrityError:
            # Alert already exists
            return False
        except Exception as e:
            self.logger.error(f"Error adding alert: {e}")
            return False

    def get_user_alerts(self, user_id: int) -> List[Tuple]:
        """Get all alerts for a specific user"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                return conn.execute(
                    '''SELECT id, coin, target_price, is_greater_than, created_at 
                       FROM alerts 
                       WHERE user_id = ? 
                       ORDER BY created_at''',
                    (user_id,)
                ).fetchall()
        except Exception as e:
            self.logger.error(f"Error getting user alerts: {e}")
            return []

    def remove_alert(self, alert_id: int, user_id: int) -> bool:
        """Remove specific alert for a user"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.execute(
                    'DELETE FROM alerts WHERE id = ? AND user_id = ?',
                    (alert_id, user_id)
                )
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Error removing alert: {e}")
            return False

    def remove_alert_by_index(self, user_id: int, index: int) -> Tuple[bool, Optional[str]]:
        """Remove alert by its index in user's alert list"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                alerts = conn.execute(
                    'SELECT id, coin FROM alerts WHERE user_id = ? ORDER BY created_at',
                    (user_id,)
                ).fetchall()

                if 0 <= index < len(alerts):
                    alert_id, coin = alerts[index]
                    conn.execute('DELETE FROM alerts WHERE id = ?', (alert_id,))
                    return True, coin
                return False, None
        except Exception as e:
            self.logger.error(f"Error removing alert by index: {e}")
            return False, None

    def remove_alert_by_coin(self, user_id: int, coin_id: str) -> bool:
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.execute("DELETE FROM alerts WHERE user_id = ? AND coin = ?", (user_id,coin_id,))
                return cursor.rowcount > 0
        except Exception as e:
            self.logger.error(f"Error removing triggered alert: {e}")
            return False

    def remove_alert_by_user(self, user_id: int) -> bool:
        """Remove alert after it's been triggered"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute('DELETE FROM alerts WHERE user_id = ?', (user_id,))
                return True
        except Exception as e:
            self.logger.error(f"Error removing triggered alert: {e}")
            return False

    def get_all_alerts(self) -> List[Tuple]:
        """Get all active alerts from all users"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                return conn.execute(
                    '''SELECT id, user_id, coin, target_price, is_greater_than 
                       FROM alerts'''
                ).fetchall()
        except Exception as e:
            self.logger.error(f"Error getting all alerts: {e}")
            return []

    def remove_triggered_alert(self, alert_id: int) -> bool:
        """Remove alert after it's been triggered"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                conn.execute('DELETE FROM alerts WHERE id = ?', (alert_id,))
                return True
        except Exception as e:
            self.logger.error(f"Error removing triggered alert: {e}")
            return False

    def get_unique_coins(self) -> List[str]:
        """Get list of unique coins from all alerts"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                return [row[0] for row in conn.execute(
                    'SELECT DISTINCT coin FROM alerts'
                ).fetchall()]
        except Exception as e:
            self.logger.error(f"Error getting unique coins: {e}")
            return []

    def get_alerts_count(self, user_id: int) -> int:
        """Get count of alerts for a user"""
        try:
            with sqlite3.connect(self.db_name) as conn:
                return conn.execute(
                    'SELECT COUNT(*) FROM alerts WHERE user_id = ?',
                    (user_id,)
                ).fetchone()[0]
        except Exception as e:
            self.logger.error(f"Error getting alerts count: {e}")
            return 0