import os
from dotenv import load_dotenv
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management
load_dotenv()

# Initialize Pinecone with API key and assistant
api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key)
assistant = pc.assistant.Assistant(assistant_name="lra")


def format_links_with_citations(content, citations):
    """Format content by replacing citation links with friendly names and appending HTML-formatted references."""
    # Append a References section at the end of the content if there are citations
    if citations:
        content += "<br><br><strong>References:</strong><br>"
        for index, citation in enumerate(citations, start=1):
            for reference in citation.get("references", []):
                file_info = reference.get("file", {})
                file_name = file_info.get("name")
                file_url = file_info.get("signed_url")
                if file_name and file_url:
                    content += f'{index}. <a href="{file_url}" target="_blank">{file_name}</a><br>'

    return content


@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'history' not in session:
        session['history'] = []

    if request.method == 'POST':
        user_message = request.form['message_content']
        session['history'].append({'sender': 'User', 'message': user_message})

        # Prepare the user message for the assistant
        msg = Message(content=user_message)

        # Use the assistant to get a response with structured citations
        resp = assistant.chat(messages=[msg])
        assistant_response = resp.message.content if resp and resp.message else "Error: No response"

        print("Citations:", resp.citations)

        # Format assistant response with friendly links
        if resp and resp.citations:
            assistant_response = format_links_with_citations(assistant_response, resp.citations)

        # Add the assistant's response to the chat history
        session['history'].append({'sender': 'I-DealAI', 'message': assistant_response})

        # Save session data and reload the page to avoid re-submitting
        session.modified = True
        return redirect(url_for('chat'))

    return render_template('chat.html', history=session['history'])


@app.route('/reset')
def reset():
    session.pop('history', None)  # Clear chat history
    return redirect(url_for('chat'))


if __name__ == '__main__':
    app.run(debug=True)
