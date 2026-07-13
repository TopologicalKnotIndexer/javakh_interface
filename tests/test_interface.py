import importlib
import sys
from types import ModuleType
import unittest


backend = ModuleType("cppkh_interface")
backend.calls = []


def record(name, result):
    def function(*args, **kwargs):
        backend.calls.append((name, args, kwargs))
        return result
    return function


backend.solve_khovanov = record("one", "single-result")
backend.solve_many_khovanov = record("many", ["a", "b"])
backend.compute_signed_variants = record("signed", ["x", "y"])
sys.modules["cppkh_interface"] = backend

import javakh_interface


class InterfaceTests(unittest.TestCase):
    def setUp(self):
        backend.calls.clear()

    def test_single_call_preserves_historical_options(self):
        pd_code = [[1, 1, 2, 2]]
        result = javakh_interface.solve_khovanov(
            pd_code,
            encoding="utf-8",
            de_r1=False,
            de_k8=False,
            show_real_pdcode=True,
        )
        self.assertEqual(result, "single-result")
        self.assertEqual(
            backend.calls,
            [
                (
                    "one",
                    (pd_code,),
                    {
                        "encoding": "utf-8",
                        "de_r1": False,
                        "de_k8": False,
                        "show_real_pdcode": True,
                    },
                )
            ],
        )

    def test_batch_and_signed_calls_are_forwarded_exactly(self):
        diagrams = [[[1, 1, 2, 2]], []]
        self.assertEqual(
            javakh_interface.solve_many_khovanov(diagrams, threads=3), ["a", "b"]
        )
        signs = [[1], [-1]]
        self.assertEqual(
            javakh_interface.solve_signed_variants(diagrams[0], signs), ["x", "y"]
        )
        self.assertEqual(backend.calls[0][0], "many")
        self.assertEqual(backend.calls[0][2]["threads"], 3)
        self.assertEqual(backend.calls[1], ("signed", (diagrams[0], signs), {}))


if __name__ == "__main__":
    unittest.main()
