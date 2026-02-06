from agent_server.tools.seats import get_all_seats

# ====== CHANGE THESE VALUES ONLY ======
BASE_URL = "http://localhost:2026"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY5NjhlM2U0ZmQxODFmYzAxOWNmZmFlMSIsInJvbGUiOiJ1c2VyIiwiaWF0IjoxNzcwMzcyNzEzLCJleHAiOjE3NzA0NTkxMTN9.U41x4zbpuZ6X0DbCg8vug0yO2X_W0E1W88gp93rfO6U"

payload = {
    "tripId": "696f033151154fe516cdcd46",
    "from": "Surat",
    "to": "Ahmedabad",
    "traveldate": "2026-02-13"
}
# =====================================


print(get_all_seats(payload,TOKEN))