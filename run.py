from src import app
import os

app.secret_key = 'S1m0n4m0n4'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)