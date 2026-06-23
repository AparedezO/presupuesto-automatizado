from app.services.code_generator import generate_material_code


def test_generate_material_code_keeps_measurements():
    assert generate_material_code("Tubo PVC 3/4") == "TUBO-PVC-3/4"


def test_generate_material_code_removes_accents_and_stop_words():
    assert generate_material_code("Conector de compresión 4/0") == "CONE-COMP-4/0"
