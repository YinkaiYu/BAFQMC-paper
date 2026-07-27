"""Reader-facing physical models for the sixteen strict matrix classes."""

from __future__ import annotations


MODEL_CATALOG: dict[str, dict[str, str]] = {
    "B-J2g-s1-q1+": {
        "field_word": "iY",
        "title": "单模 pair-quadrature 相互作用振子",
        "body": r"""
        <p>
        取一个普通玻色模 \(a\)，并定义 Hermitian pair quadrature
        \[
          \hat O=\frac12\left(a^{+2}+a^2\right).
        \]
        一个非平凡且有界下的模型是
        \[
          \hat H=\kappa\,a^+a+\frac U2\hat O^2,
          \qquad \kappa>0,\quad U>0.
        \]
        它是带 quartic pair-quadrature stiffness 的 parametric oscillator，
        可用于研究 squeezing、双光子涨落与 parity-resolved transitions。
        </p>
        <p>
        Repulsive-square Gaussian HS 分解给出
        \[
          e^{-\Delta\tau U\hat O^2/2}
          \propto\int d\phi\,e^{-\phi^2/2}
          e^{\,i\sqrt{\Delta\tau U}\phi\hat O}.
        \]
        在本节的 Nambu convention 中
        \[
          \hat h(-\sigma_z)=-a^+a-\frac12,\qquad
          \hat h(i\,i\sigma_y)=i\hat O.
        \]
        因而时间片中的两个生成元是
        \[
          A_0=-\kappa\Delta\tau\,\sigma_z,\qquad
          A_{\rm HS}(\phi)=
          \sqrt{\Delta\tau U}\phi\,i(i\sigma_y).
        \]
        第一项正是 strict witness \(-\eta\)，第二项正是本类
        maximal subgroup 的 \(iY\) direction，所以
        \[
          \eta A_0+A_0^\dagger\eta=-2\kappa\Delta\tau I<0,\qquad
          \eta A_{\rm HS}+A_{\rm HS}^\dagger\eta=0
        \]
        对所有实 \(\phi\) 同时成立。这里不是只找到一个抽象 matrix：
        HS field、quartic interaction 与物理玻色算符已经逐项对应。
        </p>
        """,
    },
    "B-J2g-s1-q1-": {
        "field_word": "IY",
        "title": "双模 bond-current 相互作用振子",
        "body": r"""
        <p>
        取两个玻色模 \(a_1,a_2\)，定义 Hermitian bond current
        \[
          \hat j=-i(a_1^+a_2-a_2^+a_1),
          \qquad
          \hat H=\kappa(\hat n_1+\hat n_2)+\frac U2\hat j^2 ,
          \qquad \kappa>0,\quad U>0 .
        \]
        这是带 current-current interaction 的 bosonic dimer。推广到
        plaquette 或 frustrated lattice 后，可研究 orbital-current
        correlations 与 chiral ordering。
        </p>
        <p>
        这里
        \[
          \hat h(I_2\otimes i\sigma_y)
          =a_1^+a_2-a_2^+a_1=i\hat j .
        \]
        所以同一个 repulsive-square HS identity 产生两个生成元
        \[
          A_0=-\kappa\Delta\tau\,\sigma_z\otimes I_2,\qquad
          A_{\rm HS}(\phi)=
          \sqrt{\Delta\tau U}\phi\,I_2\otimes(i\sigma_y) .
        \]
        \(IY\) 在本类的 maximal-subgroup basis 中，而
        \(-ZI=-\eta\) 在 strict cone 内。\(J_1=ZY\) 对两个生成元
        分别满足复共轭约束，且
        \[
          \eta A_0+A_0^\dagger\eta=-2\kappa\Delta\tau I_4,\qquad
          \eta A_{\rm HS}+A_{\rm HS}^\dagger\eta=0 .
        \]
        </p>
        """,
    },
    "B-J2g-s1+q1+": {
        "field_word": "iZZ",
        "title": "反射配对的双组分 Bose-Hubbard 局域模型",
        "body": r"""
        <p>
        取文章中的两种 boson flavors \(b,c\)，考虑
        \[
          \hat H=\kappa(\hat n_b+\hat n_c)
          +\frac U2(\hat n_b-\hat n_c)^2,
          \qquad \kappa>0,\quad U>0 .
        \]
        在格点上可加入位于同一 maximal subgroup 或正确取向 invariant
        cone 的 hopping 与 pairing，前提是总固定生成元仍严格收缩，且
        玻色 Hamiltonian 保持稳定。这样才得到文章 paired benchmark 的
        局域 building block；仅有 flavor reflection 本身不够保证收缩。
        </p>
        <p>
        Repulsive HS field 耦合到
        \(\hat O=\hat n_b-\hat n_c\)：
        \[
          e^{-\Delta\tau U\hat O^2/2}
          \propto\int d\phi\,e^{-\phi^2/2}
          e^{\,i\sqrt{\Delta\tau U}\phi\hat O}.
        \]
        由于
        \[
          \hat h(i\sigma_z\otimes\sigma_z)=i(\hat n_b-\hat n_c),
        \]
        两个时间片生成元为
        \[
          A_0=-\kappa\Delta\tau\,ZI,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,iZZ .
        \]
        \(J_1=IX\) 正是交换 \(b,c\) 后复共轭的 reflection；
        \(iZZ\) 属于 maximal subgroup，\(-ZI=-\eta\) 是 stable strict
        direction。因此该模型不仅“满足 Case 7 的五条式子”，而且逐个
        HS configuration 都满足严格 \(J_2g\)-contraction。这就是
        Yinkai's case 与 7 月 19 日 pole-free paired model 的直接连接。
        </p>
        """,
    },
    "B-J2g-s1+q1-": {
        "field_word": "iZZ",
        "title": "Kramers-like 双组分 relative-density 模型",
        "body": r"""
        <p>
        取两个 boson components，并定义
        \[
          \hat O=\hat n_1-\hat n_2 .
        \]
        考虑稳定的 Hermitian model
        \[
          \hat H=\kappa(\hat n_1+\hat n_2)+\frac U2\hat O^2,
          \qquad \kappa,U>0 .
        \]
        它与 Case 7 使用同一个物理 Hamiltonian，但现在选择
        \(J_1=I_{\rm Nambu}\otimes(i\sigma_y)\)，所以
        \(J_1^2=-I\)。同一个 HS family 同时属于不同五位标签，说明这些
        标签记录的是可用的 symmetry structures，而不是互斥的物理相。
        </p>
        <p>
        直接展开得到
        \[
          \hat h(i\sigma_z\otimes\sigma_z)=i\hat O .
        \]
        因此 repulsive-square HS 分解使用
        \[
          A_0=-\kappa\Delta\tau\,ZI,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,iZZ .
        \]
        \(iZZ\) 是本类的 maximal-subgroup direction；
        \(J_1=IY\) 满足 \(J_1^2=-I\)，
        并分别把两个生成元送到其复共轭。固定的 \(-ZI\) 给出
        \(-2\kappa\Delta\tau I_4\)，而场生成元的 contraction
        expression 为零。
        </p>
        """,
    },
    "B-iJ2g-s1-q1+": {
        "field_word": "ZX",
        "title": "固定粒子数的 bosonic Lipkin-Meshkov-Glick dimer",
        "body": r"""
        <p>
        对两个 boson modes 定义 collective spin
        \[
          S_x=\frac12(a_1^+a_2+a_2^+a_1),\qquad
          S_y=\frac{1}{2i}(a_1^+a_2-a_2^+a_1).
        \]
        在固定总粒子数 sector 中考虑
        \[
          \hat H=-2\Omega S_y-2U S_x^2,\qquad \Omega>0,\quad U>0 .
        \]
        这是可在双阱凝聚体或双内部态冷原子中实现的
        Lipkin-Meshkov-Glick/Josephson model，可研究 collective-spin
        symmetry breaking、macroscopic tunnelling 与 squeezing。
        </p>
        <p>
        本类的 strict witness 与 subgroup direction 分别满足
        \[
          \hat h(-iIY)=2S_y,\qquad
          \hat h(ZX)=2S_x .
        \]
        Attractive-square HS identity 因而给出
        \[
          A_0=-\Omega\Delta\tau\,iIY,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,ZX .
        \]
        \(ZX\) 位于 maximal subgroup，所以任意正负实场都不改变
        固定因子的
        \(\eta A_0+A_0^\dagger\eta=-2\Omega\Delta\tau I_4\)；
        场因子的 contraction expression 为零。
        该模型保持总粒子数，固定-\(N\) Hilbert space 有限，因而是这一
        \(iJ_2g\) 类最直接的物理用途。
        </p>
        <p class="scope">
        <strong>范围。</strong>
        这里已经验证的是每个 HS slice 都满足本类的矩阵等式与严格
        contraction inequality。固定-\(N\) Hilbert space 虽然有限，
        但还必须另证相应 fixed-\(N\) character 沿全部场构型不为零，
        才能宣布无符号；本报告尚未给出这一步。若改做
        grand-canonical bare boson trace，\(-iIY\) 的两个
        single-particle branches 符号相反，因而不能把这个例子当作本文
        BAFQMC 的 grand-canonical sign-free model。
        </p>
        """,
    },
    "B-iJ2g-s1-q1-": {
        "field_word": "ZIZ",
        "title": "四组分 synthetic-spin-orbit collective bosons",
        "body": r"""
        <p>
        令四个 boson components 组成
        \(\boldsymbol a=(a_{\uparrow 1},a_{\uparrow 2},
        a_{\downarrow 1},a_{\downarrow 2})^T\)，两个内部 Pauli spaces
        分别表示 pseudo-spin 与 orbital。固定总粒子数时考虑
        \[
          \hat H=
          -\Omega\,\boldsymbol a^+
          (\sigma_y\otimes\sigma_x)\boldsymbol a
          -\frac U2
          \left[
          \boldsymbol a^+(I_2\otimes\sigma_z)\boldsymbol a
          \right]^2 ,
          \qquad \Omega>0,\quad U>0 .
        \]
        第一项是 synthetic spin-orbit/Raman conversion，第二项是
        orbital-polarization attraction。它适合研究四组分 spinor
        condensates 中的 collective ordering 与 entanglement。
        </p>
        <p>
        这里
        \[
          \hat h(-iIYX)=
          \boldsymbol a^+(\sigma_y\otimes\sigma_x)\boldsymbol a,\qquad
          \hat h(ZIZ)=
          \boldsymbol a^+(I_2\otimes\sigma_z)\boldsymbol a .
        \]
        因而 attractive HS 分解使用
        \[
          A_0=-\Omega\Delta\tau\,iIYX,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,ZIZ .
        \]
        \(ZIZ\) 明确列在本类 maximal-subgroup basis 中；
        \(A_0/(\Omega\Delta\tau)=-iIYX=-\eta\) 是 strict direction。
        所有实场值的场因子都是 metric isometry，固定因子则严格收缩。
        四维内部空间不是为了凑 Pauli
        words，而是 \(J_1^2=-I\) 与本类其余关系同时实现所需的最小
        physical component structure。
        </p>
        <p class="scope">
        与上一类相同，当前结论只完成逐时间片的矩阵结构检验。
        固定总粒子数计算没有玻色 grand-canonical trace divergence，
        但仍需独立证明 fixed-\(N\) 权重不经过零点；grand-canonical
        bare trace 则明确缺少稳定锚点。
        </p>
        """,
    },
    "B-iJ2g-s1+q1+": {
        "field_word": "XX",
        "title": "带 quartic pair-phase stiffness 的 bosonic parametric dimer",
        "body": r"""
        <p>
        仍取两个 boson modes，并令
        \[
          \hat O=-i(a_1^+a_2^+-a_1a_2).
        \]
        \(\hat O\) 是 Hermitian two-mode pair-phase quadrature。模型
        \[
          \hat H=-2\Omega S_y+\frac U2\hat O^2,
          \qquad \Omega>0,\quad U>0
        \]
        描述 coherent flavor conversion 与 two-mode parametric
        fluctuations 的竞争，可用于 driven cavity pairs、molecular
        conversion 或受限占据的 bosonic simulators。
        </p>
        <p>
        直接计算
        \[
          \hat h(-iIY)=2S_y,\qquad
          \hat h(XX)=a_1^+a_2^+-a_1a_2=i\hat O .
        \]
        Repulsive-square HS 分解给出
        \[
          A_0=-\Omega\Delta\tau\,iIY,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,XX .
        \]
        \(XX\) 是本类 maximal-subgroup direction；因此 continuous
        Gaussian field 不论正负都给出 metric-isometric factor，
        strict part 始终由 \(-iIY\) 提供。\(J_1=IX\) 又把两个
        flavors 交换并复共轭，所以两个生成元分别满足本类的实性约束。
        </p>
        <p class="scope">
        该 Hamiltonian 具有清楚的 parametric-boson 物理意义，但
        \(XX\) 改变总粒子数，而现有 strict witness 不是
        grand-canonical trace-convergent anchor。有限占据截断或
        open-system effective dynamics 可以给这个 slice family 一个定义，
        但那是不同的计算问题；不能据此声称已经得到本文所需的 bare
        thermal BAFQMC。
        </p>
        """,
    },
    "B-iJ2g-s1+q1-": {
        "field_word": "ZZ",
        "title": "固定粒子数的 one-axis-twisting Josephson dimer",
        "body": r"""
        <p>
        对两个 boson modes 定义
        \(S_z=(\hat n_1-\hat n_2)/2\)。考虑固定总粒子数下的
        \[
          \hat H=-2\Omega S_y-2U S_z^2,\qquad \Omega>0,\quad U>0 .
        \]
        这是带 one-axis twisting 的 bosonic Josephson/collective-spin
        model，可研究 self trapping、spin squeezing、cat states 与
        quantum metrology。
        </p>
        <p>
        因为
        \[
          \hat h(-iIY)=2S_y,\qquad \hat h(ZZ)=2S_z ,
        \]
        attractive-square HS 分解使用
        \[
          A_0=-\Omega\Delta\tau\,iIY,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,ZZ .
        \]
        \(ZZ\) 位于本类 maximal subgroup，故
        \(\eta A_0+A_0^\dagger\eta=-2\Omega\Delta\tau I_4\)，而
        \(\eta A_{\rm HS}+A_{\rm HS}^\dagger\eta=0\)。
        \(J_1=YX\) 的 square 为 \(-I\)，并逐项保持这个 slice family
        的 anti-linear condition。
        </p>
        <p class="scope">
        固定-\(N\) sector 给出有限的 many-body problem，却不会自动给出
        fixed-\(N\) trace 的恒正性；这一点仍需另证。grand-canonical
        bare trace 的限制与前两个 bosonic \(iJ_2g\) models 相同。
        </p>
        """,
    },
    "F-J2g-s1-q1+": {
        "field_word": "IY",
        "title": "spinless-fermion bond-current interaction dimer",
        "body": r"""
        <p>
        最小 Pauli representative 只有一个 fermion mode，maximal subgroup
        因而退化。把同一 \(J_1=\sigma_z\otimes I\)、
        \(J_2=i\sigma_y\otimes I\) tensor-extend 到两个 sites 后，定义
        \[
          \hat j=-i(c_1^+c_2-c_2^+c_1)
        \]
        并考虑
        \[
          \hat H=\kappa(\hat n_1+\hat n_2-1)
          -t(c_1^+c_2+c_2^+c_1)+\frac U2\hat j^2,
          \qquad \kappa>|t|,\quad U>0 .
        \]
        在单条 bond 上，
        \(\hat j^2=\hat n_1+\hat n_2-2\hat n_1\hat n_2\)，
        所以这个 dimer 等价于 density interaction，并没有形成几何 loop。
        推广到含多条独立 bond currents 的 plaquette 后，才可研究
        loop-current correlations 与 time-reversal breaking。
        </p>
        <p>
        Nambu generators 满足
        \[
          \hat h(IY)=c_1^+c_2-c_2^+c_1=i\hat j ,
        \]
        所以 repulsive HS 分解使用
        \[
          A_0=\Delta\tau(-\kappa ZI+tZX),\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,IY .
        \]
        \(IY\) 是 tensor-extended maximal-subgroup direction；
        real symmetric hopping \(ZX\) 位于 cone。条件
        \(\kappa>|t|\) 使 number-conserving \(B=-\kappa I+t\sigma_x\)
        negative definite，因此固定因子严格 contraction，场因子是
        metric isometry；其有序乘积对任意实场仍严格 contraction。
        这也说明最小 representative 的零维 subgroup 不是该 class
        在物理 lattice extension 中没有相互作用模型。
        </p>
        """,
    },
    "F-J2g-s1-q1-": {
        "field_word": "iXY",
        "title": "particle-hole anti-linear symmetry 下的配对通道 attractive dot",
        "body": r"""
        <p>
        对两个 fermion modes \(c,d\) 定义 Hermitian pair quadrature
        \[
          \hat P_y=i(c^+d^+ + cd).
        \]
        考虑
        \[
          \hat H=\kappa(\hat n_c+\hat n_d-1)-\frac U2\hat P_y^2,
          \qquad \kappa>0,\quad U>0 .
        \]
        这个两模问题中有恒等式
        \[
          \hat P_y^2=(\hat n_c+\hat n_d-1)^2.
        \]
        因此它不是一个独立的 local charge-\(4e\) interaction，而是把
        attractive density interaction 选在 pairing quadrature 通道做
        HS 分解。加入显式 proximity pairing 或扩展到格点后，可用于研究
        superconducting parity crossing 与 interacting Andreev levels。
        </p>
        <p>
        在当前 ordering convention 中
        \[
          \hat h(iXY)=\hat P_y .
        \]
        Attractive-square HS transformation 因而产生
        \[
          A_0=-\kappa\Delta\tau\,ZI,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,iXY .
        \]
        \(iXY\) 位于本类 maximal subgroup，\(-ZI=-\eta\) 是 strict
        number-damping direction。因此固定因子的 contraction
        expression 是 \(-2\kappa\Delta\tau I_4\)，场因子的
        contraction expression 为零。
        \(J_1=ZY\) 同时给出本类 \(J_1^2=-I\) 与
        \(J_1^TAJ_1=\bar A\)。
        </p>
        """,
    },
    "F-J2g-s1+q1+": {
        "field_word": "iXY",
        "title": "Majorana-reflection 两轨道 attractive dimer",
        "body": r"""
        <p>
        仍定义 \(\hat P_y=i(c^+d^+ + cd)\)，但现在加入 reflection-even
        orbital hybridization：
        \[
          \hat H=\kappa(\hat n_c+\hat n_d-1)
          -t(c^+d+d^+c)-\frac U2\hat P_y^2,
          \qquad \kappa>|t|,\quad U>0 .
        \]
        由于 \(\hat P_y^2=(\hat n_c+\hat n_d-1)^2\)，这是在 pairing
        通道分解的 attractive two-orbital dimer。它同时含 normal
        hybridization 与 pairing-channel fluctuations，是研究
        Majorana-reflection cone 与 Andreev spectra 的最小非平凡模型。
        </p>
        <p>
        其两个生成元是
        \[
          A_0=\Delta\tau(-\kappa ZI+tZX),\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,iXY .
        \]
        \(iXY\) 属于 maximal subgroup；\(ZX\) 是本类允许的
        reflection-even cone direction。由于
        \(B=-\kappa I+t\sigma_x\) 的两个 eigenvalues 都为负，
        \(\kappa>|t|\) 保证固定因子 strict contraction，而 HS
        因子位于 maximal subgroup。\(J_1=IX\)
        交换两个 reflected orbitals 并复共轭，逐场值保持整个
        有序时间片。
        </p>
        """,
    },
    "F-J2g-s1+q1-": {
        "field_word": "YY",
        "title": "Kramers pair-quadrature attractive model",
        "body": r"""
        <p>
        把 \(c,d\) 看作一对 Kramers partners，并定义
        \[
          \hat P_x=c^+d^+-cd .
        \]
        由于 fermion ordering，\(\hat P_x^\dagger=\hat P_x\)。
        取
        \[
          \hat H=\kappa(\hat n_c+\hat n_d-1)-\frac U2\hat P_x^2 ,
          \qquad \kappa>0,\quad U>0 .
        \]
        同样有
        \(\hat P_x^2=(\hat n_c+\hat n_d-1)^2\)，所以这是保持
        Kramers anti-linear structure 的 pairing-channel
        attractive model；在 lattice extension 中可研究
        time-reversal-invariant superconducting collective modes。
        </p>
        <p>
        直接展开可得
        \[
          \hat h(YY)=c^+d^+-cd=\hat P_x .
        \]
        所以 attractive HS 分解使用
        \[
          A_0=-\kappa\Delta\tau\,ZI,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,YY .
        \]
        \(YY\) 是本类 maximal-subgroup direction，而
        \(J_1=IY\) 正是 \(T(c)=d,\ T(d)=-c\) 的 real matrix part。
        每个 slice 因而既满足 Kramers reality condition，又保持由
        \(-ZI\) 给出的 strict \(J_2g\)-contraction。
        </p>
        """,
    },
    "F-iJ2g-s1-q1+": {
        "field_word": "ZI",
        "title": "带 attractive charging energy 的 proximitized fermion dot",
        "body": r"""
        <p>
        定义 Hermitian pairing quadrature
        \[
          \hat\Delta_y=-i(c^+d^+ + cd),\qquad
          \hat Q=\hat n_c+\hat n_d-1 .
        \]
        考虑 superconducting quantum dot
        \[
          \hat H=-\Delta\,\hat\Delta_y-\frac U2\hat Q^2,
          \qquad \Delta,U>0 .
        \]
        对 \(d\) 做一个固定 phase rotation 后，第一项就是通常的
        real \(s\)-wave proximity pairing；第二项是 attractive charging
        interaction。该模型可研究 even/odd parity crossings 与 Andreev states。
        </p>
        <p>
        本类满足
        \[
          \hat h(-iXY)=\hat\Delta_y,\qquad
          \hat h(ZI)=\hat Q .
        \]
        因而 attractive HS 分解使用
        \[
          A_0=-\Delta\Delta\tau\,iXY,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,ZI .
        \]
        \(-iXY=-\eta\) 是 physical pairing strict direction，
        \(ZI\) 属于 maximal subgroup。费米 Fock space 有限，所以
        不存在玻色 bare-trace divergence；固定因子严格收缩，所有实场的
        density factors 都位于同一个 maximal subgroup。
        </p>
        """,
    },
    "F-iJ2g-s1-q1-": {
        "field_word": "iZZ",
        "title": "带 spin-polarization interaction 的 superconducting dot",
        "body": r"""
        <p>
        继续使用 \(\hat\Delta_y=-i(c^+d^+ + cd)\)，并定义
        \(\hat S_z=\hat n_c-\hat n_d\)。模型
        \[
          \hat H=-\Delta\hat\Delta_y+\frac U2\hat S_z^2,
          \qquad \Delta,U>0
        \]
        是有 proximity pairing 与 repulsive polarization channel 的
        superconducting Anderson atom，可研究 pairing 与 magnetic
        polarization 的竞争。
        </p>
        <p>
        因为
        \[
          \hat h(-iXY)=\hat\Delta_y,\qquad
          \hat h(iZZ)=i\hat S_z ,
        \]
        repulsive-square HS decomposition 给出
        \[
          A_0=-\Delta\Delta\tau\,iXY,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,iZZ .
        \]
        \(iZZ\) 是本类 maximal-subgroup direction，故 field sign
        不影响 strictness；\(J_1=YI\) 与 \(J_2=IY\) 对易并分别满足
        本类所需的 \(g\)-sign 与 square relations。
        </p>
        """,
    },
    "F-iJ2g-s1+q1+": {
        "field_word": "iZZ",
        "title": "reflection-paired proximitized fermion dimer",
        "body": r"""
        <p>
        令 \(c,d\) 为 reflection partners，取
        \[
          \hat H=-\Delta\hat\Delta_y
          -t(c^+d+d^+c)+\frac U2(\hat n_c-\hat n_d)^2 ,
          \qquad \Delta>|t|,\quad U>0 .
        \]
        这是同时含 proximity pairing、orbital hybridization 与
        polarization interaction 的 two-level superconducting dot，
        可研究 Majorana-reflection constraints 下的 interacting
        Andreev spectrum。
        </p>
        <p>
        相应的固定与辅助场生成元分别为
        \[
          A_0=\Delta\tau(-\Delta\,iXY+tZX),\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,iZZ .
        \]
        \(iZZ\) 在 maximal subgroup；\(ZX\) 是允许的 cone direction。
        直接对角化 contraction matrix 得到最大 eigenvalue
        \(2\Delta\tau(-\Delta+|t|)\)，所以显示的
        \(\Delta>|t|\) 正好保证固定生成元严格小于零；场因子位于
        maximal subgroup。
        \(J_1=IX\) 交换两个
        reflected modes，逐场值保持 reality condition。
        </p>
        """,
    },
    "F-iJ2g-s1+q1-": {
        "field_word": "ZII",
        "title": "Kramers 两轨道 superconducting island",
        "body": r"""
        <p>
        取两条 orbitals，每条含一对 fermion components，并按
        \[
          \boldsymbol c=(c_{\uparrow1},c_{\uparrow2},
          c_{\downarrow1},c_{\downarrow2})^T
        \]
        排列，使第一个内部 Pauli factor 作用在
        \(\uparrow,\downarrow\)，第二个作用在 orbital \(1,2\)。令
        \[
          \hat\Delta_y=-i\sum_{\ell=1}^2
          (c_{\uparrow\ell}^+c_{\downarrow\ell}^+
           +c_{\uparrow\ell}c_{\downarrow\ell}),\qquad
          \hat Q=\sum_{\ell,s}\hat n_{\ell s}-2 .
        \]
        考虑
        \[
          \hat H=-\Delta\hat\Delta_y-\frac U2\hat Q^2 ,
          \qquad \Delta>0,\quad U>0 .
        \]
        这是带 Kramers structure、两条 orbitals 和 attractive charging
        energy 的 superconducting island，可研究 parity transitions、
        pair transfer 与多轨道 Andreev multiplets。
        </p>
        <p>
        在本类最小 Pauli realization 中
        \[
          \hat h(-iXYI)=\hat\Delta_y,\qquad
          \hat h(ZII)=\hat Q ,
        \]
        因而两个生成元为
        \[
          A_0=-\Delta\Delta\tau\,iXYI,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,ZII .
        \]
        \(ZII\) 明确属于 maximal subgroup，\(-iXYI=-\eta\)
        是 strict pairing direction。\(J_1=IXY\) 平方为 \(-I\)，
        因而 \(J_1K\) 是一个 Kramers-type anti-linear operation；
        它同时交换 spin 与 orbital labels，而不是默认等同于电子的标准
        time reversal。\(J_2=IYI\) 则选择 contraction cone。
        </p>
        <p>
        在 lattice 上可以加入同一 maximal subgroup 中的 hopping，
        并把 onsite pairing 换成保持相同 matrix conditions 的 bond pairing。
        这个模型与 Wei semigroup paper 一样同时含 Kramers-type structure
        与 pairing，但不能据此把两个 matrix classes 直接等同。Wei 论文的
        canonical Majorana metric 完整拉回 Nambu basis 后落在
        \(J_2g\) branch；本例属于另一条 \(iJ_2g\) branch。
        它们是否可由额外的 particle--hole or complex-orthogonal
        transformation 联系，必须另行证明。
        </p>
        """,
    },
}


