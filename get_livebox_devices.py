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
        # The devices are in a different structure than expected
        topology = devices_data.get("status", [])[0]  # Get the first status item

        # Extract devices from the topology
        if "Children" in topology:
            for device in topology["Children"]:
                name = device.get("Name", "Unknown")
                ip = device.get("IPAddress", "N/A")
                mac = device.get("PhysAddress", "N/A")
                conn_type = device.get("ConnectionType", "N/A")
                status = device.get("Active", False)
                status_str = "Active" if status else "Inactive"

                markdown += f"| {name} | {ip} | {mac} | {conn_type} | {status_str} |\n"

    except Exception as e:
        print(f"Error generating markdown: {str(e)}")
        print(f"Raw data structure: {json.dumps(devices_data, indent=2)[:500]}...")
        # Print the full structure for debugging
        with open("debug_topology.json", "w", encoding="utf-8") as f:
            json.dump(devices_data, f, indent=2)
        print("Full topology data written to debug_topology.json")

    return markdown


def main():
    try:
        devices = fetch_devices()

        # Debug: Print the raw structure
        print("\nResponse structure:")
        print(json.dumps(devices, indent=2))

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
