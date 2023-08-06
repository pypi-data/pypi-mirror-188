class Damper:
    def __init__(self, name: str, damping: list = [0.0, 0.0, 0.0]) -> None:
        self._name = name
        self._damping = damping
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def damping(self) -> list:
        return self._damping

    @damping.setter
    def damping(self, new_damping: list) -> None:
        self._damping = new_damping