from app.extensions import SessionLocal
from app.models.motivation import Motivation
from app.models.request_log import RequestLog
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response

def create_motivations(theme: str, total: int):
    session = SessionLocal()

    try:
        # ============================================================
        # PROMPT YANG DIPERBAIKI MENGGUNAKAN BEST PRACTICES
        # ============================================================
        # 1️⃣ ROLE PROMPTING - Memberi persona spesifik
        # 2️⃣ INSTRUCTIONAL PROMPTING - Instruksi yang jelas
        # 3️⃣ CONSTRAINT PROMPTING - Batasan yang tegas
        # 4️⃣ FORMAT PROMPTING - Output JSON terstruktur
        # ============================================================

        prompt = f"""
        [ROLE]
        Kamu adalah seorang apoteker klinis dengan pengalaman 10 tahun di rumah sakit terkemuka di Indonesia.
        Kamu terbiasa menjelaskan informasi obat kepada pasien dengan bahasa yang mudah dipahami.

        [TUGAS]
        Berikan {total} informasi penting tentang OBAT dengan topik "{theme}".

        [KRITERIA KUALITAS]
        Setiap informasi WAJIB:
        1. Akurat secara medis dan berbasis evidence-based medicine
        2. Edukatif dan bermanfaat bagi pasien awam
        3. Menggunakan bahasa Indonesia yang mudah dipahami (hindari istilah teknis tanpa penjelasan)
        4. Mencakup aspek: cara penggunaan, dosis dewasa, efek samping umum, kontraindikasi, atau interaksi obat

        [CONTOH TOPIK VALID]
        Paracetamol, Amoksisilin, Vitamin C, Ibuprofen, Cetirizine, Domperidone, Metformin, Amlodipine

        [FORMAT OUTPUT - WAJIB]
        Kamu HARUS mengembalikan JSON murni dengan struktur persis seperti ini:
        {{
            "motivations": [
                {{"text": "informasi obat pertama yang lengkap dan edukatif"}},
                {{"text": "informasi obat kedua yang lengkap dan edukatif"}}
            ]
        }}

        [BATASAN KERAS - JANGAN DILANGGAR]
        ❌ JANGAN tambahkan teks apapun di luar JSON (termasuk pembukaan, penutup, atau penjelasan)
        ❌ JANGAN gunakan markdown code block (```json atau ```)
        ❌ JANGAN gunakan karakter backtick (`)
        ❌ JANGAN buat informasi yang berbahaya atau menyesatkan
        ❌ JANGAN gunakan kalimat "Sebagai AI..." atau "Maaf, saya tidak bisa..."

        [PANJANG OUTPUT]
        Setiap informasi obat maksimal 200 karakter.

        [VERIFIKASI DIRI]
        Sebelum memberikan output, pastikan:
        - Apakah informasi ini aman untuk pasien awam?
        - Apakah dosis yang disebutkan sesuai standar?
        - Apakah saya menyebutkan peringatan yang diperlukan?
        """

        result = generate_from_llm(prompt)

        # Ambil response dari dictionary
        if isinstance(result, dict):
            raw_response = result.get("response", "")
        else:
            raw_response = result

        motivations = parse_llm_response(raw_response)

        # VALIDASI: Pastikan output tidak kosong
        if not motivations:
            raise Exception("Gemini tidak mengembalikan data yang valid")

        # save request log
        req_log = RequestLog(theme=theme)
        session.add(req_log)
        session.flush()

        saved = []
        for item in motivations:
            text = item.get("text")
            if text and len(text.strip()) > 10:  # Validasi minimal panjang
                m = Motivation(
                    text=text.strip(),
                    request_id=req_log.id
                )
                session.add(m)
                saved.append(text.strip())

        if not saved:
            raise Exception("Tidak ada informasi obat yang valid untuk disimpan")

        session.commit()
        return saved

    except Exception as e:
        session.rollback()
        print(f"Error di create_motivations: {e}")
        raise e

    finally:
        session.close()


def get_all_motivations(page: int = 1, per_page: int = 100):
    session = SessionLocal()

    try:
        query = session.query(Motivation)
        total = query.count()

        data = (
            query
            .order_by(Motivation.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )

        result = [
            {
                "id": m.id,
                "text": m.text,
                "created_at": m.created_at.isoformat() if m.created_at else None
            }
            for m in data
        ]

        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
            "data": result
        }

    finally:
        session.close()