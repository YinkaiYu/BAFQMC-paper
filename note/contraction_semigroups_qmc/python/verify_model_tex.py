#!/usr/bin/env python3
"""Cross-check the B05, B13, and F04 model formulas against their verifier.

The note keeps the physical time step and Hubbard--Stratonovich amplitudes
explicit.  ``verify_model_slices.py`` sets the time step to one and absorbs
``sqrt(Delta tau U) phi`` into its variable ``field``.  Subject to this
normalization, this script checks the Pauli factors and signs term by term.

No TeX engine is involved.  The labeled equations are read directly from the
source, while Python's abstract syntax tree checks the symbolic constructions
used by the numerical verifier.  The verifier is then executed in memory, so
this command creates no result files.
"""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
import importlib.util
from pathlib import Path
import re
import sys
from types import ModuleType


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TEX = REPO_ROOT / "note" / "ContractionSemigroupsQMC.tex"
DEFAULT_MODEL_SCRIPT = Path(__file__).with_name("verify_model_slices.py")


@dataclass(frozen=True)
class ModelContract:
    identifier: str
    title: str
    labeled_equations: dict[str, str]
    required_fragments: tuple[tuple[str, str], ...]
    python_assignments: dict[str, str]
    expected_signs: tuple[int, int, int, int, int]


