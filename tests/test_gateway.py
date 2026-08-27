"""Automated Test Suite for Zero-Trust AI Gateway."""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from gateway import ZeroTrustAgentGateway

def test_authorized_tool_execution():
    gateway = ZeroTrustAgentGateway()
    res = gateway.invoke_tool("financial_analyst_agent", "query_revenue_db", "Q3 2026")
    assert res["status"] == "success"
    assert res["http_code"] == 200

def test_rbac_unauthorized_tool():
    gateway = ZeroTrustAgentGateway()
    # Support agent trying to run SQL query
    res = gateway.invoke_tool("customer_support_agent", "execute_sql_query", "SELECT * FROM customers")
    assert res["status"] == "blocked"
    assert res["http_code"] == 403

def test_malicious_sql_payload():
    gateway = ZeroTrustAgentGateway()
    # Sysadmin is authorized to run SQL, but payload inspector blocks DROP TABLE
    res = gateway.invoke_tool("sysadmin_agent", "execute_sql_query", "DROP TABLE users;")
    assert res["status"] == "blocked"
    assert res["http_code"] == 406

def test_command_injection_payload():
    gateway = ZeroTrustAgentGateway()
    res = gateway.invoke_tool("sysadmin_agent", "restart_service", "nginx; rm -rf /")
    assert res["status"] == "blocked"
    assert res["http_code"] == 406
