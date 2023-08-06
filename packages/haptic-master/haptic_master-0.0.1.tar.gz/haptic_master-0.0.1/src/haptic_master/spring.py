class Spring:
    def __init__(self, name: str, stiffness: float = 0.0,
                 position: list = [0.0, 0.0, 0.0],
                 direction: list = [0.0, 0.0, 0.0],
                 damp_factor: float = 0.0,
                 max_force: float = 0.0) -> None:
        self._name = name
        self._stiffness = stiffness
        self._position = position
        self._direction = direction
        self._damp_factor = damp_factor
        self._max_force = max_force

    @property
    def name(self) -> str:
        return self._name

    @property
    def stiffness(self) -> float:
        return self._stiffness

    @stiffness.setter
    def stiffness(self, new_stiffness: float) -> None:
        self._stiffness = new_stiffness

    @property
    def position(self) -> list:
        return self._position

    @position.setter
    def position(self, new_position: list) -> None:
        self._position = new_position

    @property
    def direction(self) -> list:
        return self._direction

    @direction.setter
    def direction(self, new_direction: list) -> None:
        self._direction = new_direction

    @property
    def damp_factor(self) -> float:
        return self._damp_factor

    @damp_factor.setter
    def damp_factor(self, new_damp_factor: float) -> None:
        self._damp_factor = new_damp_factor

    @property
    def max_force(self) -> float:
        return self._max_force

    @max_force.setter
    def max_force(self, new_max_force: float) -> None:
        self._max_force = new_max_force
