# TRS 叙述顺序与正文重点调整

本轮延续此前的整合工作，diff 始终比较 1b207e7；高可见度文风继续以导师在 66c6cd4 中修改的摘要、Introduction 和 Concluding remarks 为参照。

## 本轮形成的文章结构

正文先陈述 Theorem 1。定理自然地先说粒子数守恒时的单个 Kramers TRS，再说一般 Nambu 二次演化；没有人为的分项标题。随后用共轭本征值配对解释机制，并保留原来的 eq:block_TRS 作为直观例子。含配对演化与周期表在这之后引入。

周期表只展示玻色子的 sign-free 和 sign-problem-possible 类别。正文对三个基本 TRS 类别作平衡介绍；{+,+,+} 的特殊性只出现在周期表说明和 Examples and applications。摘要和结论恢复对整个玻色子 TRS/RP 框架及受挫体系计算能力的强调。

补充材料 Sec. V 的顺序为：单 Kramers 的粒子数守恒证明、沿用 Secs. II–III 的 Nambu 记号、Kramers 类、Majorana 类、split-orthogonal 类、周期表其余类别，最后说明粒子数守恒时三个 Nambu 类都约化为单个 Kramers 对称性。原先的玻色—费米统一框架、费米权重证明和 Majorana-basis 对照已删除；统一使用 Ω、A、M、W 等文章已有记号。

Sec. VII 的 odd-parity 内容合并成一个 subsection，保留物理动机、flavor 反对称结构、TRS 排除证明、具体相互作用与 HS 分解、稳定条件及物理后果。等幅三角格子模型仍作为最简构造，同时说明实键幅 Δₚ(1,1/2,−1/2) 实现纯 pₓ pairing，并明确后面的色散公式属于等幅模型。

原有 benchmark 模型、两张数据图及全部数值参数保留，没有增加 benchmark。

## 判据关系及局部公式核对

补充材料新增了两个判据之间的直接联系：

- 对本文所用的 number-preserving reflection，Gaussian RP 中的 F 半正定条件和粒子数守恒共同强制 F=0；剩下的共轭双份结构属于单 Kramers 判据。
- 配对 benchmark 的共同反幺正映射仍然存在，但它们彼此对易，不能组成任何一个保护正性的 TRS 集合。因此正文准确表述为超出 TRS 判据的覆盖，而没有声称所有 TRS 都被破坏。

RP 的半群意义只保留正文结论中的一句展望和补充材料的一段说明，没有展开为独立研究主线。Canonical AFQMC 也保持为控制高占据涨落的未来方向，没有直接把 grand-canonical 正性当作投影权重的已证性质。

此外，修正了 RP 对称分块对应混合算符时的因子 2，并明确 Nambu 更新比包括标量变化 exp(δξ)，恒等更新同时要求 Δℓ=0 和 δξℓ=0。粒子数守恒约化中的 polar-decomposition 推导保留，以涵盖起初允许 Bogoliubov 混合的 TRS。

## 单独保留的延拓问题

独立核验发现一个同时满足现有 Majorana 与 RP 代数条件的两模例子，其收敛迹为正，但既定解析延拓在非收敛区有限且为负。按照本轮作者决定，文章暂时保留既定适用范围，下一轮再处理这个问题。因此，本轮的结构、排版和局部代数核对不等于配对延拓定理及完整周期表已经通过最终数学审计。

完整算符、TRS 矩阵、Bogoliubov 对角化、平方根分支分析、对现有证明的具体影响和复核程序见 [独立反例说明](2026-09-10_trs_branch_issue/README.md)。

## 验证与交付

- 已完成独立物理审读与首次读者审读，并落实本轮范围内的更正。
- WSL 中的局部核验覆盖 RP 混合块归一化、benchmark 的完整 Nambu 对称性、粒子数守恒的 polar reduction 和纯 pₓ 键幅。反例报告附带的独立复核程序通过 41 项矩阵检查，并重现收敛迹与负延拓值的差别。
- 正文和补充材料经仓库 WSL 构建入口编译，完整 PDF 为 33 页，正文在第 5 页结束。
- 已检查正文第 3–5 页以及补充材料 TRS、RP、配对模型和 benchmark 细节所在的第 21–33 页；公式、标题和段落均无溢出。
- 已更新 pdf/main.pdf 与 pdf/main-diff.pdf，后者严格以 1b207e7 为基准，并在展开输入时分别使用新旧版本的 SM.tex。仅在生成的 diff 文件中给新表格前加分页，解决增删标记引起的 REVTeX 浮动体警告；正式稿的排版设置没有改动。
- 正式稿没有未定义引用、重复标签或 overfull 警告。保留的提示均为原有的 REVTeX 默认字号、nameref 的 label 重定义、BibTeX 的 jnrlst 设置、内部 SM 条目的空年份，以及参考文献中 badness 1337 的轻微 underfull。diff 的增删标记另外产生三处轻微 underfull（1242、1077、1237），目视检查均可正常阅读。

本轮没有新增参考文献条目或修改文献信息字段。references.bib 只撤掉了一条已不再引用的 Pelissetto–Vicari 文献标题中的人工断词标记，恢复原始标题写法；原先核实过的 odd-parity 背景引文继续保留。
