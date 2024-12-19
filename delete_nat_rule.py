import requests
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def delete_nat_rule():
    url = "http://192.168.1.1/ws"
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/x-sah-ws-4-call+json",
        "Authorization": "X-Sah lnWxt67utG+hwAIMevoB/aPkKQFc97nCxBEFASxEuq0CVsaxQjcJ/9kEngi4L95r",
        "X-Context": "lnWxt67utG+hwAIMevoB/aPkKQFc97nCxBEFASxEuq0CVsaxQjcJ/9kEngi4L95r",
    }

    # Delete the problematic rule
    data = {
        "service": "Firewall",
        "method": "deletePortForwarding",
        "parameters": {
            "id": "webui_Secure Shell Server (SSH)"  # The problematic rule ID
        },
    }

    try:
        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        print("Successfully deleted the problematic rule")

        # Now create a new clean rule
        data = {
            "service": "Firewall",
            "method": "addPortForwarding",
            "parameters": {
                "id": "SSH_Server",  # New clean ID
                "origin": "webui",
                "protocol": "6",  # TCP
                "externalPort": "22",
                "internalPort": "22",
                "destinationIPAddress": "192.168.1.43",  # Your Mac mini's IP
                "sourceInterface": "data",
                "description": "SSH Server",
                "persistent": True,
                "enable": True,
            },
        }

        response = requests.post(url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        print("Successfully created new clean rule")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    delete_nat_rule()
