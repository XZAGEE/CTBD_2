
import threading


class Debounce:
    def __init__(self, delayMs, leading=False, trailing=True):
        self.delayMs = delayMs
        self.leading = leading
        self.trailing = trailing

        self.lock = threading.Lock()
        self.timers = set()
        self.disposed = False

    def debounce(self, fn):
        state = {
            "timer": None,
            "last_args": None,
            "last_kwargs": None,
            "generation": 0
        }

        def wrapper(*args, **kwargs):
            call_now = False

            with self.lock:
                if self.disposed:
                    return

                is_first = state["timer"] is None

                if is_first:
                    call_now = self.leading

                    if self.trailing and not self.leading:
                        state["last_args"] = args
                        state["last_kwargs"] = kwargs
                    else:
                        state["last_args"] = None
                        state["last_kwargs"] = None

                else:
                    if self.trailing:
                        state["last_args"] = args
                        state["last_kwargs"] = kwargs

                    old_timer = state["timer"]
                    old_timer.cancel()
                    self.timers.discard(old_timer)

                state["generation"] += 1
                generation = state["generation"]

                def finish():
                    call_args = None
                    call_kwargs = None

                    with self.lock:
                        if self.disposed:
                            return

                        if generation != state["generation"]:
                            return

                        current_timer = state["timer"]
                        if current_timer is not None:
                            self.timers.discard(current_timer)

                        state["timer"] = None

                        if self.trailing and state["last_args"] is not None:
                            call_args = state["last_args"]
                            call_kwargs = state["last_kwargs"]

                        state["last_args"] = None
                        state["last_kwargs"] = None

                    if call_args is not None:
                        fn(*call_args, **call_kwargs)

                timer = threading.Timer(
                    self.delayMs / 1000,
                    finish
                )

                timer.daemon = True
                state["timer"] = timer
                self.timers.add(timer)
                timer.start()

            if call_now:
                fn(*args, **kwargs)

        return wrapper

    def dispose(self):
        with self.lock:
            self.disposed = True

            for timer in self.timers:
                timer.cancel()

            self.timers.clear()
