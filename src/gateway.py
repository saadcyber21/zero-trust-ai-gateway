"""Core Zero-Trust Proxy Gateway for AI Agent Orchestration."""
import json
import logging
from typing import Dict, Any

from rbac_engine import RBACEngine
from payload_inspector import PayloadInspector

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(levelname)s] - %(message)s")

class ZeroTrustAgentGateway:
    """Intercepts and evaluates AI agent tool calls prior to API/DB execution."""
    
    def __init__(self):
        self.rbac = RBACEngine()
        self.inspector = PayloadInspector()

    def invoke_tool(self, agent_role: str, tool_name: str, tool_arguments: str) -> Dict[str, Any]:
        """Enforces Zero-Trust Principles: Never Trust, Always Verify."""
        logging.info(f"Intercepted Action: Agent[{agent_role}] -> Tool[{tool_name}]")
        
        # Step 1: Identity & Access Policy Check
        if not self.rbac.is_authorized(agent_role, tool_name):
            return {
                "status": "blocked",
                "reason": "RBAC Policy Violation: Tool execution unauthorized for role.",
                "http_code": 403
            }

        # Step 2: Deep Packet Payload Inspection
        if not self.inspector.inspect(tool_arguments):
            return {
                "status": "blocked",
                "reason": "Security Alert: Malicious payload or destructive command detected.",
                "http_code": 406
            }

        # Step 3: Authorization Granted
        logging.info(f"Execution Approved: Agent[{agent_role}] -> Tool[{tool_name}]")
        return {
            "status": "success",
            "message": f"Tool '{tool_name}' executed safely.",
            "http_code": 200
        }

if __name__ == "__main__":
    gateway = ZeroTrustAgentGateway()
    
    print("\n" + "="*50)
    print("DEMO 1: Authorized Benign Tool Call")
    print("="*50)
    res1 = gateway.invoke_tool("customer_support_agent", "get_order_status", "order_id=98765")
    print(json.dumps(res1, indent=2))
    
    print("\n" + "="*50)
    print("DEMO 2: RBAC Access Control Block")
    print("="*50)
    res2 = gateway.invoke_tool("customer_support_agent", "execute_sql_query", "SELECT * FROM users")
    print(json.dumps(res2, indent=2))
    
    print("\n" + "="*50)
    print("DEMO 3: Destructive Payload Interception")
    print("="*50)
    res3 = gateway.invoke_tool("sysadmin_agent", "execute_sql_query", "DROP TABLE customer_records;")
    print(json.dumps(res3, indent=2))
