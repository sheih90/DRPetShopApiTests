PET_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "category": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                }
            },
            "required": ["id", "name"],
            "additionalProperties": False
        },
        "photoUrls": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "tags": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    }
                },
                "required": ["id", "name"],
                "additionalProperties": False
            }
        },
        "status": {
            "type": "string",
            "enum": ["available", "pending", "sold"]
        }
    },
    "required": ["id", "name", "photoUrls", "status"],
    "additionalProperties": False
}

INVENTORY_SCHEMA = {
    "type": "object",
    "properties": {
        "approved": {
            "type": "integer",
            "minimum": 0,
            "description": "Количество одобренных товаров"
        },
        "available": {
            "type": "integer",
            "minimum": 0,
            "description": "Количество доступных товаров"
        },
        "delivered": {
            "type": "integer",
            "minimum": 0,
            "description": "Количество доставленных товаров"
        }
    },
    "required": ["approved", "available", "delivered"],
    "additionalProperties": False
}
