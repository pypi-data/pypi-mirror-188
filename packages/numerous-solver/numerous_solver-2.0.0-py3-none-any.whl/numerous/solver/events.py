import numpy as np

from .interface import Interface
from .base import _Jitter, event

class Event(_Jitter):
    """
    The event base class for creating events (:class:~solver.interface.StateEvent and TimeEvent)
    """
    id: str
    _is_external: bool
    _trigger: bool

    def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:

        """Function called hen the event has been triggered. Can be used to trigger an action.
        Must be implemented if events are added to model.

        :param interface: model interface
        :type interface: :class:`~solver.interface.Interface`
        :param t: time
        :type t: float
        :param y: current solver and model states in numpy format
        :type y: :class:`numpy.ndarray`
        :return: updated states
        :rtype: :class:`numpy.ndarray`
        """

        raise NotImplementedError

    def is_triggered(self):
        """
        Helper function to check if event is trigged
        :return:
        """
        return self._trigger

    def clear(self):
        """
        Helper function to clear the event
        :return:
        """
        self._trigger = False

    def set(self):
        """
        Helper function to set event trigger
        :return:
        """
        self._trigger = True

    def reset(self):
        pass

    def post_event(self, interface: Interface, t: float, y: np.array):
        raise NotImplementedError

    def is_external(self):
        return self._is_external

    def get_id(self):
        return self.id

class TimeEvent(Event):
    """
    The base class for creating time events
    """
    def get_next_event_time(self, interface: Interface, t: float) -> float:
        raise NotImplementedError

    def post_event(self, interface: Interface, t: float, y: np.array):
        pass

class TimestampedEvent(TimeEvent):
    def __init__(self, id: str, timestamps: np.array, is_external: bool = False):
        self.id = id
        self._is_external = is_external
        self.timestamps = timestamps
        self._trigger = False
        self._last_ix = 0

    def get_next_event_time(self, interface: Interface, t: float):
        idx = np.argwhere(self.timestamps[self._last_ix:] >= t) + self._last_ix
        if len(idx) == 0:
            return -1.0
        ix = np.min(idx)
        self._last_ix = ix
        return self.timestamps[ix]

    def post_event(self, interface: Interface, t: float, y: np.array):
        self._last_ix += 1

class PeriodicTimeEvent(TimeEvent):
    """
    The default :class:`~solver.events.Event` class for periodic timestamped events.
    """

    def __init__(self, id: str, period: float, is_external: bool = False):
        self.id = id
        self._is_external = is_external
        self.period = period
        self.t_next_event = 0.0
        self._trigger = False

    def get_next_event_time(self, interface: Interface, t: float):
        return self.t_next_event

    def post_event(self, interface: Interface, t: float, y: np.array):
        self.t_next_event += self.period

    def reset(self):
        self.t_next_event = 0
        self.clear()

class StateEvent(Event):
    def __init__(self, id: str, is_external: bool = False):
        self.id = id
        self._is_external = is_external
        self._trigger = False

    def get_event_results(self, interface: Interface, t: float, y: np.array) -> float:
        """Function called to find events. Used together with event directions to determine if an event occured.

        :param interface: the model interface
        :type interface: :class:`~solver.interface.Interface`
        :param t: time
        :type t: float
        :param y: current solver and model states in numpy format
        :type y: :class:`numpy.ndarray`

        :return: value of the event function f(z(t)). The triggered event is found using a \
        bisection method, if the previous value has a different sign, and the event directions matches.
        :rtype: :class:`numpy.ndarray`
        """
        raise NotImplementedError

    def get_event_directions(self) -> int:
        """
        The event direction that determines if the event is triggered. If -1 then the event is triggered if the previous
        value was positive, and the current value is negative, and vice verse.
        :return: -1 or +1
        """
        raise NotImplementedError

    def post_event(self, interface: Interface, t: float, y: np.array):
        pass

    def locate_event(self, interface: Interface, event_tolerance: float, imax: int, t_previous, y_previous, t, y,
                    roller, order):
        """
        An bi-section iteration method for determining when an event takes place

        :param interface: The :class:`~solver.interface.Interface`
        :param event_tolerance: a tolerance parameter
        :param imax: maximum number of iterations (currently unused)
        :param t_previous: last converged time
        :param y_previous: last converged states
        :param t: current time
        :param y: current states
        :param roller: a vector containing up to :param order: number of last states
        :param order: the order of the roller
        :return:
        """
        def sol(t, t_r, y_r):
            """
            Interpolation using up to :param order: number of last values for time and states
            :param t: sought time
            :param t_r: current time
            :param y_r: current state
            :return:
            """
            yi = np.zeros(len(y))
            tv = np.append(roller[1][0:order], t_r)
            yv = np.append(roller[2][0:order], y_r)
            yv = yv.reshape(order + 1, len(y)).T
            for i, yvi in enumerate(yv):
                yi[i] = np.interp(t, tv, yvi)
            return yi

        t_l = t_previous
        y_l = y_previous
        e_l = self.get_event_results(interface, t_l, y_l)
        t_r = t
        y_r = y
        e_r = self.get_event_results(interface, t_r, y_r)
        status = 0
        if np.sign(e_l) == np.sign(e_r):
            return status, t, y
        i = 0
        t_m = (t_l + t_r) / 2
        y_m = sol(t_m, t, y)

        while status == 0:  # bisection method
            e_m = self.get_event_results(interface, t_m, y_m)
            if np.sign(e_l) != np.sign(e_m):
                t_r = t_m
            elif np.sign(e_r) != np.sign(e_m):
                t_l = t_m
            if abs(e_m) < event_tolerance or abs(t_l - t_r) < event_tolerance:
                status = 1
            if i > imax:
                raise ValueError("maximum iterations reached")
                #status = -1
            t_m = (t_l + t_r) / 2
            y_m = sol(t_m, t, y)
            i += 1

        return status, t_r, sol(t_r, t, y)

@event
class MockStateEvent(StateEvent):

    def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
        return y

    def get_event_results(self, interface: Interface, t: float, y: np.array) -> float:
        return 1.0

    def get_event_directions(self):
        return 0

@event
class MockTimeEvent(TimeEvent):
    def __init__(self, id: str, is_external: bool):
        self.id = id
        self._is_external = is_external
        self._trigger = False

    def run_event_action(self, interface: Interface, t: float, y: np.array) -> np.array:
        return y

    def get_next_event_time(self, interface: Interface, t: float) -> float:
        return -1.0