MODEL_CONTRACTS = (
    ModelContract(
        identifier="B05",
        title="frustrated plaquette-current interactions",
        labeled_equations={
            "eq:B05_model": r"""
                H_{\rm B05}=\sum_{ij}b_i^+E_{ij}b_j
                +\frac12\sum_p U_p\hat{\mathcal J}_p^2,
                \qquad U_p>0,
            """,
            "eq:B05_HS": r"""
                \ee^{-\frac12\Delta\tau U_p\hat{\mathcal J}_p^2}
                =\int\frac{d\phi_p}{\sqrt{2\pi}}\,
                \ee^{-\phi_p^2/2}
                \ee^{\ii\sqrt{\Delta\tau U_p}\,\phi_p\hat{\mathcal J}_p}.
            """,
            "eq:B05_slices": r"""
                A_{\rm cone}&=-\Delta\tau\,\sigma_z^{({\rm N})}\otimes E,\notag\\
                A_{\rm group}&=\sum_p\sqrt{\Delta\tau U_p}\,\phi_p
                I_2^{({\rm N})}\otimes R_p.
            """,
            "eq:B05_contraction": r"""
                \eta A_{\rm cone}+A_{\rm cone}^\dagger\eta
                =-2\Delta\tau I_2^{({\rm N})}\otimes E<0,
                \qquad
                \eta A_{\rm group}+A_{\rm group}^\dagger\eta=0.
            """,
        },
        required_fragments=(
            ("positive symmetric hopping", r"E=E^\trans>0"),
            (
                "real antisymmetric circulation matrix",
                r"\overline{R_p}=R_p,\qquad R_p^\trans=-R_p",
            ),
            (
                "circulation operator",
                r"\hat{\mathcal J}_p=-\ii\sum_{ij}b_i^+(R_p)_{ij}b_j",
            ),
            ("J1", r"J_1=I_2^{({\rm N})}"),
            ("J2", r"J_2=\sigma_x^{({\rm N})}"),
            ("eta", r"\eta=\sigma_z^{({\rm N})}"),
        ),
        python_assignments={
            "site_identity": "np.eye(2)",
            "energy": "np.diag([2.0, 3.0])",
            "circulation": "np.array([[0.0, 1.0], [-1.0, 0.0]])",
            "g": "kron(-Y, site_identity)",
            "first": "kron(I2, site_identity)",
            "second": "kron(X, site_identity)",
            "eta": "kron(Z, site_identity)",
            "cone": "-kron(Z, energy)",
            "group": "field * kron(I2, circulation)",
        },
        expected_signs=(1, 1, -1, 1, 1),
    ),
    ModelContract(
        identifier="B13",
        title="paired two-component bosons",
        labeled_equations={
            "eq:B13_model": r"""
                H_{\rm B13}={}&
                \sum_{ij}\sum_{s,s'=\uparrow,\downarrow}
                b_{is}^+\left[\delta_{ss'}E_{ij}
                +(\ii\sigma_y)_{ss'}R_{ij}\right]b_{js'}
                +\frac12\sum_{s=\uparrow,\downarrow}\sum_{ij}\Delta_{ij}
                \bigl(b_{is}^+b_{js}^++b_{is}b_{js}\bigr)\notag\\*
                &+\frac12\sum_\alpha U_\alpha\hat Q_\alpha^2,
                \qquad U_\alpha>0.
            """,
            "eq:B13_slices": r"""
                A_{\rm cone}={}&-\Delta\tau\bigl[
                \sigma_z^{({\rm N})}\otimes I_2^{({\rm f})}\otimes E
                +\sigma_z^{({\rm N})}\otimes(\ii\sigma_y)^{({\rm f})}\otimes R
                +(\ii\sigma_y)^{({\rm N})}\otimes I_2^{({\rm f})}\otimes\Delta\bigr],\notag\\*
                A_{\rm group}={}&\ii\sum_\alpha\sqrt{\Delta\tau U_\alpha}\,\phi_\alpha
                \sigma_z^{({\rm N})}\otimes\sigma_z^{({\rm f})}\otimes F_\alpha.
            """,
            "eq:B13_contraction": r"""
                \eta A_{\rm cone}+A_{\rm cone}^\dagger\eta
                =-2\Delta\tau
                \left[I_2^{({\rm N})}\otimes I_2^{({\rm f})}\otimes E
                +I_2^{({\rm N})}\otimes(\ii\sigma_y)^{({\rm f})}\otimes R
                +\sigma_x^{({\rm N})}\otimes I_2^{({\rm f})}\otimes\Delta\right].
            """,
            "eq:B13_block_condition": r"""
                \begin{pmatrix}
                I_2^{({\rm f})}\otimes E+(\ii\sigma_y)^{({\rm f})}\otimes R
                &I_2^{({\rm f})}\otimes\Delta\\
                I_2^{({\rm f})}\otimes\Delta
                &I_2^{({\rm f})}\otimes E+(\ii\sigma_y)^{({\rm f})}\otimes R
                \end{pmatrix}>0.
            """,
        },
        required_fragments=(
            ("symmetric energy", r"E=E^\trans"),
            ("symmetric pairing", r"\Delta=\Delta^\trans"),
            ("symmetric field matrices", r"F_\alpha=F_\alpha^\trans"),
            ("antisymmetric circulation", r"R^\trans=-R"),
            (
                "relative-density operator",
                r"\hat Q_\alpha=\sum_{ij}(F_\alpha)_{ij}"
                r"\bigl(b_{i\uparrow}^+b_{j\uparrow}"
                r"-b_{i\downarrow}^+b_{j\downarrow}\bigr)",
            ),
            (
                "J1, J2, and eta",
                r"J_1=I_2^{({\rm N})}\otimes(\ii\sigma_y)^{({\rm f})},"
                r"J_2=\sigma_x^{({\rm N})}\otimes I_2^{({\rm f})},"
                r"\eta=\sigma_z^{({\rm N})}\otimes I_2^{({\rm f})}",
            ),
        ),
        python_assignments={
            "site_identity": "np.eye(2)",
            "energy": "4.0 * site_identity",
            "circulation": "np.array([[0.0, 1.0], [-1.0, 0.0]])",
            "pairing": "site_identity",
            "field_matrix": "np.diag([1.0, 2.0])",
            "g": "kron(-Y, I2, site_identity)",
            "first": "kron(I2, Y, site_identity)",
            "second": "kron(X, I2, site_identity)",
            "eta": "kron(Z, I2, site_identity)",
            "cone": "-(kron(Z, I2, energy) + kron(Z, Y, circulation) + "
            "kron(Y, I2, pairing))",
            "block": "np.block([[kron(I2, energy) + kron(Y, circulation), "
            "kron(I2, pairing)], [kron(I2, pairing), "
            "kron(I2, energy) + kron(Y, circulation)]])",
            "group": "1j * field * kron(Z, Z, field_matrix)",
        },
        expected_signs=(1, -1, -1, 1, 1),
    ),
    ModelContract(
        identifier="F04",
        title="an interacting two-component superconductor",
        labeled_equations={
            "eq:F04_model": r"""
                H_{\rm F04}={}&
                \sum_{s=\uparrow,\downarrow}\sum_{ij}c_{is}^+K_{ij}c_{js}
                +\sum_{ij}T_{ij}
                \bigl(c_{i\uparrow}^+c_{j\downarrow}
                +c_{i\downarrow}^+c_{j\uparrow}\bigr)
                +\ii\sum_{ij}D_{ij}
                \bigl(c_{i\uparrow}c_{j\downarrow}
                +c_{i\uparrow}^+c_{j\downarrow}^+\bigr)\notag\\
                &+\frac12\sum_\alpha U_\alpha\hat Q_\alpha^2,
                \qquad U_\alpha>0.
            """,
            "eq:F04_slices": r"""
                A_{\rm group}={}&-\Delta\tau\,
                \sigma_z^{({\rm N})}\otimes I_2^{({\rm f})}\otimes K
                +\ii\sum_\alpha\sqrt{\Delta\tau U_\alpha}\,\phi_\alpha
                \sigma_z^{({\rm N})}\otimes\sigma_z^{({\rm f})}\otimes F_\alpha,
                \notag\\
                A_{\rm cone}={}&\Delta\tau\,
                \sigma_x^{({\rm N})}\otimes\sigma_y^{({\rm f})}\otimes D
                -\Delta\tau\,\sigma_z^{({\rm N})}\otimes\sigma_x^{({\rm f})}\otimes T.
            """,
            "eq:F04_contraction": r"""
                \eta A_{\rm group}+A_{\rm group}^\dagger\eta=0,
                \qquad
                \eta A_{\rm cone}+A_{\rm cone}^\dagger\eta
                =-2\Delta\tau\left[
                I_4\otimes D
                +\sigma_y^{({\rm N})}\otimes\sigma_z^{({\rm f})}\otimes T
                \right]<0.
            """,
            "eq:F04_matrix_condition": r"""
                D+T>0,\qquad D-T>0.
            """,
        },
        required_fragments=(
            ("symmetric hopping", r"K=K^\trans"),
            ("positive symmetric pairing", r"D=D^\trans>0"),
            ("symmetric flavor conversion", r"T=T^\trans"),
            ("symmetric field matrices", r"F_\alpha=F_\alpha^\trans"),
            (
                "relative-density operator",
                r"\hat Q_\alpha=\sum_{ij}(F_\alpha)_{ij}"
                r"\bigl(c_{i\uparrow}^+c_{j\uparrow}"
                r"-c_{i\downarrow}^+c_{j\downarrow}\bigr)",
            ),
            (
                "J1, J2, and eta",
                r"J_1=I_2^{({\rm N})}\otimes\sigma_x^{({\rm f})},"
                r"J_2=I_2^{({\rm N})}\otimes(\ii\sigma_y)^{({\rm f})},"
                r"\eta=-\sigma_x^{({\rm N})}\otimes\sigma_y^{({\rm f})}",
            ),
        ),
        python_assignments={
            "site_identity": "np.eye(2)",
            "hopping": "np.diag([1.0, 2.0])",
            "pairing": "4.0 * site_identity",
            "conversion": "np.diag([1.0, -1.0])",
            "field_matrix": "np.diag([1.0, 2.0])",
            "g": "kron(X, I2, site_identity)",
            "first": "kron(I2, X, site_identity)",
            "second": "kron(I2, Y, site_identity)",
            "eta": "1j * second @ g",
            "cone": "kron(X, SIGMA_Y, pairing) - kron(Z, X, conversion)",
            "group": "-kron(Z, I2, hopping) + 1j * field * "
            "kron(Z, Z, field_matrix)",
        },
        expected_signs=(1, 1, 1, -1, -1),
    ),
)


