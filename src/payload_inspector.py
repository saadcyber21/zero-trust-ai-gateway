"""Deep Packet Inspection for AI Agent Tool Call Arguments."""
import re
import logging

class PayloadInspector:
    """Scans tool execution parameters for injection attacks, shell drops, and destructive SQL."""
    
    DANGEROUS_PATTERNS = [
        r"(?i)drop\s+table",        # SQL Drop Table
        r"(?i)delete\s+from",       # SQL Delete
        r"rm\s+-rf",                # Linux destructive remove
        r"(?i)chmod\s+777",         # Dangerous permission escalation
        r"(?i)nc\s+-e",             # Netcat reverse shell
        r";\s*ls",                  # Command chaining
        r"(?i)union\s+select",      # SQL Union Injection
    ]

    @staticmethod
    def inspect(payload: str) -> bool:
        """Returns True if payload is clean; False if malicious signature is detected."""
        if not payload:
            return True
            
        for pattern in PayloadInspector.DANGEROUS_PATTERNS:
            if re.search(pattern, str(payload)):
                logging.warning(f"Security Alert: Malicious payload signature matched -> {pattern}")
                return False
                
        return True
