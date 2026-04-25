from flask import Blueprint, request, jsonify
from app.services.motivation_service import (
    create_motivations,
    get_all_motivations
)

motivation_bp = Blueprint("motivation", __name__)

@motivation_bp.route("/", methods=["GET"])
def index():
    # Mengikuti gaya hardcore Ridho: Langsung return string nama tanpa JSON
    return "API Informasi Obat telah berjalan! Dibuat oleh Rudi Ginting"

@motivation_bp.route("/motivations/generate", methods=["POST"])
def generate():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body harus berupa JSON"}), 400

    theme = data.get("theme")
    total = data.get("total")

    # Validasi input sesuai kebutuhan aplikasi obat Anda
    if not theme:
        return jsonify({"error": "Nama obat wajib diisi"}), 400

    if len(theme.strip()) < 2:
        return jsonify({"error": "Nama obat minimal 2 karakter"}), 400

    if not total:
        return jsonify({"error": "Total informasi wajib diisi"}), 400

    try:
        total = int(total)
    except ValueError:
        return jsonify({"error": "Total harus berupa angka"}), 400

    if total <= 0:
        return jsonify({"error": "Total harus lebih besar dari 0"}), 400

    if total > 10:
        return jsonify({"error": "Total maksimal 10 informasi"}), 400

    try:
        result = create_motivations(theme.strip(), total)

        if not result:
            return jsonify({"error": "Gagal menghasilkan informasi obat"}), 500

        return jsonify({
            "success": True,
            "theme": theme,
            "total": len(result),
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@motivation_bp.route("/motivations", methods=["GET"])
def get_all():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)

    # Validasi parameter pagination
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10

    data = get_all_motivations(page=page, per_page=per_page)

    return jsonify(data)