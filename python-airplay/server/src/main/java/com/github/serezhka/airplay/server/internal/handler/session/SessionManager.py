"""
Python rewrite of:
  java-airplay/server/src/main/java/com/github/serezhka/airplay/server/internal/handler/session/SessionManager.java
"""

import threading
from typing import Dict

from .....server.AirPlayConsumerFactory import AirPlayConsumerFactory
from .Session import Session


class SessionManager:
    """
    Manages active AirPlay sessions.
    """

    def __init__(self, consumer_factory: AirPlayConsumerFactory):
        self._consumer_factory = consumer_factory
        self._sessions: Dict[str, Session] = {}
        self._lock = threading.Lock()

    def get_session(self, session_id: str) -> Session:
        with self._lock:
            if session_id not in self._sessions:
                consumer = self._consumer_factory.create(session_id)
                self._sessions[session_id] = Session(session_id, consumer)
            return self._sessions[session_id]

    def remove_session(self, session_id: str) -> None:
        with self._lock:
            if session_id in self._sessions:
                del self._sessions[session_id]
        
        # Assume consumer_factory.destroy exists as in Java
        self._consumer_factory.destroy(session_id)
