from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)
clients_info = {}  # Dictionary to store information from clients

def format_info(key, value):
    if key == 'timestamp':
        return datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(value, bool):
        return 'Yes' if value else 'No'
    elif isinstance(value, (float, int)):
        return f'{value:,}'  # Format numbers with commas
    elif isinstance(value, dict):
        return ', '.join([f'{k}: {v}' for k, v in value.items()])
    return value

@app.route('/update', methods=['POST'])
def update_info():
    data = request.json
    client_id = data['client_id']
    clients_info[client_id] = data['info']
    return "Info Updated", 200

@app.route('/data')
def get_data():
    formatted_info = {
        client_id: {key: format_info(key, value) for key, value in info.items()}
        for client_id, info in clients_info.items()
    }
    return jsonify(formatted_info)

@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Aculi-Observe</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        body { background-color: #333; color: #fff; }
        .container { margin-top: 20px; }
        .card { background-color: #444; }
        .card-header, .card-body { color: #fff; }
        .github-image {
            position: absolute;
            top: 0;
            left: 0;
            max-height: 50px;
        }
        .grid-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding: 10px;
            margin-top: 60px;
        }
        .grid-item {
            background-color: #444;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
            flex: 1 1 calc(33.333% - 20px);  /* Ensure three items per row with spacing */
            box-sizing: border-box;
        }
        .grid-item h5 {
            font-size: 1rem;
        }
        .grid-item ul {
            font-size: 0.875rem;
            text-align: left;
        }
    </style>
    <script>
        function updateData() {
            $.get('/data', function(data) {
                $('.grid-container').empty();
                $.each(data, function(client_id, info) {
                    var item = '<div class="grid-item">' +
                               '<h5>Client ID: ' + client_id + '</h5>' +
                               '<ul class="list-unstyled">';
                    $.each(info, function(key, value) {
                        item += '<li><strong>' + key + ':</strong> ' + value + '</li>';
                    });
                    item += '</ul></div>';
                    $('.grid-container').append(item);
                });
            });
        }

        $(document).ready(function() {
            updateData();
            setInterval(updateData, 2000);  // Update every 2 seconds
        });
    </script>
</head>
<body>
    <img src="https://raw.githubusercontent.com/Fischherboot/Aculi/main/watermark-no-bg.png" alt="GitHub Image" class="github-image">
    <div class="container">
        <h2 class="text-center mb-4">Aculi-Observe</h2>
        <div class="grid-container">
        <!-- Grid items will be populated by JavaScript -->
        </div>
    </div>
</body>
</html>
    """, clients_info=clients_info, format_info=format_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
