"""Role-Based Access Control (RBAC) Engine for Autonomous AI Agents."""
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

# IAM Role Definitions & Allowed Tooling
AGENT_ROLES = {
    "customer_support_agent": {
        "allowed_tools": ["search_knowledge_base", "get_order_status"]
    },
    "financial_analyst_agent": {
        "allowed_tools": ["search_knowledge_base", "query_revenue_db", "generate_report"]
    },
    "sysadmin_agent": {
        "allowed_tools": ["search_knowledge_base", "query_revenue_db", "execute_sql_query", "restart_service"]
    }
}

class RBACEngine:
    """Evaluates if an AI agent is cryptographically/role-authorized to invoke a tool."""
    
    @staticmethod
    def is_authorized(agent_role: str, tool_name: str) -> bool:
        role_config = AGENT_ROLES.get(agent_role)
        
        if not role_config:
            logging.error(f"RBAC Deny: Role '{agent_role}' is undefined in IAM policy.")
            return False
            
        if tool_name not in role_config.get("allowed_tools", []):
            logging.warning(f"RBAC Deny: Agent role '{agent_role}' unauthorized for tool '{tool_name}'.")
            return False
            
        return True