def remove_tex_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        match = re.search(r"(?<!\\)%", line)
        lines.append(line[: match.start()] if match else line)
    return "\n".join(lines)


def normalize_tex(text: str) -> str:
    text = remove_tex_comments(text)
    text = re.sub(r"\\label\{[^{}]+\}", "", text)
    for command in (
        r"\notag",
        r"\qquad",
        r"\quad",
        r"\bigl",
        r"\bigr",
        r"\left",
        r"\right",
        r"\,",
        r"\!",
        r"\;",
        r"\:",
    ):
        text = text.replace(command, "")
    text = text.replace("&", "")
    text = text.replace(r"\\*", "")
    text = text.replace(r"\\", "")
    return re.sub(r"\s+", "", text)


def extract_model_sections(text: str) -> dict[str, tuple[str, str]]:
    pattern = re.compile(r"\\subsection\*\{([BF]\d\d):\s*([^{}]+)\}")
    starts = list(pattern.finditer(text))
    sections: dict[str, tuple[str, str]] = {}
    for index, match in enumerate(starts):
        identifier = match.group(1)
        if identifier not in {contract.identifier for contract in MODEL_CONTRACTS}:
            continue
        if identifier in sections:
            raise AssertionError(f"TeX contains duplicate {identifier} model sections")
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        sections[identifier] = (match.group(2).strip(), text[match.end() : end])
    expected = {contract.identifier for contract in MODEL_CONTRACTS}
    if set(sections) != expected:
        missing = sorted(expected - set(sections))
        extra = sorted(set(sections) - expected)
        raise AssertionError(
            f"TeX model-section mismatch; missing={missing}, unexpected={extra}"
        )
    return sections


