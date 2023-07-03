import http.client

conn = http.client.HTTPSConnection("api.browse.ai")

headers = { 'Authorization': "Bearer 8f5212bd-890c-4616-95fe-15315aa1524b:f9c9fb24-2ff4-4da0-afc9-c3147af119b7" }

conn.request("GET", "/v2/{55357a73-6b60-48cd-8641-8004b01f5d74}/tasks/{taskId}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))