def render_physical_model(class_name: str) -> str:
    model = MODEL_CATALOG[class_name]
    scalar_note = ""
    if class_name.startswith("B-J2g"):
        scope = "稳定的 grand-canonical 玻色 HS 构造"
        mode_count = 1 if class_name == "B-J2g-s1-q1+" else 2
        scalar_note = rf"""
        <p class="small">
        <strong>正常序标量因子。</strong>
        这里有 \(m={mode_count}\) 个玻色模，且
        \[
          \hat h(A_0)=-\kappa\Delta\tau(\hat N+m/2).
        \]
        因此物理因子 \(e^{{-\kappa\Delta\tau\hat N}}\) 等于
        \(e^{{+\kappa\Delta\tau m/2}}e^{{\hat h(A_0)}}\)。
        前面的标量严格为正，必须计入完整权重，但不改变符号和收缩判据。
        </p>
        """
    elif class_name.startswith("B-iJ2g"):
        scope = "逐时间片矩阵实现；尚不是 grand-canonical 无符号模型"
    else:
        scope = r"费米物理 HS slice；按标准传播矩阵 \(e^A\) 条件检验"
    return (
        '<section class="model-example">'
        f'<p class="model-title"><strong>物理模型：{model["title"]}</strong></p>'
        f'<p class="model-scope"><strong>证据范围：</strong>{scope}</p>'
        f'{model["body"]}'
        f"{scalar_note}"
        "</section>"
    )