def extract_labeled_equation(section: str, label: str, identifier: str) -> str:
    marker = rf"\label{{{label}}}"
    occurrences = [match.start() for match in re.finditer(re.escape(marker), section)]
    if len(occurrences) != 1:
        raise AssertionError(
            f"{identifier}: expected one {marker}, found {len(occurrences)}"
        )
    label_position = occurrences[0]
    begins = list(
        re.finditer(r"\\begin\{(equation|align)\}", section[:label_position])
    )
    if not begins:
        raise AssertionError(f"{identifier}: cannot find environment for {marker}")
    begin = begins[-1]
    environment = begin.group(1)
    end = re.search(
        rf"\\end\{{{re.escape(environment)}\}}", section[label_position:]
    )
    if end is None:
        raise AssertionError(
            f"{identifier}: missing end of {environment} containing {marker}"
        )
    return section[begin.end() : label_position + end.start()]


def verify_tex_contract(text: str) -> None:
    sections = extract_model_sections(text)
    for contract in MODEL_CONTRACTS:
        actual_title, section = sections[contract.identifier]
        if actual_title != contract.title:
            raise AssertionError(
                f"{contract.identifier}: section title drifted; expected "
                f"{contract.title!r}, found {actual_title!r}"
            )
        normalized_section = normalize_tex(section)
        for description, fragment in contract.required_fragments:
            if normalize_tex(fragment) not in normalized_section:
                raise AssertionError(
                    f"{contract.identifier}: TeX {description} does not match the "
                    "model-verifier contract"
                )
        for label, expected in contract.labeled_equations.items():
            actual = extract_labeled_equation(section, label, contract.identifier)
            if normalize_tex(actual) != normalize_tex(expected):
                raise AssertionError(
                    f"{contract.identifier}: TeX equation {label} drifted\n"
                    f"expected: {normalize_tex(expected)}\n"
                    f"found:    {normalize_tex(actual)}"
                )


def canonical_ast(expression: str) -> str:
    return ast.dump(
        ast.parse(expression, mode="eval").body,
        annotate_fields=True,
        include_attributes=False,
    )


def function_definitions(tree: ast.Module) -> dict[str, ast.FunctionDef]:
    return {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }


def assigned_expressions(function: ast.FunctionDef) -> dict[str, list[ast.expr]]:
    assignments: dict[str, list[ast.expr]] = {}
    for node in ast.walk(function):
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if isinstance(target, ast.Name):
            assignments.setdefault(target.id, []).append(node.value)
    return assignments


