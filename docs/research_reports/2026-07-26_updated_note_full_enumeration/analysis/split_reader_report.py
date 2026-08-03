#!/usr/bin/env python3
"""Split the complete report into faster MathJax-sized reading volumes."""

from __future__ import annotations

import copy
from pathlib import Path

from bs4 import BeautifulSoup, Tag


REPORT_DIR = Path(__file__).resolve().parents[1]
SOURCE_PATH = REPORT_DIR / "report_updated_note_full_enumeration_zh.html"
BRANCH_FRAGMENT_PATH = REPORT_DIR / "branch_sign_sampling_zh.fragment.html"
CASE12_FRAGMENT_PATH = REPORT_DIR / "case12_semigroups_zh.fragment.html"
DETERMINANT_SYMMETRY_FRAGMENT_PATH = (
    REPORT_DIR / "determinant_symmetry_groups_zh.fragment.html"
)
CANONICAL_ALGORITHM_FRAGMENT_PATH = (
    REPORT_DIR / "canonical_projector_algorithms_zh.fragment.html"
)
FINITE_T_CANONICAL_FRAGMENT_PATH = (
    REPORT_DIR / "canonical_afqmc_algorithm_zh.fragment.html"
)
HALF_POWER_SYMMETRY_TABLE_PATH = (
    REPORT_DIR / "half_power_symmetry_64_table.fragment.html"
)


def clone(tag: Tag) -> Tag:
    return copy.copy(tag)


def page_shell(source: BeautifulSoup, title: str) -> tuple[BeautifulSoup, Tag]:
    page = BeautifulSoup("<!doctype html><html><body><main></main></body></html>", "html.parser")
    page.html.insert(0, clone(source.head))
    page.title.string = title
    main = page.main
    main.append(clone(source.header))
    return page, main


def navigation(items: list[tuple[str, str]]) -> BeautifulSoup:
    links = "".join(f'<a href="{href}">{label}</a>' for href, label in items)
    return BeautifulSoup(
        f'<nav class="toc" aria-label="分卷导航">{links}</nav>', "html.parser"
    )


def write_page(path: Path, page: BeautifulSoup) -> None:
    rendered = "<!doctype html>\n" + str(page.html) + "\n"
    path.write_text(rendered, encoding="utf-8")


