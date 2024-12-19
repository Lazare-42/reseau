import json
import sys
from typing import Dict, List

import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class PortForwardingManager:
    def __init__(self):
        self.url = "http://192.168.1.1/ws"
        self.headers = {
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
            "Content-Type": "application/x-sah-ws-4-call+json",
            "Authorization": "X-Sah l0EJNIYvSRYvzV4wbww/ssW3amVNKDkK8Lys6ALKbtMtzCiCR6Y5eTpEYWmNHIYt",
            "X-Context": "l0EJNIYvSRYvzV4wbww/ssW3amVNKDkK8Lys6ALKbtMtzCiCR6Y5eTpEYWmNHIYt",
            "Cookie": "b9ebac9e/accept-language=en-US,en; UILang=fr; lastKnownIpv6TabState=visible; b9ebac9e/sessid=OJhRQs+kRygxitKwt2HlqEaX; sah/contextId=l0EJNIYvSRYvzV4wbww%2FssW3amVNKDkK8Lys6ALKbtMtzCiCR6Y5eTpEYWmNHIYt",
            "Origin": "http://192.168.1.1",
            "Referer": "http://192.168.1.1/",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
        }

    def clean_rule_id(self, rule_id: str) -> str:
        """Clean up rule ID by removing any control characters."""
        return rule_id.strip().replace("\t", "")

    def get_rules(self) -> List[Dict]:
        data = {
            "service": "Firewall",
            "method": "getPortForwarding",
            "parameters": {"origin": "webui"},
        }

        try:
            response = requests.post(self.url, headers=self.headers, json=data)
            cleaned_text = response.text.replace("\t", " ").strip()

            if cleaned_text:
                result = json.loads(cleaned_text)
                rules = []

                if isinstance(result.get("status"), dict):
                    for rule in result["status"].values():
                        # Clean up the rule ID
                        if "\t" in rule.get("Id", ""):
                            old_id = rule["Id"]
                            rule["Id"] = self.clean_rule_id(old_id)
                            print(f"\nFound rule with tab character: {old_id!r}")
                            print(f"Cleaning up to: {rule['Id']!r}")

                            # Try to update the rule
                            if self.update_rule(old_id, rule):
                                print("Successfully updated rule with clean ID")
                            else:
                                print("Failed to update rule with clean ID")

                        rules.append(rule)
                return rules

        except Exception as e:
            print(f"Error fetching rules: {str(e)}")
            import traceback

            traceback.print_exc()
            return []

    def update_rule(self, old_id: str, rule: Dict) -> bool:
        """Update an existing rule with cleaned data."""
        # First delete the old rule
        if not self.delete_rule(old_id):
            print(f"Failed to delete rule with ID: {old_id!r}")
            return False

        # Then add the new rule
        if not self.add_rule(rule):
            print(f"Failed to add cleaned rule: {rule['Id']!r}")
            return False

        print(f"Successfully replaced rule {old_id!r} with {rule['Id']!r}")
        return True

    def add_rule(self, rule_config: Dict) -> bool:
        data = {
            "service": "Firewall",
            "method": "addPortForwarding",
            "parameters": rule_config,
        }

        response = requests.post(
            self.url, headers=self.headers, json=data, verify=False
        )
        return response.status_code == 200

    def delete_rule(self, rule_id: str) -> bool:
        data = {
            "service": "Firewall",
            "method": "deletePortForwarding",
            "parameters": {"id": rule_id},
        }

        response = requests.post(
            self.url, headers=self.headers, json=data, verify=False
        )
        return response.status_code == 200

    def save_config(self, filename: str = "port_forwarding_config.json"):
        rules = self.get_rules()
        with open(filename, "w") as f:
            json.dump(rules, f, indent=2)
        print(f"Configuration saved to {filename}")

    def load_config(self, filename: str = "port_forwarding_config.json"):
        with open(filename) as f:
            rules = json.load(f)

        # First delete all existing rules
        current_rules = self.get_rules()
        for rule in current_rules:
            self.delete_rule(rule["id"])

        # Then add the new ones
        for rule in rules:
            self.add_rule(rule)

        print(f"Configuration loaded from {filename}")

    def print_rules(self):
        rules = self.get_rules()
        if not rules:
            print("\nNo port forwarding rules found.")
            return

        print("\nCurrent Port Forwarding Rules:")
        for rule in rules:
            print("-" * 80)
            print(f"ID: {rule.get('Id', 'N/A')}")
            print(f"Description: {rule.get('Description', 'N/A')}")
            print(f"External Port: {rule.get('ExternalPort', 'N/A')}")
            print(f"Internal Port: {rule.get('InternalPort', 'N/A')}")
            print(f"Destination IP: {rule.get('DestinationIPAddress', 'N/A')}")
            print(f"Protocol: {rule.get('Protocol', 'N/A')}")
            print(f"Enabled: {rule.get('Enable', False)}")


def main():
    manager = PortForwardingManager()

    if len(sys.argv) < 2:
        manager.print_rules()
        return

    command = sys.argv[1]

    if command == "save":
        manager.save_config()
    elif command == "load":
        manager.load_config()
    elif command == "list":
        manager.print_rules()
    else:
        print("Unknown command. Available commands: save, load, list")


if __name__ == "__main__":
    main()