def verify_check_slice_call(
    function: ast.FunctionDef, contract: ModelContract
) -> None:
    calls = [
        node
        for node in ast.walk(function)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "check_slice"
    ]
    if len(calls) != 1:
        raise AssertionError(
            f"{contract.identifier}: expected one check_slice call, found {len(calls)}"
        )
    keywords = {keyword.arg: keyword.value for keyword in calls[0].keywords}
    for keyword in ("model", "class_number", "expected_signs"):
        if keyword not in keywords:
            raise AssertionError(
                f"{contract.identifier}: check_slice is missing {keyword}"
            )
    model = ast.literal_eval(keywords["model"])
    class_number = ast.literal_eval(keywords["class_number"])
    signs = ast.literal_eval(keywords["expected_signs"])
    if model != contract.identifier or class_number != contract.identifier:
        raise AssertionError(
            f"{contract.identifier}: verifier case labels drifted; "
            f"model={model!r}, class_number={class_number!r}"
        )
    if signs != contract.expected_signs:
        raise AssertionError(
            f"{contract.identifier}: verifier five-relation signs drifted; "
            f"expected {contract.expected_signs}, found {signs}"
        )


def verify_python_contract(source: str) -> None:
    tree = ast.parse(source)
    functions = function_definitions(tree)
    for contract in MODEL_CONTRACTS:
        function_name = contract.identifier.lower() + "_rows"
        if function_name not in functions:
            raise AssertionError(
                f"verify_model_slices.py is missing {function_name}()"
            )
        function = functions[function_name]
        assignments = assigned_expressions(function)
        for name, expression in contract.python_assignments.items():
            found = assignments.get(name, [])
            if len(found) != 1:
                raise AssertionError(
                    f"{contract.identifier}: expected one verifier assignment to "
                    f"{name}, found {len(found)}"
                )
            actual = ast.dump(found[0], annotate_fields=True, include_attributes=False)
            expected = canonical_ast(expression)
            if actual != expected:
                raise AssertionError(
                    f"{contract.identifier}: verify_model_slices.py assignment "
                    f"{name} drifted; expected `{expression}`, found "
                    f"`{ast.unparse(found[0])}`"
                )
        verify_check_slice_call(function, contract)


def load_model_verifier(path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("_model_slice_verifier", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load model verifier from {path}")
    module = importlib.util.module_from_spec(spec)
    old_setting = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old_setting
    return module


def verify_numerical_checks(module: ModuleType) -> None:
    for contract in MODEL_CONTRACTS:
        function = getattr(module, contract.identifier.lower() + "_rows")
        rows = function()
        if len(rows) != 3:
            raise AssertionError(
                f"{contract.identifier}: expected three numerical field checks, "
                f"found {len(rows)}"
            )
        for row in rows:
            if row.get("model") != contract.identifier:
                raise AssertionError(
                    f"{contract.identifier}: numerical row has model={row.get('model')!r}"
                )
            if row.get("class_number") != contract.identifier:
                raise AssertionError(
                    f"{contract.identifier}: numerical row has "
                    f"class_number={row.get('class_number')!r}"
                )
            if float(row["maximum_contraction_eigenvalue"]) >= 0.0:
                raise AssertionError(
                    f"{contract.identifier}: numerical contraction margin is not negative"
                )
            margin = row.get("minimum_coefficient_margin", "")
            if contract.identifier in {"B13", "F04"} and float(margin) <= 0.0:
                raise AssertionError(
                    f"{contract.identifier}: numerical coefficient inequality failed"
                )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Cross-check the B05, B13, and F04 TeX formulas against "
            "verify_model_slices.py."
        )
    )
    parser.add_argument("--tex", type=Path, default=DEFAULT_TEX)
    parser.add_argument(
        "--model-script", type=Path, default=DEFAULT_MODEL_SCRIPT
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    tex_text = arguments.tex.read_text(encoding="utf-8")
    model_source = arguments.model_script.read_text(encoding="utf-8")
    verify_tex_contract(tex_text)
    verify_python_contract(model_source)
    verify_numerical_checks(load_model_verifier(arguments.model_script))
    print(
        "Verified the B05, B13, and F04 TeX formulas against "
        "verify_model_slices.py."
    )


if __name__ == "__main__":
    main()