def build_index(source: BeautifulSoup) -> None:
    page, main = page_shell(
        source, "ToYinkaiYu-20260726 note 研究报告：分卷入口"
    )
    index_content = BeautifulSoup(
        r"""
        <section>
          <h2>分卷阅读入口</h2>
          <p class="lead">
            本入口将完整报告按阅读任务拆分，避免浏览器一次排版六千余行 HTML
            与全部 note 公式。建议先读第 0 卷，再按顺序阅读 note；研究结论、
            Octave 穷举、生成元结构和物理 Hamiltonian 集中在第 3 卷。
            单文件完整版仍保留，适合全文搜索。
          </p>
          <div class="summary-grid">
            <div class="summary-item established">
              <strong><a href="part_0_framework.html">第 0 卷：阅读框架</a></strong>
              从 AFQMC 时间片出发，说明 \(J_1,J_2\)、五条离散关系、
              maximal subgroup、invariant cone，以及 TRS/RP 与收缩半群内部条件
              三条证明路线的区别。
            </div>
            <div class="summary-item established">
              <strong><a href="part_1_note_01.html">第 1A--1D 卷：note 逐段讲解</a></strong>
              note 第 22--1824 行连续覆盖，共 42 个单元；每段完整原文之后
              紧跟公式补全、具体矩阵、物理解释和局部校核。
            </div>
            <div class="summary-item established">
              <strong><a href="part_2_physical_mapping.html">第 2 卷：物理对应</a></strong>
              把 note 的 \(J_1,J_2\) 对应到 main.tex 的 Kramers TRS、
              operator reflection positivity、reflection phase 与 paired benchmark。
            </div>
            <div class="summary-item established">
              <strong><a href="part_3_enumeration_models.html">第 3 卷：分类、生成元与模型讲义</a></strong>
              从解析判据与 Octave 算法依次讲到 64 类穷举，逐类展开
              \(A\) 的最终约束、maximal subgroup 与 invariant cone。
              每张类别卡片都就地给出一个厄米相互作用格点模型，并分开写明
              strict cone 非空时的收缩半群证明；只有 cone 为空时才补充
              时间反演对称性或更小无符号子群的判据。
            </div>
            <div class="summary-item established">
              <strong><a href="part_4_implications.html">第 4 卷：文章影响与结论</a></strong>
              对文章的修改建议、各结论的准确适用范围、最终结论、
              给合作者的建议回复和可复现文件索引。
            </div>
            <div class="summary-item established">
              <strong><a href="part_5_branch_sampling.html">独立算法卷：lifted double-cover 符号追踪</a></strong>
              用 \((M,\eta_U)\) lifted state 取代逐 proposal 的连续路径，
              推导 Gaussian cocycle、product tree、低秩 fast update
              与 sign/phase 重加权；旋转、squeezing 和 local ratio
              均有 Python/SciPy 与有限 Fock-space 检查。
            </div>
            <div class="summary-item established">
              <strong><a href="part_6_case12_semigroups.html">独立理论卷：Case 1/2 的半群证明</a></strong>
              分别建立 Kramers TRS 的乘法闭合结构和 RP 的
              reflected-square operators 在乘法下封闭；并逐块证明，
              全部 reflection-positive generators 不可能共同服从同一个
              固定 contraction metric，因而不能改写成固定 Nambu metric
              下的单向 contraction semigroup。
            </div>
            <div class="summary-item established">
              <strong><a href="part_7_determinant_symmetry_groups.html">独立理论卷：Gaussian AFQMC 权重的对称性正性</a></strong>
              从固定辅助场构型的 many-body trace 出发，先给出玻色、费米
              时间反演周期表，再解释共轭物理部分、Nambu 空间中的 Kramers
              简并、玻色三条全正对称性、含 pairing 模型与 64 类
              \(J_1,J_2\) 结论。
            </div>
            <div class="summary-item established">
              <strong><a href="part_8_canonical_projector_algorithms.html">独立算法卷：固定粒子数有限温与零温投影</a></strong>
              解释当前 \(iJ_2g\) 模型为何采用 fixed-\(N\)，给出
              grand-canonical 可行的统一收敛条件；随后完整推导有限温
              canonical character 算法，以及 BPQMC 使用的零温 rank-one
              projector、局域更新、测量与稳定化。
            </div>
            <div class="summary-item corrected">
              <strong><a href="report_updated_note_full_enumeration_zh.html">单文件完整版</a></strong>
              包含第 0--4 卷的 note 研究主报告，适合浏览器全文搜索；
              double-cover 采样与 Case 1/2 半群证明分别保留为独立卷。
            </div>
          </div>
        </section>
        """,
        "html.parser",
    )
    main.append(index_content.section)
    write_page(REPORT_DIR / "report_index.html", page)


def build_section_page(
    source: BeautifulSoup,
    filename: str,
    title: str,
    section_ids: list[str],
    nav_items: list[tuple[str, str]],
) -> None:
    page, main = page_shell(source, title)
    main.append(navigation(nav_items))
    for section_id in section_ids:
        section = source.find("section", id=section_id)
        if section is None:
            raise RuntimeError(f"Missing section {section_id}")
        main.append(clone(section))
    main.append(navigation(nav_items))
    write_page(REPORT_DIR / filename, page)


def build_note_pages(source: BeautifulSoup) -> None:
    note = source.find("section", id="note-walkthrough")
    if note is None:
        raise RuntimeError("Missing note walkthrough")
    articles = note.find_all("article", recursive=False)
    if len(articles) != 42:
        raise RuntimeError(f"Expected 42 note articles, found {len(articles)}")
    ranges = [(0, 11), (11, 21), (21, 32), (32, 42)]
    filenames = [f"part_1_note_0{index}.html" for index in range(1, 5)]
    for volume_index, ((start, end), filename) in enumerate(
        zip(ranges, filenames, strict=True), start=1
    ):
        page, main = page_shell(
            source,
            f"ToYinkaiYu-20260726 note 逐段讲解 {volume_index}/4",
        )
        nav_items = [
            ("report_index.html", "分卷入口"),
            ("part_0_framework.html", "第 0 卷：先读框架"),
        ]
        if volume_index > 1:
            nav_items.append((filenames[volume_index - 2], "上一卷 note"))
        if volume_index < 4:
            nav_items.append((filenames[volume_index], "下一卷 note"))
        else:
            nav_items.append(("part_2_physical_mapping.html", "下一卷：物理对应"))
        main.append(navigation(nav_items))
        new_section = page.new_tag("section", id=f"note-walkthrough-{volume_index}")
        heading = page.new_tag("h2")
        heading.string = f"1. note 原文与逐段讲解，第 {volume_index}/4 卷"
        new_section.append(heading)
        introduction = note.find("p", recursive=False)
        if introduction is not None:
            new_section.append(clone(introduction))
        for article in articles[start:end]:
            new_section.append(clone(article))
        main.append(new_section)
        main.append(navigation(nav_items))
        write_page(REPORT_DIR / filename, page)


