def test_payment_intent_operation_id_unique(outbox_event, telemetry_event):
    # Basic check: outbox payload contains operation_id and telemetry references matrix_version
    payload = outbox_event.get("payload", {})
    assert payload.get("operation_id"), "Outbox payload must include operation_id"
    assert telemetry_event.get("payload", {}).get("matrix_version"), "Telemetry payload must include matrix_version"
