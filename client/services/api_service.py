import requests
from typing import Dict, Any, Optional
from config.settings import BASE_URL, DEFAULT_TIMEOUT


class ApiService:
    """Centralized service for handling HTTP API requests with authentication."""
    
    def __init__(self, token: Optional[str] = None):
        self.base_url = BASE_URL
        self.headers = {"Authorization": f"Bearer {token}"} if token else {}
        self.timeout = DEFAULT_TIMEOUT
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute GET request to the API."""
        return self._make_request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
             params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute POST request to the API."""
        return self._make_request("POST", endpoint, data=data, params=params)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute PUT request to the API."""
        return self._make_request("PUT", endpoint, data=data)
    
    def delete(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute DELETE request to the API."""
        return self._make_request("DELETE", endpoint, data=data)
    
    def update_token(self, token: str) -> None:
        """Update the authentication token in headers."""
        self.headers["Authorization"] = f"Bearer {token}"
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None,
                     params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute HTTP request with proper error handling."""
        try:
            url = f"{self.base_url}{endpoint}"
            kwargs = {
                "headers": self.headers,
                "timeout": self.timeout
            }
            
            if params:
                kwargs["params"] = params
            if data:
                kwargs["json"] = data
            
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            status_code = getattr(e.response, 'status_code', None)
            return {"error": str(e), "status_code": status_code} 