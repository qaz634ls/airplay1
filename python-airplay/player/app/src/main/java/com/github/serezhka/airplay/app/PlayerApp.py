"""
Python rewrite of:
  java-airplay/player/app/src/main/java/com/github/serezhka/airplay/app/PlayerApp.java

Main entry point of the application, comparable to the Spring Boot application class.
"""

import logging
import signal
import sys
import time
from typing import Dict, Any

from .config.PlayerConfig import PlayerConfig

# Setup basic logging similar to @Slf4j
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
log = logging.getLogger(__name__)


class PlayerApp:
    """
    Encapsulates the application lifecycle, taking the place of the Spring context.
    """

    def __init__(self, air_play_server):
        self._air_play_server = air_play_server

    def post_construct(self) -> None:
        """
        Equivalent to @PostConstruct in Java.
        Starts the AirPlay server when the application is fully loaded.
        """
        try:
            log.info("Starting AirPlay Server...")
            self._air_play_server.start()
        except Exception as e:
            log.error("Failed to start AirPlay Server: %s", e)
            raise

    def pre_destroy(self) -> None:
        """
        Equivalent to @PreDestroy in Java.
        Gracefully stops the AirPlay server before the application exits.
        """
        log.info("Stopping AirPlay Server...")
        self._air_play_server.stop()



def _load_properties() -> Dict[str, Any]:
    """Reads simple properties from application.properties"""
    properties: Dict[str, Any] = {
        "airplay": {}
    }
    
    import os
    props_path = os.path.join(os.path.dirname(__file__), '../../../resources/application.properties')
    try:
        with open(props_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    k, v = k.strip(), v.strip()
                    if v.lower() == 'true': v = True
                    elif v.lower() == 'false': v = False
                    elif v.isdigit(): v = int(v)
                    properties[k] = v
                    if k.startswith('airplay.'):
                        properties['airplay'][k.split('.', 1)[1]] = v
    except FileNotFoundError:
        log.warning("application.properties not found at %s. Using default settings.", props_path)
    
    return properties


def main():
    """
    Main entry point of the Python application.
    Replaces the SpringApplicationBuilder execution.
    """
    properties = _load_properties()

    # 1. Initialize configuration and wire dependencies (Spring Boot replacement)
    config = PlayerConfig(properties)
    air_play_server = config.build_server()

    # 2. Initialize application wrapper
    app = PlayerApp(air_play_server)

    # 3. Register graceful shutdown hooks (replaces Spring's JVM shutdown hooks)
    def signal_handler(sig, frame):
        log.info("Received interrupt signal. Initiating shutdown...")
        app.pre_destroy()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 4. Start the application lifecycle
    try:
        app.post_construct()
        log.info("AirPlay Player App is running. Press Ctrl+C to exit.")
        
        # Spring Boot web(WebApplicationType.NONE) mode typically keeps 
        # the main thread alive if there are running non-daemon threads.
        # We simulate this behavior here.
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log.exception("Application encountered a fatal error: %s", e)
    finally:
        app.pre_destroy()


if __name__ == '__main__':
    main()
