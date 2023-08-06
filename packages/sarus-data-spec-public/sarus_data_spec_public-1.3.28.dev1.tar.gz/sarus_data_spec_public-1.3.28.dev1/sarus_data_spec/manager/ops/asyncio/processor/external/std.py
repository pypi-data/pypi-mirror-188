from typing import Any

from .utils import sarus_external_op


@sarus_external_op
async def add(val_1: Any, val_2: Any) -> Any:
    return val_1 + val_2


@sarus_external_op
async def sub(val_1: Any, val_2: Any) -> Any:
    return val_1 - val_2


@sarus_external_op
async def rsub(val_1: Any, val_2: Any) -> Any:
    return val_2 - val_1


@sarus_external_op
async def mul(val_1: Any, val_2: Any) -> Any:
    return val_1 * val_2


@sarus_external_op
async def div(val_1: Any, val_2: Any) -> Any:
    return val_1 / val_2


@sarus_external_op
async def rdiv(val_1: Any, val_2: Any) -> Any:
    return val_2 / val_1


@sarus_external_op
async def invert(val: Any) -> Any:
    return ~val


@sarus_external_op
async def length(val: Any) -> Any:
    return len(val)


@sarus_external_op
async def getitem(val: Any, key: Any) -> Any:
    return val[key]


@sarus_external_op
async def setitem(val: Any, key: Any, newvalue: Any) -> Any:
    val.__setitem__(key, newvalue)
    return val


@sarus_external_op
async def greater_than(val_1: Any, val_2: Any) -> Any:
    return val_1 > val_2


@sarus_external_op
async def greater_equal(val_1: Any, val_2: Any) -> Any:
    return val_1 >= val_2


@sarus_external_op
async def lower_than(val_1: Any, val_2: Any) -> Any:
    return val_1 < val_2


@sarus_external_op
async def lower_equal(val_1: Any, val_2: Any) -> Any:
    return val_1 <= val_2


@sarus_external_op
async def not_equal(val_1: Any, val_2: Any) -> Any:
    return val_1 != val_2


@sarus_external_op
async def neg(val_1: Any) -> Any:
    return -val_1


@sarus_external_op
async def pos(val_1: Any) -> Any:
    return +val_1


@sarus_external_op
async def _abs(val_1: Any) -> Any:
    return abs(val_1)


@sarus_external_op
async def _round(*args: Any, **kwargs: Any) -> Any:
    return round(*args, **kwargs)


@sarus_external_op
async def modulo(val_1: Any, val_2: Any) -> Any:
    return val_1 % val_2


@sarus_external_op
async def rmodulo(val_1: Any, val_2: Any) -> Any:
    return val_2 % val_1


@sarus_external_op
async def _or(val_1: Any, val_2: Any) -> Any:
    return val_1 | val_2


@sarus_external_op
async def ror(val_1: Any, val_2: Any) -> Any:
    return val_2 | val_1


@sarus_external_op
async def _and(val_1: Any, val_2: Any) -> Any:
    return val_1 & val_2


@sarus_external_op
async def rand(val_1: Any, val_2: Any) -> Any:
    return val_2 & val_1


@sarus_external_op
async def _int(*args: Any, **kwargs: Any) -> Any:
    return int(*args, **kwargs)


@sarus_external_op
async def _float(*args: Any, **kwargs: Any) -> Any:
    return float(*args, **kwargs)


@sarus_external_op
async def _list(*args: Any, **kwargs: Any) -> Any:
    return list(args)


@sarus_external_op
async def _dict(*args: Any, **kwargs: Any) -> Any:
    return dict(kwargs)


@sarus_external_op
async def _slice(*args: Any, **kwargs: Any) -> Any:
    return slice(*args, **kwargs)


@sarus_external_op
async def _set(*args: Any, **kwargs: Any) -> Any:
    return set(args)


@sarus_external_op
async def _tuple(*args: Any, **kwargs: Any) -> Any:
    return tuple(args)


@sarus_external_op
async def keys(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return list(parent_val.keys(*args, **kwargs))


@sarus_external_op
async def values(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return list(parent_val.values(*args, **kwargs))


@sarus_external_op
async def sudo(val: Any) -> Any:
    return val


@sarus_external_op
async def extend(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    parent_val.extend(*args, **kwargs)
    return parent_val


@sarus_external_op
async def append(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    parent_val.append(*args, **kwargs)
    return parent_val


@sarus_external_op
async def pop(parent_val: Any, *args: Any, **kwargs: Any) -> Any:
    return parent_val.pop(*args, **kwargs)
