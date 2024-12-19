import json

import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def fetch_devices():
    url = "http://192.168.1.1/ws"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-sah-ws-4-call+json",
        "Authorization": "X-Sah lnWxt67utG+hwAIMevoB/aPkKQFc97nCxBEFASxEuq0CVsaxQjcJ/9kEngi4L95r",
        "X-Context": "lnWxt67utG+hwAIMevoB/aPkKQFc97nCxBEFASxEuq0CVsaxQjcJ/9kEngi4L95r",
        "Cookie": "b9ebac9e/accept-language=en-US,en; UILang=fr; lastKnownIpv6TabState=visible; b9ebac9e/sessid=tfjXn8qDNfdOhwQ9i3UUr6aN; sah/contextId=lnWxt67utG%2BhwAIMevoB%2FaPkKQFc97nCxBEFASxEuq0CVsaxQjcJ%2F9kEngi4L95r",
    }

    # Request topology data
    data = {
        "service": "TopologyDiagnostics",
        "method": "buildTopology",
        "parameters": {"SendXmlFile": False},
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching devices: {str(e)}")
        raise


def generate_markdown(devices_data):
    markdown = "# Connected Devices\n\n"
    markdown += (
        "| Device Name | IP Address | MAC Address | Connection Type | Status |\n"
    )
    markdown += (
        "|-------------|------------|-------------|-----------------|--------|\n"
    )

    try:
        for device in devices_data.get("status", {}).get("nodes", []):
            name = device.get("name", "Unknown")
            ip = device.get("ipaddress", "N/A")
            mac = device.get("physaddress", "N/A")
            conn_type = device.get("connectiontype", "N/A")
            status = device.get("active", False)
            status_str = "Active" if status else "Inactive"

            markdown += f"| {name} | {ip} | {mac} | {conn_type} | {status_str} |\n"

    except Exception as e:
        print(f"Error generating markdown: {str(e)}")
        print(f"Raw data structure: {json.dumps(devices_data, indent=2)[:200]}...")

    return markdown


def fetch_nat_rules():
    url = "http://192.168.1.1/ws"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-sah-ws-4-call+json",
        "Authorization": "X-Sah lnWxt67utG+hwAIMevoB/aPkKQFc97nCxBEFASxEuq0CVsaxQjcJ/9kEngi4L95r",
        "X-Context": "lnWxt67utG+hwAIMevoB/aPkKQFc97nCxBEFASxEuq0CVsaxQjcJ/9kEngi4L95r",
    }

    data = {
        "service": "Firewall",
        "method": "getPortForwarding",
        "parameters": {},
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()

        # Clean the response text by removing control characters
        cleaned_text = "".join(
            char for char in response.text if ord(char) >= 32 or char in "\n\r"
        )

        return json.loads(cleaned_text)
    except Exception as e:
        print(f"Error fetching NAT rules: {str(e)}")
        raise


def main():
    try:
        devices = fetch_devices()
        markdown = generate_markdown(devices)

        # Save to markdown file
        with open("livebox_devices.md", "w", encoding="utf-8") as f:
            f.write(markdown)

        print("Device list generated successfully!")

        # Also print to console
        print("\nConnected Devices:")
        print(markdown)

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
