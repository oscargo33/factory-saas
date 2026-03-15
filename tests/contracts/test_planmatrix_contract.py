def test_planmatrix_schema(plan_matrix):
    assert "id" in plan_matrix
    assert "version" in plan_matrix
    assert isinstance(plan_matrix.get("allowed_products"), list)
    assert isinstance(plan_matrix.get("allowed_verticals"), dict)


def test_product_in_plan(plan_matrix, product_detail):
    pid = product_detail.get("product_id")
    assert pid in plan_matrix.get("allowed_products", []), "Product must be listed in PlanMatrix allowed_products for this fixture"
