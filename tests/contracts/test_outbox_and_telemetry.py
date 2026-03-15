def test_outbox_event_structure(outbox_event):
    assert outbox_event.get("event_type") == "provision.requested"
    payload = outbox_event.get("payload")
    assert payload and "order_id" in payload and "operation_id" in payload
    items = payload.get("items", [])
    assert isinstance(items, list) and len(items) > 0


def test_telemetry_event_fields(telemetry_event):
    assert "event_type" in telemetry_event
    assert "payload" in telemetry_event
    assert telemetry_event["payload"].get("matrix_version"), "Telemetry event must include matrix_version"
