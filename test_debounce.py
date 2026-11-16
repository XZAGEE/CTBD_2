
import time
from debounce import Debounce

def test_basic_debounce():
    debounce = Debounce(delayMs=200)
    results = []
    fn = debounce.debounce(lambda: results.append("called"))
    fn()
    time.sleep(0.05)
    fn()
    time.sleep(0.05)
    fn()
    time.sleep(0.3)
    assert results == ["called"]

def test_leading_true():
    debounce = Debounce(delayMs=200, leading=True, trailing=False)
    results = []
    fn = debounce.debounce(lambda: results.append("called"))
    fn()
    fn()
    fn()
    assert len(results) == 1
    time.sleep(0.3)
    fn()
    assert len(results) == 2
    debounce.dispose()

def test_trailing_true():
    debounce = Debounce(delayMs=200, leading=False, trailing=True)
    results = []
    fn = debounce.debounce(lambda value: results.append(value))
    fn(1)
    fn(2)
    fn(3)
    assert results == []
    time.sleep(0.3)
    assert results == [3]
    debounce.dispose()

def test_leading_and_trailing():
    debounce = Debounce(delayMs=200, leading=True, trailing=True)
    results = []
    fn = debounce.debounce(lambda value: results.append(value))
    fn(1)
    assert results == [1]
    fn(2)
    fn(3)
    time.sleep(0.3)
    assert results == [1, 3]
    debounce.dispose()

def test_dispose_cancels_timer():
    debounce = Debounce(delayMs=200)
    results = []
    fn = debounce.debounce(lambda: results.append("called"))
    fn()
    debounce.dispose()
    time.sleep(0.3)
    assert results == []

def test_no_calls_after_dispose():
    debounce = Debounce(delayMs=200)
    results = []
    fn = debounce.debounce(lambda: results.append("called"))
    debounce.dispose()
    fn()
    time.sleep(0.3)
    assert results == []

def test_leading_and_trailing_single_call():
    debounce = Debounce(delayMs=200, leading=True, trailing=True)
    results = []
    fn = debounce.debounce(lambda: results.append("called"))
    fn()
    assert results == ["called"]
    time.sleep(0.3)
    assert results == ["called"]
    debounce.dispose()


def test_trailing_false():
    debounce = Debounce(delayMs=200, leading=False, trailing=False)
    results = []
    fn = debounce.debounce(lambda: results.append("called"))
    fn()
    fn()
    time.sleep(0.3)
    assert results == []
    debounce.dispose()

def test_arguments_and_kwargs():
    debounce = Debounce(delayMs=200)
    results = []
    def example_fn(name, age=None):
        results.append((name, age))
    fn = debounce.debounce(example_fn)
    fn("Yurii", age=20)
    time.sleep(0.3)
    assert results == [("Yurii", 20)]
    debounce.dispose()
