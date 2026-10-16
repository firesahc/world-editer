"""Minimal big-endian NBT read/write for 1.12 Java Edition."""
import struct


TAG_END = 0
TAG_BYTE = 1
TAG_SHORT = 2
TAG_INT = 3
TAG_LONG = 4
TAG_FLOAT = 5
TAG_DOUBLE = 6
TAG_BYTE_ARRAY = 7
TAG_STRING = 8
TAG_LIST = 9
TAG_COMPOUND = 10
TAG_INT_ARRAY = 11
TAG_LONG_ARRAY = 12


def read_root(data):
    """Parse root compound. Returns (name, compound_dict, consumed)."""
    pos = 0
    assert data[pos] == TAG_COMPOUND
    pos += 1
    n = struct.unpack(">H", data[pos:pos + 2])[0]
    pos += 2
    name = data[pos:pos + n].decode("utf-8")
    pos += n
    comp, pos = _read_compound(data, pos)
    return name, comp, pos


def _read_string(data, pos):
    n = struct.unpack(">H", data[pos:pos + 2])[0]
    pos += 2
    s = data[pos:pos + n].decode("utf-8")
    pos += n
    return pos, s


def _read_payload(data, pos, t):
    if t == TAG_BYTE:
        return pos + 1, data[pos]
    if t == TAG_SHORT:
        return pos + 2, struct.unpack(">h", data[pos:pos + 2])[0]
    if t == TAG_INT:
        return pos + 4, struct.unpack(">i", data[pos:pos + 4])[0]
    if t == TAG_LONG:
        return pos + 8, struct.unpack(">q", data[pos:pos + 8])[0]
    if t == TAG_FLOAT:
        return pos + 4, struct.unpack(">f", data[pos:pos + 4])[0]
    if t == TAG_DOUBLE:
        return pos + 8, struct.unpack(">d", data[pos:pos + 8])[0]
    if t == TAG_BYTE_ARRAY:
        n = struct.unpack(">i", data[pos:pos + 4])[0]
        pos += 4
        v = bytes(data[pos:pos + n])
        pos += n
        return pos, ("bytearray", v)
    if t == TAG_STRING:
        pos, s = _read_string(data, pos)
        return pos, s
    if t == TAG_LIST:
        t2 = data[pos]
        pos += 1
        n = struct.unpack(">i", data[pos:pos + 4])[0]
        pos += 4
        out = []
        for _ in range(n):
            pos, val = _read_payload(data, pos, t2)
            out.append(val)
        return pos, ("list", t2, out)
    if t == TAG_COMPOUND:
        comp, newpos = _read_compound(data, pos)
        return newpos, comp
    if t == TAG_INT_ARRAY:
        n = struct.unpack(">i", data[pos:pos + 4])[0]
        pos += 4
        out = list(struct.unpack(">" + "i" * n, data[pos:pos + n * 4]))
        pos += n * 4
        return pos, ("intarray", out)
    if t == TAG_LONG_ARRAY:
        n = struct.unpack(">i", data[pos:pos + 4])[0]
        pos += 4
        out = list(struct.unpack(">" + "q" * n, data[pos:pos + n * 8]))
        pos += n * 8
        return pos, ("longarray", out)
    raise ValueError(f"unknown tag type {t}")


def _read_compound(data, pos):
    out = {}
    while True:
        t = data[pos]
        pos += 1
        if t == TAG_END:
            break
        pos, name = _read_string(data, pos)
        pos, value = _read_payload(data, pos, t)
        out[name] = (t, value)
    return out, pos


def write_root(name, comp):
    out = bytearray()
    out.append(TAG_COMPOUND)
    n = name.encode("utf-8")
    out += struct.pack(">H", len(n))
    out += n
    _write_compound(out, comp)
    return bytes(out)


