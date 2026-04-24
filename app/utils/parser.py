from flask import Blueprint, request, jsonify
from app.services.medicine_service import (
    create_medicines,
    get_all_medicines,
    get_medicine_by_id
)

medicine_bp = Blueprint("medicine", __name__)

@medicine_bp.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "API Obat telah berjalan!",
        "status": "active",
        "endpoints": [
            "/medicines/generate",
            "/medicines",
            "/medicines/<id>"
        ]
    })

@medicine_bp.route("/medicines/generate", methods=["POST"])
def generate():
    data = request.get_json()
    disease = data.get("disease")
    total = data.get("total")

    if not disease:
        return jsonify({"error": "Penyakit (disease) diperlukan"}), 400

    if not total:
        return jsonify({"error": "Total diperlukan"}), 400

    try:
        total = int(total)
    except ValueError:
        return jsonify({"error": "Total harus berupa angka"}), 400

    if total <= 0:
        return jsonify({"error": "Total harus lebih dari 0"}), 400

    if total > 10:
        return jsonify({"error": "Total maksimal 10"}), 400

    try:
        result = create_medicines(disease, total)

        return jsonify({
            "disease": disease,
            "total": len(result),
            "data": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@medicine_bp.route("/medicines", methods=["GET"])
def get_all():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)

    data = get_all_medicines(page=page, per_page=per_page)
    return jsonify(data)


@medicine_bp.route("/medicines/<int:medicine_id>", methods=["GET"])
def get_detail(medicine_id):
    medicine = get_medicine_by_id(medicine_id)
    if medicine:
        return jsonify(medicine)
    return jsonify({"error": "Obat tidak ditemukan"}), 404