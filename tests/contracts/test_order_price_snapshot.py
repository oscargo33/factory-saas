def test_orderline_price_snapshot_consistency(order_line, price_snapshot):
    ol_snapshot = order_line.get("price_snapshot")
    assert ol_snapshot, "order_line must include embedded price_snapshot"
    assert ol_snapshot.get("id") == price_snapshot.get("id"), "OrderLine price_snapshot.id should match price_snapshot fixture"

def test_orderline_product_type_presence(order_line):
    assert "product_type" in order_line, "order_line must include product_type"
    assert order_line["product_type"] in ("subscription", "one_time", "metered")
