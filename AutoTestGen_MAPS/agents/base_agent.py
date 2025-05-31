from abc import ABC, abstractmethod
from typing import Dict, List, Any
import logging

class BaseAgent(ABC):
    """Base class for all requirement engineering agents"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        # Removed the direct call to setup_logging from base __init__.
        # Derived classes are now responsible for calling this after their own init.
        # self.setup_logging()

    def setup_logging(self):
        """Configure logging for the agent - default basic configuration"""
        # This basic config will be used if derived class doesn't override or calls super().setup_logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    @abstractmethod
    def process(self, input_data: Any) -> Dict[str, Any]:
        """Process input data and return results"""
        pass
    
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate input data"""
        pass
    
    def log_error(self, error: Exception, context: str = ""):
        """Log errors with context"""
        self.logger.error(f"{context}: {str(error)}")
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value with default fallback"""
        return self.config.get(key, default)
    
    def update_config(self, key: str, value: Any):
        """Update configuration value"""
        self.config[key] = value

    def setup_logging(self):
        """Configure logging for the agent - default basic configuration"""
        # This basic config will be used if derived class doesn't override or calls super().setup_logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ) 