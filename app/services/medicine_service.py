from app.extensions import SessionLocal
from app.models.medicine import Medicine  # ← Perbaiki ini!
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_gemini
from app.utils.parser import parse_llm_response

def create_medicines(disease: str, total: int):
    session = SessionLocal()

    try:
        prompt = f"""
        Berikan informasi tentang {total} obat yang umum digunakan untuk mengatasi penyakit "{disease}".

        Format response HARUS dalam bentuk JSON seperti berikut:
        {{
            "medicines": [
                {{
                    "name": "Nama Obat",
                    "description": "Deskripsi singkat tentang obat",
                    "indication": "Indikasi/kegunaan utama",
                    "dosage": "Dosis umum yang direkomendasikan",
                    "side_effect": "Efek samping yang mungkin terjadi"
                }}
            ]
        }}

        Pastikan response hanya berisi JSON tanpa teks tambahan di luar JSON.
        """

        result = generate_from_gemini(prompt)
        medicines = parse_llm_response(result)

        # Save request log
        req_log = RequestLog(disease=disease, total=total)
        session.add(req_log)
        session.commit()

        saved = []

        for item in medicines:
            medicine = Medicine(
                name=item.get("name", ""),
                description=item.get("description", ""),
                indication=item.get("indication", ""),
                dosage=item.get("dosage", ""),
                side_effect=item.get("side_effect", ""),
                request_id=req_log.id
            )
            session.add(medicine)
            saved.append({
                "name": medicine.name,
                "description": medicine.description,
                "indication": medicine.indication,
                "dosage": medicine.dosage,
                "side_effect": medicine.side_effect
            })

        session.commit()
        return saved

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_medicines(page: int = 1, per_page: int = 10):
    session = SessionLocal()

    try:
        query = session.query(Medicine)

        total = query.count()

        data = (
            query
            .order_by(Medicine.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": m.id,
                "name": m.name,
                "description": m.description,
                "indication": m.indication,
                "dosage": m.dosage,
                "side_effect": m.side_effect,
                "created_at": m.created_at.isoformat()
            }
            for m in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page if total > 0 else 1,
            "data": result
        }

    finally:
        session.close()


def get_medicine_by_id(medicine_id: int):
    session = SessionLocal()
    try:
        medicine = session.query(Medicine).filter(Medicine.id == medicine_id).first()
        if medicine:
            return {
                "id": medicine.id,
                "name": medicine.name,
                "description": medicine.description,
                "indication": medicine.indication,
                "dosage": medicine.dosage,
                "side_effect": medicine.side_effect,
                "created_at": medicine.created_at.isoformat()
            }
        return None
    finally:
        session.close()