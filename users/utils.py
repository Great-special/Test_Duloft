import uuid


def generate_ref_code():
    ref_code = str(uuid.uuid4()).replace('-', '')[:16]
    return ref_code