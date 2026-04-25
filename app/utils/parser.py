import json
import re

def parse_llm_response(result):
    """
    Parse response dari LLM dengan berbagai skenario error handling.
    Menerapkan best practices untuk parsing output yang tidak terstruktur.
    """
    try:
        # Ambil content string
        content = result.get("response") if isinstance(result, dict) else result

        if not content or not isinstance(content, str):
            raise Exception("Response kosong atau bukan string")

        # Langkah 1: Hapus markdown code block
        content = re.sub(r"```json\s*", "", content)
        content = re.sub(r"```\s*", "", content)

        # Langkah 2: Hapus whitespace berlebih
        content = content.strip()

        # Langkah 3: Cari JSON object pertama dalam teks
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            content = json_match.group()

        # Langkah 4: Parse JSON
        parsed = json.loads(content)

        # Langkah 5: Validasi struktur
        if "motivations" not in parsed:
            raise Exception("JSON tidak memiliki key 'motivations'")

        if not isinstance(parsed["motivations"], list):
            raise Exception("'motivations' harus berupa list")

        return parsed.get("motivations", [])

    except json.JSONDecodeError as e:
        raise Exception(f"JSON tidak valid: {str(e)}. Content: {content[:200]}")
    except Exception as e:
        raise Exception(f"Gagal parse response LLM: {str(e)}")