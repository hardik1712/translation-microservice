from flask import jsonify, request, render_template_string
from app import app
from app.mock_translation import mock_translator

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Translation Service</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 600px; margin: 0 auto; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        select, input[type="text"] { width: 100%; padding: 8px; margin-bottom: 10px; }
        button { padding: 10px 15px; background: #4CAF50; color: white; border: none; cursor: pointer; }
        .result { margin-top: 20px; padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Translation Service</h1>
        <form method="POST" action="/translate">
            <div class="form-group">
                <label for="text">Text to Translate:</label>
                <input type="text" id="text" name="text" required>
            </div>
            <div class="form-group">
                <label for="target_language">Target Language:</label>
                <select id="target_language" name="target_language" required>
                    <option value="hi">Hindi</option>
                    <option value="ta">Tamil</option>
                    <option value="kn">Kannada</option>
                    <option value="bn">Bengali</option>
                    <option value="en">English</option>
                </select>
            </div>
            <button type="submit">Translate</button>
        </form>
        {% if translated_text %}
        <div class="result">
            <h3>Translation:</h3>
            <p>{{ translated_text }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/translate", methods=["GET", "POST"])
def translate():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        text = data.get("text")
        target_language = data.get("target_language")

        if not text or not target_language:
            return jsonify({"error": "text and target_language are required"}), 400

        translated_text = mock_translator.translate(text, target_language)
        
        if request.is_json:
            return jsonify({"translated_text": translated_text})
        else:
            return render_template_string(HTML_TEMPLATE, translated_text=translated_text)
            

    return render_template_string(HTML_TEMPLATE)
