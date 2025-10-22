"""
API extractor for fetching data from REST APIs.
"""
import pandas as pd
import requests
from typing import Dict, Optional, Any
import json
from datetime import datetime

from .base_extractor import BaseExtractor
from ..utils.logging import logger


class APIExtractor(BaseExtractor):
    """
    Generic API extractor for REST APIs.
    
    This extractor can fetch data from any REST API endpoint and convert
    the response to a pandas DataFrame.
    """
    
    def __init__(self, url: str, headers: Optional[Dict] = None, 
                 params: Optional[Dict] = None, config: Optional[Dict] = None):
        """
        Initialize the API extractor.
        
        Args:
            url: API endpoint URL
            headers: Optional HTTP headers
            params: Optional query parameters
            config: Optional configuration dictionary
        """
        super().__init__("api_extractor", config)
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.timeout = self.config.get("timeout", 30)
        self.retries = self.config.get("retries", 3)
    
    def extract(self) -> pd.DataFrame:
        """
        Extract data from the API endpoint.
        
        Returns:
            DataFrame containing the API response data
        """
        logger.info(f"Extracting data from API: {self.url}")
        
        try:
            # Make API request
            response = requests.get(
                self.url,
                headers=self.headers,
                params=self.params,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            # Parse response
            data = self._parse_response(response)
            
            # Convert to DataFrame
            df = self._convert_to_dataframe(data)
            
            logger.info(f"Successfully extracted {len(df)} records from API")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Data extraction failed: {e}")
            raise
    
    def _parse_response(self, response: requests.Response) -> Any:
        """
        Parse the API response.
        
        Args:
            response: The API response object
            
        Returns:
            Parsed data from the response
        """
        content_type = response.headers.get('content-type', '').lower()
        
        if 'application/json' in content_type:
            return response.json()
        elif 'text/csv' in content_type:
            return response.text
        elif 'text/plain' in content_type:
            return response.text
        else:
            # Try to parse as JSON by default
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.text
    
    def _convert_to_dataframe(self, data: Any) -> pd.DataFrame:
        """
        Convert parsed data to DataFrame.
        
        Args:
            data: Parsed data from API response
            
        Returns:
            DataFrame containing the data
        """
        if isinstance(data, list):
            # List of dictionaries
            if data and isinstance(data[0], dict):
                return pd.DataFrame(data)
            else:
                # List of values
                return pd.DataFrame(data, columns=['value'])
        
        elif isinstance(data, dict):
            # Single dictionary
            if 'data' in data and isinstance(data['data'], list):
                # Common API pattern: {"data": [...]}
                return pd.DataFrame(data['data'])
            elif 'results' in data and isinstance(data['results'], list):
                # Common API pattern: {"results": [...]}
                return pd.DataFrame(data['results'])
            else:
                # Flatten dictionary
                return pd.DataFrame([data])
        
        elif isinstance(data, str):
            # String data (CSV, etc.)
            if data.strip().startswith('{') or data.strip().startswith('['):
                # JSON string
                json_data = json.loads(data)
                return self._convert_to_dataframe(json_data)
            else:
                # CSV string
                from io import StringIO
                return pd.read_csv(StringIO(data))
        
        else:
            # Unknown format, create single-row DataFrame
            return pd.DataFrame([{"value": data}])
    
    def validate(self, data: pd.DataFrame) -> bool:
        """
        Validate the extracted data.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        if data.empty:
            logger.warning("API returned empty data")
            return False
        
        # Check for required columns if specified
        required_columns = self.config.get("required_columns", [])
        if required_columns:
            missing_columns = set(required_columns) - set(data.columns)
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                return False
        
        # Check data quality
        null_percentage = data.isnull().sum().sum() / (len(data) * len(data.columns))
        if null_percentage > 0.5:  # More than 50% null values
            logger.warning(f"High percentage of null values: {null_percentage:.2%}")
        
        logger.info(f"Data validation passed: {len(data)} records, {len(data.columns)} columns")
        return True
    
    def test_connection(self) -> bool:
        """
        Test the API connection.
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                params=self.params,
                timeout=self.timeout
            )
            response.raise_for_status()
            logger.info(f"API connection test successful: {self.url}")
            return True
            
        except Exception as e:
            logger.error(f"API connection test failed: {e}")
            return False