def build_branch_page(source: BeautifulSoup) -> None:
    fragment = BeautifulSoup(
        BRANCH_FRAGMENT_PATH.read_text(encoding="utf-8"), "html.parser"
    )
    page = BeautifulSoup(
        "<!doctype html><html><body><main></main></body></html>", "html.parser"
    )
    page.html.insert(0, clone(source.head))
    page.title.string = "玻色 Gaussian AFQMC：用 (M, eta_U) 离散追踪符号"
    header = fragment.find("header", recursive=False)
    section = fragment.find("section", id="branch-sampling", recursive=False)
    if header is None or section is None:
        raise RuntimeError("Branch-sampling fragment needs one header and one section")
    nav_items = [
        ("report_index.html", "分卷入口"),
        ("part_4_implications.html", "返回 note 研究主报告"),
        ("part_6_case12_semigroups.html", "Case 1/2 半群证明"),
        (
            "report_updated_note_full_enumeration_zh.html",
            "主报告单文件完整版",
        ),
    ]
    page.main.append(clone(header))
    page.main.append(navigation(nav_items))
    page.main.append(clone(section))
    page.main.append(navigation(nav_items))
    write_page(REPORT_DIR / "part_5_branch_sampling.html", page)


def build_case12_page(source: BeautifulSoup) -> None:
    fragment = BeautifulSoup(
        CASE12_FRAGMENT_PATH.read_text(encoding="utf-8"), "html.parser"
    )
    page = BeautifulSoup(
        "<!doctype html><html><body><main></main></body></html>", "html.parser"
    )
    page.html.insert(0, clone(source.head))
    page.title.string = "玻色 Case 1/2：TRS、reflection positivity 与半群"
    header = fragment.find("header", recursive=False)
    section = fragment.find("section", id="case12-semigroups", recursive=False)
    if header is None or section is None:
        raise RuntimeError("Case-1/2 fragment needs one header and one section")
    nav_items = [
        ("report_index.html", "分卷入口"),
        ("part_2_physical_mapping.html", "返回物理对应卷"),
        ("part_5_branch_sampling.html", "double-cover 算法卷"),
        (
            "report_updated_note_full_enumeration_zh.html",
            "主报告单文件完整版",
        ),
    ]
    page.main.append(clone(header))
    page.main.append(navigation(nav_items))
    page.main.append(clone(section))
    page.main.append(navigation(nav_items))
    write_page(REPORT_DIR / "part_6_case12_semigroups.html", page)


def build_determinant_symmetry_page(source: BeautifulSoup) -> None:
    fragment_text = DETERMINANT_SYMMETRY_FRAGMENT_PATH.read_text(encoding="utf-8")
    table_text = HALF_POWER_SYMMETRY_TABLE_PATH.read_text(encoding="utf-8")
    marker = "{{HALF_POWER_64_TABLE}}"
    if fragment_text.count(marker) != 1:
        raise RuntimeError("Symmetry fragment needs exactly one 64-class table marker")
    fragment = BeautifulSoup(fragment_text.replace(marker, table_text), "html.parser")
    page = BeautifulSoup(
        "<!doctype html><html><body><main></main></body></html>", "html.parser"
    )
    page.html.insert(0, clone(source.head))
    page.title.string = "Gaussian AFQMC 权重的对称性正性"
    header = fragment.find("header", recursive=False)
    section_ids = [
        "configuration-weight-and-trs",
        "two-basic-time-reversal-classes",
        "three-or-more-time-reversals",
        "paired-physical-models",
        "j-relations-symmetry-weight",
        "symmetry-positivity-conclusion",
        "symmetry-positivity-references",
    ]
    sections = [
        fragment.find("section", id=section_id, recursive=False)
        for section_id in section_ids
    ]
    if header is None or any(section is None for section in sections):
        raise RuntimeError(
            "Symmetry-positivity fragment is missing an ordered section"
        )
    nav_items = [
        ("report_index.html", "分卷入口"),
        ("part_3_enumeration_models.html", "返回 64 类生成元讲义"),
        ("part_5_branch_sampling.html", "double-cover 算法卷"),
        ("part_6_case12_semigroups.html", "Case 1/2 半群证明"),
    ]
    page.main.append(clone(header))
    page.main.append(navigation(nav_items))
    for section in sections:
        assert section is not None
        page.main.append(clone(section))
    page.main.append(navigation(nav_items))
    write_page(REPORT_DIR / "part_7_determinant_symmetry_groups.html", page)


