import json
import re


def _strip_fences(text: str) -> str:
    """Remove markdown code fences."""
    text = re.sub(r"```[a-zA-Z]*", "", text)
    return text.replace("```", "").strip()


def _fix_control_chars(text: str) -> str:
    """Replace raw newlines/tabs inside JSON string values with escaped versions."""
    # Replace literal newlines that are inside JSON strings (not structural)
    # We do this by only replacing \n/\t that appear between quotes
    result = []
    in_string = False
    escape_next = False
    for ch in text:
        if escape_next:
            result.append(ch)
            escape_next = False
            continue
        if ch == "\\" and in_string:
            result.append(ch)
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            result.append(ch)
            continue
        if in_string and ch == "\n":
            result.append("\\n")
            continue
        if in_string and ch == "\t":
            result.append("\\t")
            continue
        if in_string and ch == "\r":
            continue
        result.append(ch)
    return "".join(result)


def _extract_first_json_block(text: str, opener: str = "{", closer: str = "}") -> str:
    """
    Extract the first complete JSON object or array from text,
    even if the LLM truncated or appended extra content.
    """
    start = text.find(opener)
    if start == -1:
        return ""

    depth = 0
    in_string = False
    escape_next = False

    for i, ch in enumerate(text[start:], start):
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                return text[start: i + 1]
    # Truncated — try to close it ourselves
    return text[start:] + (closer * depth)


def _try_parse(text: str) -> dict | list:
    return json.loads(text)


def parse_json(text: str) -> dict | list:
    """
    Robust JSON parser that handles:
    - Markdown code fences
    - Raw control characters inside strings
    - Truncated JSON
    - Extra text before/after JSON
    """
    text = _strip_fences(text)

    # Detect whether the top-level is object or array
    obj_pos   = text.find("{")
    arr_pos   = text.find("[")
    use_array = arr_pos != -1 and (obj_pos == -1 or arr_pos < obj_pos)

    opener, closer = ("[", "]") if use_array else ("{", "}")
    block = _extract_first_json_block(text, opener, closer)

    if not block:
        raise ValueError("No JSON object or array found in text")

    # Attempt 1: parse as-is
    try:
        return _try_parse(block)
    except json.JSONDecodeError:
        pass

    # Attempt 2: fix control characters
    try:
        return _try_parse(_fix_control_chars(block))
    except json.JSONDecodeError:
        pass

    # Attempt 3: strip trailing comma before closing brace/bracket
    cleaned = re.sub(r",\s*([}\]])", r"\1", _fix_control_chars(block))
    try:
        return _try_parse(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse JSON after all attempts: {e}\nBlock: {block[:300]}")