def _write_payload(out, t, value):
    if t == TAG_BYTE:
        out.append(value & 0xFF)
    elif t == TAG_SHORT:
        out += struct.pack(">h", value)
    elif t == TAG_INT:
        out += struct.pack(">i", value)
    elif t == TAG_LONG:
        out += struct.pack(">q", value)
    elif t == TAG_FLOAT:
        out += struct.pack(">f", value)
    elif t == TAG_DOUBLE:
        out += struct.pack(">d", value)
    elif t == TAG_BYTE_ARRAY:
        v = value[1] if isinstance(value, tuple) else value
        out += struct.pack(">i", len(v))
        out += bytes(v)
    elif t == TAG_STRING:
        b = value.encode("utf-8")
        out += struct.pack(">H", len(b))
        out += b
    elif t == TAG_LIST:
        # value: (sub_tag, [values]) where values are typed-payloads
        sub, items = value[1], value[2] if isinstance(value, tuple) and len(value) == 3 else value[1]
        out.append(sub)
        out += struct.pack(">i", len(items))
        for it in items:
            _write_payload(out, sub, it)
    elif t == TAG_COMPOUND:
        _write_compound(out, value)
    elif t == TAG_INT_ARRAY:
        v = value[1] if isinstance(value, tuple) else value
        out += struct.pack(">i", len(v))
        out += struct.pack(">" + "i" * len(v), *v)
    elif t == TAG_LONG_ARRAY:
        v = value[1] if isinstance(value, tuple) else value
        out += struct.pack(">i", len(v))
        out += struct.pack(">" + "q" * len(v), *v)
    else:
        raise ValueError(f"cannot write tag {t}")


def _write_compound(out, comp):
    for name, (t, value) in comp.items():
        out.append(t)
        b = name.encode("utf-8")
        out += struct.pack(">H", len(b))
        out += b
        _write_payload(out, t, value)
    out.append(TAG_END)


def patch_field(raw_nbt, field_name, old_str, new_str):
    """Targeted string patch for one named TagString field; preserves everything."""
    tag = struct.pack(">H", len(field_name.encode("utf-8"))) + field_name.encode("utf-8")
    # full pattern: type byte (8) + name + length (short) + payload
    ob = old_str.encode("utf-8")
    nb = new_str.encode("utf-8")
    pattern_old = bytes([TAG_STRING]) + struct.pack(">H", len(field_name.encode("utf-8"))) + field_name.encode("utf-8") + struct.pack(">H", len(ob)) + ob
    pattern_new = bytes([TAG_STRING]) + struct.pack(">H", len(field_name.encode("utf-8"))) + field_name.encode("utf-8") + struct.pack(">H", len(nb)) + nb
    if raw_nbt.count(pattern_old) != 1:
        raise ValueError(f"pattern occurrence = {raw_nbt.count(pattern_old)}, field={field_name}")
    return raw_nbt.replace(pattern_old, pattern_new)


def patch_int(raw_nbt, field_name, new_int):
    tag_name = field_name.encode("utf-8")
    marker = bytes([TAG_INT]) + struct.pack(">H", len(tag_name)) + tag_name
    idx = raw_nbt.find(marker)
    if idx < 0:
        raise ValueError(f"field {field_name} not found as int")
    start = idx + len(marker)
    return raw_nbt[:start] + struct.pack(">i", new_int) + raw_nbt[start + 4:]


def walk(comp, path=""):
    """Yield (dotted_path, tag, value) for leaves."""
    if not isinstance(comp, dict):
        yield path, None, comp
        return
    for k, (tk, tv) in comp.items():
        p = (path + "." + k) if path else k
        if tk == TAG_COMPOUND:
            yield from walk(tv[1] if isinstance(tv, tuple) else tv, p)
        elif tk == TAG_LIST:
            # tv: (TAG_LIST, t2, [values]) -> our _read_payload returns ("list", t2, out)
            t2, items = tv[1], tv[2]
            for i, it in enumerate(items):
                yield from walk({f"[{i}]": (t2, it)} if False else {"": (t2, it)}, p + f"[{i}]")
        else:
            yield p, tk, tv


def find_field_path(comp, target, path=""):
    """Return dotted path to a field named target (first match)."""
    if not isinstance(comp, dict):
        return None
    for k, (tk, tv) in comp.items():
        p = (path + "." + k) if path else k
        if k == target:
            return p
        if tk == TAG_COMPOUND:
            sub = find_field_path(tv[1] if isinstance(tv, tuple) else tv, target, p)
            if sub:
                return sub
        elif tk == TAG_LIST:
            t2, items = tv[1], tv[2]
            for i, it in enumerate(items):
                sub = find_field_path({f"x": (t2, it)}, target, p + f"[{i}]")
                if sub:
                    return sub
    return None
