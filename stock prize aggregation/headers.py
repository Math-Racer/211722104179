import json
# Replace secrets.json content with recent response from the Authorization request
with open("secrets.json", "r") as file:
    token_data = json.load(file)

token_type = token_data.get("token_type", "Bearer")
access_token = token_data.get("access_token")

headers = {
    "Authorization": f"{token_type} {access_token}"
}
