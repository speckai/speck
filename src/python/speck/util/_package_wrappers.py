def get_dict(instance):
    return instance.model_dump() if hasattr(instance, "model_dump") else instance.dict()
