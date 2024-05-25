from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Define preset options
PRESETS = {
    'resets': ['reset', 'reboot', 'restart'],
    'USB': ['USB', 'Universal Serial Bus', 'usb connection'],
    'touch': ['touch', 'touchscreen', 'touch panel'],
    'critical error': ['critical error', 'fatal error', 'system failure']
}


def search_file(file_path, phrases):
    results = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if any(phrase.lower() in line.lower() for phrase in phrases):
                results.append(line)
    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = []
    if request.method == 'POST':
        search_phrase = request.form.get('search_phrase')
        preset_options = request.form.getlist('preset_options')
        uploaded_files = request.files.getlist('files')

        # Collect phrases to search for
        phrases = []
        if search_phrase:
            phrases.append(search_phrase)

        for option in preset_options:
            phrases.extend(PRESETS[option])

        # Search through each uploaded file
        for file in uploaded_files:
            file_path = os.path.join('uploaded_files', file.filename)
            file.save(file_path)
            results = search_file(file_path, phrases)
            search_results.extend(results)

        # Highlight and bold the found phrases in the results
        highlighted_results = []
        for result in search_results:
            for phrase in phrases:
                result = result.replace(phrase, f'<strong>{phrase}</strong>')
            highlighted_results.append(result)

        return render_template('index.html', results=highlighted_results)

    return render_template('index.html', results=None)


if __name__ == '__main__':
    app.run(debug=True)
