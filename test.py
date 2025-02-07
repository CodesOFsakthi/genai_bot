from flask import Flask, request, jsonify

app = Flask(__name__)

# Example document links (fetch these from your MySQL database in the actual implementation)
documents = {
    "Coordinator's Message": "https://example.com/coordinator-message.pdf",
    "Member List": "https://example.com/member-list.pdf",
    "Meeting Minutes": {
        "22-23 First Meeting": "https://example.com/meeting-22-23-1.pdf",
        "22-23 Second Meeting": "https://example.com/meeting-22-23-2.pdf",
    },
    "Policy Manual": "https://example.com/policy-manual.pdf"
}

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    user_input = data.get('message', '').lower().strip()
    reply = "Sorry, I didn't catch that."
    buttons = []  # List to store button options

    if "iqac" in user_input:
        reply = "IQAC includes the following sections. Click on the one you need:"
        buttons = [
            {"text": "Coordinator's Message", "url": documents["Coordinator's Message"]},
            {"text": "Member List", "url": documents["Member List"]},
            {"text": "Policy Manual", "url": documents["Policy Manual"]},
        ]
        # Add Meeting Minutes buttons dynamically
        for key, url in documents["Meeting Minutes"].items():
            buttons.append({"text": key, "url": url})

    response_data = {"reply": reply, "buttons": buttons}
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
