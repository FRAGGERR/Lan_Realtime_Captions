# Rolling 5-minute caption buffer

import datetime
from collections import deque
from typing import Dict, List

class CaptionBuffer:
    def __init__(self, duration_seconds: int = 300):
        """
        Initialize a rolling buffer.

        Args:
            duration_seconds (int): How many seconds of history to keep (default 5 minutes = 300 seconds)
        """
        self.buffer: deque = deque()
        self.duration_seconds = duration_seconds

    def add_caption(self, caption_entry: Dict):
        """
        Add a new caption to the buffer and clean up old ones.
        
        Args:
            caption_entry (dict): Example → {"timestamp": "2025-06-27 20:15:03", "text": "Hello world"}
        """
        self.buffer.append(caption_entry)
        self._cleanup_old_entries()

    def get_captions(self) -> List[Dict]:
        """
        Get the current list of buffered captions.

        Returns:
            List[Dict]: All caption entries within buffer window
        """
        return list(self.buffer)

    def _cleanup_old_entries(self):
        """
        Remove any captions older than the desired buffer window.
        """
        now = datetime.datetime.now()

        while self.buffer:
            oldest = self.buffer[0]
            try:
                entry_time = datetime.datetime.strptime(oldest["timestamp"], "%Y-%m-%d %H:%M:%S")
                age_seconds = (now - entry_time).total_seconds()

                if age_seconds > self.duration_seconds:
                    self.buffer.popleft()
                else:
                    break  # Oldest entry still within time window → stop cleanup

            except Exception as e:
                print(f"Buffer cleanup error: {e}")
                self.buffer.popleft()  # Remove problematic entry

        def clear(self):
            """Clear all captions from the buffer"""
            self.buffer.clear()


# changed form here -->             
#         # If the buffer is empty, we can just return
        if not self.buffer:
            return  