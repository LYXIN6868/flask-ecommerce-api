from decimal import Decimal


def serialize(item):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(item.__class__).columns]
    result = {}
    for c in columns:
        value = getattr(item, c)
        # DECIMAL 不能被 Flask 直接序列化，转成 float
        if isinstance(value, Decimal):
            value = float(value)
        result[c] = value
    return result
