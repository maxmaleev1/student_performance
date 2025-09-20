_REGISTRY = {}


def register(name):
    """Декоратор для регистрации функции как отчёта с указанным именем."""
    def deco(fn):
        _REGISTRY[name] = fn
        return fn
    return deco


def get_report(name):
    """Возвращает функцию-обработчик отчёта по имени."""
    if name not in _REGISTRY:
        raise KeyError(f'Unknown report: {name}')
    return _REGISTRY[name]


def available_reports():
    """Возвращает список доступных отчётов."""
    return sorted(_REGISTRY.keys())
