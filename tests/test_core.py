"""Tests for Tonecheck."""
from src.core import Tonecheck
def test_init(): assert Tonecheck().get_stats()["ops"] == 0
def test_op(): c = Tonecheck(); c.detect(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Tonecheck(); [c.detect() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Tonecheck(); c.detect(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Tonecheck(); r = c.detect(); assert r["service"] == "tonecheck"
