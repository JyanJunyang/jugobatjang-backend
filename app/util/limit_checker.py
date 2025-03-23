def can_add_more(current, max_limit) -> bool:
    """더 추가생성해도 되는지 체크하는 로직."""
    if current >= max_limit:
        return False
    return True
