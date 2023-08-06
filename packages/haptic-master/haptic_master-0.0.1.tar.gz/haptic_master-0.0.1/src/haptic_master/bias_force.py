class BiasForce:
    def __init__(self, name: str, force: list = [0.0, 0.0, 0.0]) -> None:
        self._name = name
        self._force = force

    @property
    def name(self) -> str:
        return self._name

    @property
    def force(self) -> list:
        return self._force

    @force.setter
    def force(self, new_force: list) -> None:
        self._force = new_force