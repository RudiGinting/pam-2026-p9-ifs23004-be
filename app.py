from app import create_app
from app.config import Config
import traceback
from flask import jsonify

app = create_app()

# ======== KODE DEBUGGING (RADAR) ========
# Kode ini akan menangkap semua error yang membuat server pingsan,
# lalu mengirimkan detailnya kembali ke layar kamu.
@app.errorhandler(Exception)
def handle_exception(e):
    error_trace = traceback.format_exc()
    print("=== ERROR DETECTED ===")
    print(error_trace)
    return jsonify({
        "status": "CRASHED",
        "pesan_error": str(e),
        "lokasi_error": error_trace
    }), 500
# ========================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(Config.APP_PORT), debug=False)