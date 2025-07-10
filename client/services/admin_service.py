from typing import Dict, Any, List
from services.api_service import ApiService


class AdminService:
    """Service for handling administrative operations."""
    
    def __init__(self, token: str):
        self.api_service = ApiService(token)
    
    def get_servers_status(self) -> Dict[str, Any]:
        """Retrieve status of external news API servers."""
        return self.api_service.get("/admin/servers")
    
    def get_server_details(self) -> Dict[str, Any]:
        """Retrieve detailed information about external servers."""
        return self.api_service.get("/admin/server-details")
    
    def update_server_api(self, server_id: str, api_key: str) -> Dict[str, Any]:
        """Update API key for a specific server."""
        data = {"api_key": api_key}
        result = self.api_service.put(f"/admin/update-server/{server_id}", data)
        
        if "error" not in result:
            success = result.get("success", True)
            return {"success": success}
        
        return result
    
    def get_categories(self) -> Dict[str, Any]:
        """Retrieve all available article categories."""
        return self.api_service.get("/admin/categories")
    
    def add_category(self, name: str) -> Dict[str, Any]:
        """Add a new article category."""
        data = {"name": name}
        return self.api_service.post("/admin/add-category", data)
    
    def trigger_manual_fetch(self) -> Dict[str, Any]:
        """Manually trigger news fetching and processing."""
        return self.api_service.post("/admin/trigger-fetch", {})
    
    def trigger_manual_notifications(self) -> Dict[str, Any]:
        """Manually trigger notification processing."""
        return self.api_service.post("/admin/trigger-notifications", {})
    
    def get_scheduler_status(self) -> Dict[str, Any]:
        """Get current scheduler status."""
        return self.api_service.get("/admin/scheduler-status") 