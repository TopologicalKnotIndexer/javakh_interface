from typing import Optional

import cppkh_interface


def solve_khovanov(
    pd_code: list[list],
    encoding: Optional[str] = None,
    de_r1: bool = True,
    de_k8: bool = True,
    show_real_pdcode: bool = False,
) -> str:
    """Compute integral Khovanov homology using the corrected cppkh backend.

    The signature is intentionally compatible with javakh-interface 0.1.0.
    cppkh is a C++ port of the same integer JavaKh computation path and fixes
    the old backend's crossing-orientation handling.
    """
    return cppkh_interface.solve_khovanov(
        pd_code,
        encoding=encoding,
        de_r1=de_r1,
        de_k8=de_k8,
        show_real_pdcode=show_real_pdcode,
    )


def solve_many_khovanov(
    pd_codes,
    encoding: Optional[str] = None,
    de_r1: bool = True,
    de_k8: bool = True,
    show_real_pdcode: bool = False,
    threads: str | int = "auto",
) -> list[str]:
    """Compute several PD codes in one backend process."""
    return cppkh_interface.solve_many_khovanov(
        pd_codes,
        encoding=encoding,
        de_r1=de_r1,
        de_k8=de_k8,
        show_real_pdcode=show_real_pdcode,
        threads=threads,
    )


def solve_signed_variants(pd_code, signs: list[list[int]]) -> list[str]:
    """Compute explicit crossing-sign variants with the native backend."""
    return cppkh_interface.compute_signed_variants(pd_code, signs)