def build_canonical_algorithm_page(source: BeautifulSoup) -> None:
    fragment_text = CANONICAL_ALGORITHM_FRAGMENT_PATH.read_text(encoding="utf-8")
    finite_t_text = FINITE_T_CANONICAL_FRAGMENT_PATH.read_text(encoding="utf-8")
    marker = "{{FINITE_T_CANONICAL}}"
    if fragment_text.count(marker) != 1:
        raise RuntimeError("Canonical algorithm fragment needs one finite-T marker")
    finite_t_text = finite_t_text.replace("6.8.", "2.")
    finite_t_text = finite_t_text.replace("<h4>", "<h3>").replace("</h4>", "</h3>")
    fragment = BeautifulSoup(
        fragment_text.replace(marker, finite_t_text), "html.parser"
    )
    page = BeautifulSoup(
        "<!doctype html><html><body><main></main></body></html>", "html.parser"
    )
    page.html.insert(0, clone(source.head))
    page.title.string = "固定粒子数玻色 AFQMC：有限温与零温投影算法"
    header = fragment.find("header", recursive=False)
    section = fragment.find(
        "section", id="canonical-projector-algorithms", recursive=False
    )
    if header is None or section is None:
        raise RuntimeError(
            "Canonical algorithm fragment needs one header and one section"
        )
    nav_items = [
        ("report_index.html", "分卷入口"),
        ("part_3_enumeration_models.html", "返回 64 类生成元讲义"),
        ("part_7_determinant_symmetry_groups.html", "对称性正性理论卷"),
    ]
    page.main.append(clone(header))
    page.main.append(navigation(nav_items))
    page.main.append(clone(section))
    page.main.append(navigation(nav_items))
    write_page(REPORT_DIR / "part_8_canonical_projector_algorithms.html", page)


def main() -> None:
    source = BeautifulSoup(SOURCE_PATH.read_text(encoding="utf-8"), "html.parser")
    build_index(source)
    common_index = ("report_index.html", "分卷入口")
    build_section_page(
        source,
        "part_0_framework.html",
        "ToYinkaiYu-20260726 note：阅读框架",
        ["reading-framework"],
        [common_index, ("part_1_note_01.html", "下一卷：note 逐段讲解")],
    )
    build_note_pages(source)
    build_section_page(
        source,
        "part_2_physical_mapping.html",
        "ToYinkaiYu-20260726 note：物理对应与合作者消息",
        ["physical-map", "message"],
        [
            common_index,
            ("part_1_note_04.html", "上一卷：note 讲解"),
            ("part_3_enumeration_models.html", "下一卷：分类与模型讲义"),
        ],
    )
    build_section_page(
        source,
        "part_3_enumeration_models.html",
        "ToYinkaiYu-20260726 note：分类、生成元与物理模型讲义",
        ["question", "derivation", "enumeration", "audit-note", "fermion-weight"],
        [
            common_index,
            ("part_2_physical_mapping.html", "上一卷：物理对应"),
            ("part_4_implications.html", "下一卷：文章影响与结论"),
            ("part_7_determinant_symmetry_groups.html", "Gaussian 权重的对称性正性"),
            ("part_8_canonical_projector_algorithms.html", "固定粒子数算法"),
        ],
    )
    build_section_page(
        source,
        "part_4_implications.html",
        "ToYinkaiYu-20260726 note：文章影响与结论",
        ["paper", "conclusion", "reproduce"],
        [
            common_index,
            ("part_3_enumeration_models.html", "上一卷：分类与模型讲义"),
            ("part_5_branch_sampling.html", "独立算法卷：符号追踪与采样"),
            ("part_6_case12_semigroups.html", "独立理论卷：Case 1/2 半群"),
            ("part_7_determinant_symmetry_groups.html", "独立理论卷：Gaussian 权重的对称性正性"),
            ("part_8_canonical_projector_algorithms.html", "独立算法卷：固定粒子数"),
            (
                "report_updated_note_full_enumeration_zh.html",
                "单文件完整版",
            ),
        ],
    )
    build_branch_page(source)
    build_case12_page(source)
    build_determinant_symmetry_page(source)
    build_canonical_algorithm_page(source)
    print("Wrote report_index.html and 12 split report volumes.")


if __name__ == "__main__":
    main()
