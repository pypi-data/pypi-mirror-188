from __future__ import annotations
import picocolorsensor._impl
import typing

__all__ = [
    "PicoColorSensor"
]


class PicoColorSensor():
    class RawColor():
        def __init__(self) -> None: ...
        @property
        def blue(self) -> int:
            """
            :type: int
            """
        @blue.setter
        def blue(self, arg0: int) -> None:
            pass
        @property
        def green(self) -> int:
            """
            :type: int
            """
        @green.setter
        def green(self, arg0: int) -> None:
            pass
        @property
        def ir(self) -> int:
            """
            :type: int
            """
        @ir.setter
        def ir(self, arg0: int) -> None:
            pass
        @property
        def red(self) -> int:
            """
            :type: int
            """
        @red.setter
        def red(self, arg0: int) -> None:
            pass
        pass
    def __init__(self) -> None: ...
    def getLastReadTimestamp(self) -> seconds: ...
    def getProximity0(self) -> int: ...
    def getProximity1(self) -> int: ...
    def getRawColor0(self) -> PicoColorSensor.RawColor: ...
    def getRawColor1(self) -> PicoColorSensor.RawColor: ...
    def isSensor0Connected(self) -> bool: ...
    def isSensor1Connected(self) -> bool: ...
    def setDebugPrints(self, debug: bool) -> None: ...
    pass
