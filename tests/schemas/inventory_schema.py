INVENTORY_SCHEMA = {
    "type": "object",
    "additionalProperties": {
        "type": "integer",
        "minimum": 0,
        "status": {
            "type": "string",
            "enum": ["placed", "approved", "delivered", "canceled"]
        },
        "quantity": {
            "type": "integer"
        },
        "required": ["quantity","status"],
        "additionalProperties": False
    }

}
