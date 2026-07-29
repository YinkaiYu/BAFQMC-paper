"""Reader-facing physical models for the sixteen classes with negative-definite points."""

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
        第一项正是使收缩矩阵负定的例子 \(-\eta\)，第二项正是本类
        maximal subgroup 的 \(iY\) direction，所以
        \[
          \eta A_0+A_0^\dagger\eta=-2\kappa\Delta\tau I<0,\qquad
          \eta A_{\rm HS}+A_{\rm HS}^\dagger\eta=0
        \]
        对所有实 \(\phi\) 同时成立。这里不只列出满足矩阵关系的 \(A\)：
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
        \(-ZI=-\eta\) 使收缩矩阵负定。\(J_1=ZY\) 对两个生成元
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
        cone 的 hopping 与 pairing，前提是总固定生成元仍使
        \(\eta A_0+A_0^\dagger\eta<0\)，且
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
        \(iZZ\) 属于 maximal subgroup，\(-ZI=-\eta\) 是稳定的负定方向。
        因此该模型不仅“满足 Case 7 的五条式子”，而且逐个
        HS configuration 的完整传播都位于 \(J_2g\)-contraction
        semigroup 内部。这就是
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
        本类的负定例子与 subgroup direction 分别满足
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
        <p class="result">
        <strong>固定-\(N\) 权重严格为正。</strong>
        令 \(m(\phi)\) 为任意数量时间片相乘后的 \(2\times2\)
        one-particle matrix。每个生成元 traceless，所以
        \(\det m=1\)；本类的 anti-linear condition 使
        \(\operatorname{tr}m\) 为实数。固定因子严格收缩、场因子取等号，
        因而完整 Nambu product 仍严格收缩，\(m\) 不可能有单位圆
        eigenvalue。零场时两个 eigenvalues 是正数；实 Gaussian field
        space 连通，故它们不能经过 \(+1\)、\(-1\) 或复共轭单位圆而变成
        负数，始终可写为 \(\lambda,\lambda^{-1}\)，其中 \(\lambda>0\)。
        固定总粒子数 \(N\) 的权重于是为
        \[
          W_N(\phi)=\sum_{n=0}^{N}\lambda^{N-n}\lambda^{-n}
          =\sum_{n=0}^{N}\lambda^{N-2n}>0 .
        \]
        这给出完整的 canonical sign-free proof。相反，其中一个
        eigenvalue 大于 1，所以 \(\sum_{N=0}^\infty W_N\) 发散；
        同一模型不能改称 grand-canonical sign-free BAFQMC。
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
        \(A_0/(\Omega\Delta\tau)=-iIYX=-\eta\) 使收缩矩阵负定。
        所有实场值的场因子都满足
        \(M_{\rm HS}^\dagger\eta M_{\rm HS}=\eta\)，固定因子则满足
        \(M_0^\dagger\eta M_0-\eta<0\)。
        四维内部空间不是为了凑 Pauli
        words，而是 \(J_1^2=-I\) 与本类其余关系同时实现所需的最小
        physical component structure。
        </p>
        <p class="result">
        <strong>这个四组分模型的 fixed-\(N\) weight 也严格为正。</strong>
        先把第一个内部 Pauli space 的 \(\sigma_y\) diagonalize。
        one-particle product 分成两个 \(2\times2\) blocks：
        一个由 \(e^{+\Omega\Delta\tau\sigma_x}\) 与
        \(e^{\phi\sigma_z}\) 相乘，另一个把
        \(\Omega\) 换成 \(-\Omega\)。由于
        \(\sigma_z e^{+\Omega\sigma_x}\sigma_z
        =e^{-\Omega\sigma_x}\)，两个 blocks 彼此相似，具有同一组
        正 eigenvalues \(\lambda,\lambda^{-1}\)。因此完整 spectrum 是
        \(\lambda,\lambda^{-1},\lambda,\lambda^{-1}\)，而
        \[
          \sum_{N=0}^{\infty}W_Nz^N
          =\frac{1}{[(1-z\lambda)(1-z/\lambda)]^2}.
        \]
        右边每个 \(z^N\) coefficient 都是正数，所以所有 fixed-\(N\)
        auxiliary-field weights 严格为正。grand-canonical sum 仍因
        \(\lambda>1\) 发散。
        </p>
        """,
    },
    "B-iJ2g-s1+q1+": {
        "field_word": "ZX",
        "title": r"具有 reflection-type \(J_1\) 的 canonical LMG dimer",
        "body": r"""
        <p>
        仍取两个 boson modes，并定义
        \[
          S_x=\frac12(a_1^+a_2+a_2^+a_1),\qquad
          S_y=\frac{1}{2i}(a_1^+a_2-a_2^+a_1).
        \]
        在固定总粒子数 sector 中考虑
        \[
          \hat H=-2\Omega S_y-2U S_x^2,
          \qquad \Omega>0,\quad U>0
        \]
        这是 collective-spin LMG/Josephson model。它与
        \(B\)-\(iJ_2g\)-\(s_1-\)-\(q_1+\) 使用同一个物理
        Hamiltonian，但本类选择
        \(J_1=I_{\rm Nambu}\otimes\sigma_x\)，所以
        \(J_1^TgJ_1=g\)。同一模型同时具有两组允许的
        \(J_1\) structures，说明四类标签不是互斥的物理相。
        </p>
        <p>
        直接计算
        \[
          \hat h(-iIY)=2S_y,\qquad
          \hat h(ZX)=2S_x .
        \]
        Attractive-square HS 分解给出
        \[
          A_0=-\Omega\Delta\tau\,iIY,\qquad
          A_{\rm HS}(\phi)=\sqrt{\Delta\tau U}\phi\,ZX .
        \]
        \(ZX\) 是本类 maximal-subgroup direction；因此 continuous
        Gaussian field 不论正负都给出满足
        \(M_{\rm HS}^\dagger\eta M_{\rm HS}=\eta\) 的传播因子，
        收缩矩阵的负定部分始终由 \(-iIY\) 提供。\(J_1=IX\) 又把两个
        flavors 交换并复共轭，所以两个生成元分别满足本类的实性约束。
        </p>
        <p class="result">
        这个 number-conserving choice 避开了原先 pairing-field 例子的
        中间态收敛问题。与另一 LMG realization 相同，完整 one-particle
        product 的 eigenvalues 始终为正的
        \(\lambda,\lambda^{-1}\)，所以
        \[
          W_N=\sum_{n=0}^{N}\lambda^{N-2n}>0 .
        \]
        因而它是完整的 canonical fixed-\(N\) sign-free model；
        grand-canonical trace 仍发散。
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
        \(J_1=YX\) 的 square 为 \(-I\)，并且 \(A_0\) 与
        \(A_{\rm HS}(\phi)\) 分别满足
        \(J_1^TAJ_1=\bar A\)。
        </p>
        <p class="result">
        把 one-particle matrices 用一个固定 unitary rotation 变换后，
        \(\sigma_y\) 与 \(\sigma_z\) 同时成为 real matrices。
        因而完整 product 的 characteristic polynomial 为实；
        严格 \(iJ_2g\) contraction 排除单位圆 eigenvalues，连通性又把
        它们固定为正的 \(\lambda,\lambda^{-1}\)。所以每个 fixed-\(N\)
        weight 都等于
        \(\sum_{n=0}^{N}\lambda^{N-2n}>0\)。
        这是完整的 canonical sign-free proof；grand-canonical sum 发散。
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
        negative definite，因此固定因子满足
        \(M^\dagger\eta M-\eta<0\)，场因子是 metric isometry；
        其有序乘积对任意实场仍位于半群内部。
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
        \(iXY\) 位于本类 maximal subgroup，\(-ZI=-\eta\) 是使收缩矩阵
        负定的 number-damping direction。因此固定因子的 contraction
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
        \(iXY\) 满足
        \(\eta iXY+(iXY)^\dagger\eta=0\)；\(ZX\) 满足
        \(\eta ZX=(ZX)^\dagger\eta\)。由于
        \(B=-\kappa I+t\sigma_x\) 的两个 eigenvalues 都为负，
        \(\kappa>|t|\) 保证固定因子满足
        \(M^\dagger\eta M-\eta<0\)，而 HS
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
        \(-ZI\) 给出的负定 \(J_2g\)-contraction condition。
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
        \(-iXY=-\eta\) 是使收缩矩阵负定的 physical pairing direction，
        \(ZI\) 属于 maximal subgroup。费米 Fock space 有限，所以
        不存在玻色 bare-trace divergence；固定因子的收缩矩阵负定，
        所有实场的 density factors 都位于同一个 maximal subgroup。
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
        不影响固定项提供的负定余量；\(J_1=YI\) 与 \(J_2=IY\) 对易并分别满足
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
        \(iZZ\) 满足
        \(\eta iZZ+(iZZ)^\dagger\eta=0\)，而 \(ZX\) 满足
        \(\eta ZX=(ZX)^\dagger\eta\)。
        直接对角化 contraction matrix 得到最大 eigenvalue
        \(2\Delta\tau(-\Delta+|t|)\)，所以显示的
        \(\Delta>|t|\) 正好保证固定生成元的收缩矩阵负定；场因子位于
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
        是使收缩矩阵负定的 pairing direction。\(J_1=IXY\) 平方为 \(-I\)，
        因而 \(J_1\mathcal K\) 是一个 Kramers-type anti-linear
        operation，其中 \(\mathcal K\) 表示逐分量复共轭；
        它同时交换 spin 与 orbital labels，而不是默认等同于电子的标准
        time reversal。\(J_2=IYI\) 则选择 contraction cone。
        </p>
        <p>
        在 lattice 上可以加入同一 maximal subgroup 中的 hopping，
        并把 onsite pairing 换成保持相同 matrix conditions 的 bond pairing。
        这个模型与 Wei semigroup paper 一样同时含 Kramers-type structure
        与 pairing，但不能据此把两个 matrix classes 直接等同。Wei 论文的
        canonical Majorana metric 完整拉回 Nambu basis 后具有
        \(\eta=J_2g\) 的形式；本例使用的则是 \(\eta=iJ_2g\)。
        它们是否可由额外的 particle--hole or complex-orthogonal
        transformation 联系，必须另行证明。
        </p>
        """,
    },
}


STRICT_RESEARCH_PROGRAMS: dict[str, dict[str, str]] = {
    "B-J2g-s1-q1+": {
        "title": "受驱动 kagome/三角平带中的相互作用玻色 BdG 相",
        "body": r"""
        <p>
        这个二维 Nambu 类不需要内部 flavor。令 \(a_i\) 是一个
        单组分玻色，取
        \[
        \begin{aligned}
          H={}&\sum_{ij}a_i^+K_{ij}a_j+
          \frac12\sum_{ij}\Delta_{ij}(a_i^+a_j^++a_ia_j)\\
          &+\frac U2\sum_\alpha
          \left[\frac12\sum_{ij}F_{\alpha,ij}
          (a_i^+a_j^++a_ia_j)\right]^2 ,
          \qquad U>0 ,
        \end{aligned}
        \]
        其中 \(K=K^\dagger\) 可取 kagome 或三角格子的受阻挫平带，
        \(\Delta=\Delta^T\)、\(F_\alpha=F_\alpha^T\) 实。
        \(K\) 与 \(\Delta\) 选择在本类
        \(A_{\mathrm{cone}}\) 中并要求
        \(\eta A_{\mathrm{cone}}<0\)；pair quadrature 的纯虚 HS
        生成元则位于 \(A_{\mathrm{group}}\)。
        </p>
        <p>
        这是可研究 interacting squeezed condensate、有限动量
        pair condensation 和受驱动平带拓扑转变的格点模型。与普通
        Bose-Hubbard 模型相比，它真正使用本类允许的 anomalous
        Nambu directions；下面展开的单模公式只是每个
        \(F_\alpha\) 通道的最小矩阵核。
        </p>
        """,
    },
    "B-J2g-s1-q1-": {
        "title": "全阻挫格子上的玻色 loop-current 相互作用模型",
        "body": r"""
        <p>
        在含三角形或方形 plaquettes 的格子上定义
        \[
          \hat j_{ij}=-i(a_i^+a_j-a_j^+a_i),\qquad
          \hat J_p=\sum_{\langle ij\rangle\in p}\nu_{p,ij}\hat j_{ij},
        \]
        并考虑
        \[
          H=\sum_{ij}a_i^+(\kappa I-t)_{ij}a_j
          +\frac U2\sum_p\hat J_p^2,\qquad U>0 .
        \]
        实反对称的有向 incidence matrices
        \(\nu_{p,ij}\) 正是本类 \(IY\otimes K_{IY}\) 的
        \(A_{\mathrm{group}}\) 方向；稳定的
        \(\kappa I-t>0\) 则从本类 number-conserving
        \(A_{\mathrm{cone}}\) 中选择。
        </p>
        <p>
        该模型直接检验 loop-current order、手性 Ising 转变与 BKT
        相干转变能否分裂，并可用于全阻挫 Bose-Hubbard 所涉及的
        chiral-Mott 邻域。相关背景见
        <a href="https://arxiv.org/abs/1207.1725">全阻挫玻色子的
        chiral Mott 工作</a>。下方 dimer 只负责把每条有向 bond 的
        HS 生成元逐项核对清楚。
        </p>
        """,
    },
    "B-J2g-s1+q1+": {
        "title": "反射配对的受阻挫双组分玻色平带",
        "body": r"""
        <p>
        令 \(b_i,c_i\) 是被 \(J_1\) 交换的一对物理组分。一个直接的
        格点推广是
        \[
        \begin{aligned}
          H={}&\sum_{ij,\alpha=b,c}
          \alpha_i^+K_{ij}\alpha_j+
          \sum_{ij}\Delta_{ij}(b_i^+c_j^++b_ic_j)\\
          &+\frac12\sum_{ij}V_{ij}
          (n_{b,i}-n_{c,i})(n_{b,j}-n_{c,j}),
          \qquad V\succeq0 .
        \end{aligned}
        \]
        \(K\) 可取三角或 kagome 阻挫平带；pairing 与稳定正位移共同
        放入本类 \(A_{\mathrm{cone}}\)，相对密度的纯虚 HS 场属于
        \(A_{\mathrm{group}}\)。这里 \(J_1=IX\) 不是额外模板，而是
        卡片解空间中实际交换两个 reflected flavors 的矩阵。
        </p>
        <p>
        这正是 Yin-Kai paired class 的可扩展版本，可研究
        pair-superfluid、手性凝聚和相对密度序的竞争；它也把 7 月
        19 日 pole-free 配对模型从局域 benchmark 推到受阻挫格点。
        </p>
        """,
    },
    "B-J2g-s1+q1-": {
        "title": "Kramers 玻色双层中的阻挫凝聚与相对密度临界性",
        "body": r"""
        <p>
        取 Kramers-like 组分
        \(\boldsymbol b_i=(b_{i\uparrow},b_{i\downarrow})^T\)，
        \[
          H=\sum_{ij}\boldsymbol b_i^+
          [K_{ij}I+iR_{ij}\sigma_z]\boldsymbol b_j+
          \frac12\sum_{ij}V_{ij}Q_iQ_j,\qquad
          Q_i=n_{i\uparrow}-n_{i\downarrow},
        \]
        其中 \(K=K^T\)、\(R=-R^T\)、\(V\succeq0\)。
        两组分看到相反的 Peierls texture；\(iR\sigma_z\) 与
        \(iQ\) 的 HS 场都可从本类 \(A_{\mathrm{group}}\) 表中选取，
        稳定的共同 chemical-potential/hopping block 放在
        \(A_{\mathrm{cone}}\)。
        </p>
        <p>
        这个模型可研究 bosonic quantum-spin-Hall-like 平带中的
        相互作用凝聚、涡旋结构与相对密度临界性。它使用
        \(J_1^2=-I\) 的实际双组分结构，而不是在最小模型外再添加一套
        无关 Kramers flavor。
        </p>
        """,
    },
    "B-iJ2g-s1-q1+": {
        "title": "固定粒子数的长程 Josephson 网络与集体临界性",
        "body": r"""
        <p>
        将两个模推广成两组各含 \(L\) 个轨道的 collective modes，
        \[
          H=-2\sum_{ij}\Omega_{ij}S_{y,ij}
          -2\sum_{\alpha}U_\alpha
          \left(\sum_i f_{\alpha i}S_{x,i}\right)^2 ,
          \qquad U_\alpha>0 .
        \]
        实际 one-body conversion 选在本类
        \(A_{\mathrm{cone}}\)，每个 \(S_x\) form factor 是
        \(A_{\mathrm{group}}\) 的实 HS 方向。算法在固定总玻色数
        \(N\) 的有限 Hilbert space 中采样，不使用发散的
        grand-canonical trace。
        </p>
        <p>
        该网络可研究多模自陷、collective first-order transitions、
        spin squeezing 与有限尺寸临界动力学。下方 LMG dimer 给出
        一条通道的严格 fixed-\(N\) 正性证明；推广时必须逐个检查
        one-particle blocks 是否仍具有同一正谱结构。
        </p>
        """,
    },
    "B-iJ2g-s1-q1-": {
        "title": "四组分自旋轨道耦合玻色子的集体拓扑与纠缠",
        "body": r"""
        <p>
        取四组分
        \(\boldsymbol a_i=(a_{\uparrow1},a_{\uparrow2},
        a_{\downarrow1},a_{\downarrow2})^T\)，并令
        \[
          H=-\sum_{ij}\boldsymbol a_i^+
          [\Omega_{ij}\sigma_y\otimes\sigma_x]\boldsymbol a_j
          -\frac12\sum_\alpha U_\alpha
          \left[\sum_i f_{\alpha i}
          \boldsymbol a_i^+(I\otimes\sigma_z)\boldsymbol a_i\right]^2 .
        \]
        第一项来自这个 8 维物理代表的
        \(A_{\mathrm{cone}}\)，orbital polarization 则是
        \(A_{\mathrm{group}}\) 的实 HS 方向。四个组分是同时实现
        本类 \(J_1^2=-I\) 与其余关系所需的结构，不是装饰性复制。
        </p>
        <p>
        在固定总粒子数下，这一模型可研究 spin-orbital entanglement、
        Raman-induced band inversion 与 collective symmetry breaking。
        下方公式还说明为什么当前已证明的正性依赖两个相似
        \(2\times2\) blocks；任意加入破坏该 block pairing 的 hopping
        都必须重新检验。
        </p>
        """,
    },
    "B-iJ2g-s1+q1+": {
        "title": "反射对称双阱阵列中的多轴 squeezing 相",
        "body": r"""
        <p>
        对反射交换的双阱单元 \(i\) 定义 \(S_{x,i},S_{y,i}\)，取
        \[
          H=-2\sum_{ij}\Omega_{ij}S_{y,ij}
          -2\sum_{\alpha}U_\alpha
          \left(\sum_i f_{\alpha i}S_{x,i}\right)^2 .
        \]
        \(J_1^2=+I\) 的 reflection 把两个阱交换；conversion block
        选择在 \(A_{\mathrm{cone}}\)，所有 collective \(S_x\)
        HS directions 列在 \(A_{\mathrm{group}}\) 表中。
        </p>
        <p>
        该 fixed-\(N\) 阵列可研究多轴 squeezing、反射破缺和
        macroscopic tunnelling。它与另一 LMG 标签可共享同一高对称
        Hamiltonian，但在本卡中必须用这里实际的 \(J_1,J_2\) 逐项
        检查；下方 dimer 是这一检查的最小版本。
        </p>
        """,
    },
    "B-iJ2g-s1+q1-": {
        "title": "固定粒子数 Josephson 阵列中的自陷、cat 态与量子计量",
        "body": r"""
        <p>
        令 \(S_{z,i}=(n_{i1}-n_{i2})/2\)，考虑
        \[
          H=-2\sum_{ij}\Omega_{ij}S_{y,ij}
          -2\sum_\alpha U_\alpha
          \left(\sum_i f_{\alpha i}S_{z,i}\right)^2 .
        \]
        \(S_y\) conversion 取自本类 \(A_{\mathrm{cone}}\)，
        \(S_z\) form factors 取自 \(A_{\mathrm{group}}\)。
        这给出带空间相关 one-axis twisting 的 canonical AFQMC
        目标，而不是只计算单个 Josephson dimer。
        </p>
        <p>
        可测量的核心问题包括 interaction-driven self trapping、
        多体 cat-state crossover、Fisher information 与 squeezing
        的温度依赖。严格证明目前覆盖保持下方正谱配对的 form factors；
        一般空间耦合需按卡片中的 \(P\)–\(K_P\) 条件重新核对。
        </p>
        """,
    },
    "F-J2g-s1-q1+": {
        "title": "阻挫 Dirac/平带费米子的 loop-current 相互作用",
        "body": r"""
        <p>
        在 honeycomb、kagome 或 \(\pi\)-flux 格子上定义 plaquette
        current \(\hat J_p\)，考虑
        \[
          H=\sum_{ij}c_i^+(\kappa I-t)_{ij}c_j+
          \frac U2\sum_p\hat J_p^2 .
        \]
        有向实反对称 bond matrix 给出本类
        \(IY\otimes K_{IY}\) 的 \(A_{\mathrm{group}}\) HS 方向；
        \(\kappa I-t>0\) 是 number-conserving
        \(A_{\mathrm{cone}}\)。它可研究 loop-current mass、
        anomalous Hall order 与平带轨道磁性。
        </p>
        <p>
        单条 bond 上 \(\hat j^2\) 会退化为密度相互作用，所以真正值得
        计算的是含多个独立 plaquette currents 的格点；下方 dimer 仅
        用来验证每条 bond 的矩阵归属。
        </p>
        """,
    },
    "F-J2g-s1-q1-": {
        "title": "相互作用拓扑超导体中的 parity 与 pair-density-wave 转变",
        "body": r"""
        <p>
        将两模 pair quadrature 推广到格点 form factors
        \[
          P_\alpha=i\sum_{ij}F_{\alpha,ij}
          (c_i^+c_j^++c_ic_j),\qquad
          H=H_{\mathrm{BdG}}-\frac12\sum_\alpha U_\alpha P_\alpha^2 .
        \]
        稳定的 \(H_{\mathrm{BdG}}\) 取自
        \(A_{\mathrm{cone}}\)，每个 \(P_\alpha\) 的实 HS
        direction 取自本类 \(A_{\mathrm{group}}\)。通过选择 onsite、
        bond 或有限动量 \(F_\alpha\)，可研究 Andreev-band parity
        crossing、pair-density wave 与 charge-\(4e\) 关联。
        </p>
        <p>
        下方两模恒等式说明最小 onsite 通道并不独立；在格点上采用多个
        bond form factors 后，quartic interaction 不再只是一个局域
        charging term，这才是该类的新物理内容。
        </p>
        """,
    },
    "F-J2g-s1+q1+": {
        "title": "Majorana-reflection 多轨道 BdG 平带与相互作用边界态",
        "body": r"""
        <p>
        对一对 reflected orbitals 写
        \[
          H=H_{\mathrm{BdG}}[K,\Delta]
          -\frac12\sum_\alpha U_\alpha P_{\alpha,y}^2 ,
        \]
        其中 reflection-even hybridization 与稳定 pairing 选入
        \(A_{\mathrm{cone}}\)，\(P_{\alpha,y}\) 的 HS generators
        逐行取自 \(A_{\mathrm{group}}\)。在 decorated honeycomb、
        kagome 或 amorphous lattices 上，这允许研究 flat Majorana
        bands、interaction-shifted Andreev levels 与边界质量生成。
        </p>
        <p>
        本类的关键不是抽象 reflection 名称，而是卡片表中
        \(J_1=IX\) 对每个 \(gA\) block 的实际作用；下方 dimer 把
        hybridization、cone margin 与 pairing HS 三者的矩阵位置写明。
        </p>
        """,
    },
    "F-J2g-s1+q1-": {
        "title": "Kramers 拓扑超导平带中的集体配对涨落",
        "body": r"""
        <p>
        令 \(c_{i\uparrow},c_{i\downarrow}\) 是 Kramers partners，
        取 time-reversal-invariant \(H_{\mathrm{BdG}}\) 并加入
        \[
          -\frac12\sum_\alpha U_\alpha
          \left[\sum_{ij}F_{\alpha,ij}
          (c_{i\uparrow}^+c_{j\downarrow}^+
          -c_{i\uparrow}c_{j\downarrow})\right]^2 .
        \]
        Kramers-even BdG stability block 放在
        \(A_{\mathrm{cone}}\)，pair quadratures 的实 HS 场放在
        \(A_{\mathrm{group}}\)。可选择窄带、Dirac 或 moiré-inspired
        hopping，研究预成对、赝能隙与 time-reversal-invariant
        topological superconductivity。
        </p>
        <p>
        这里 \(J_1^2=-I\) 就作用在真实 Kramers pair 上；下方两模
        模型是每个格点 form factor 的局部核，不再额外引入另一套
        “physical Kramers”来补证明。
        </p>
        """,
    },
    "F-iJ2g-s1-q1+": {
        "title": "相互作用 proximitized Dirac/Chern 格点的 parity 临界性",
        "body": r"""
        <p>
        将 superconducting dot 推广为
        \[
          H=H_{\mathrm{Dirac/Chern}}-\sum_i\Delta_i\Delta_{y,i}
          -\frac12\sum_{ij}U_{ij}Q_iQ_j,\qquad U\succeq0 .
        \]
        物理 pairing stability direction 属于本类
        \(A_{\mathrm{cone}}\)，charge HS directions 属于
        \(A_{\mathrm{group}}\)。这使有限温 AFQMC 可以同时处理拓扑
        normal band、proximity pairing 与 attractive charging
        fluctuations。
        </p>
        <p>
        值得测量的问题包括 parity-changing transitions、Andreev
        flat bands 与 interaction-driven topological changes。下方
        quantum dot 不是最终目标，而是每个局域 pairing/charge
        channel 的严格矩阵核。
        </p>
        """,
    },
    "F-iJ2g-s1-q1-": {
        "title": "磁性涨落与拓扑配对竞争的超导格点模型",
        "body": r"""
        <p>
        取
        \[
          H=H_{\mathrm{BdG}}[\Delta,K]
          +\frac12\sum_{\alpha}U_\alpha
          \left(\sum_i f_{\alpha i}S_{z,i}\right)^2 ,
          \qquad U_\alpha>0 .
        \]
        稳定 pairing block 是 \(A_{\mathrm{cone}}\)，纯虚
        spin-polarization HS generators 是
        \(A_{\mathrm{group}}\)。选择 Dirac、Chern 或多轨道窄带
        \(K\) 后，可研究磁性量子临界涨落如何重构 Andreev bands，
        以及是否诱导 nodal 或拓扑超导相。
        </p>
        <p>
        下方 superconducting atom 给出一个 \(S_z\) 通道的精确
        HS 对应；格点推广只允许卡片 \(P\)–\(K_P\) 表中列出的
        form factors。
        </p>
        """,
    },
    "F-iJ2g-s1+q1+": {
        "title": "reflection-protected 高阶拓扑超导体的相互作用角态",
        "body": r"""
        <p>
        在 reflection-symmetric 多轨道格子上取
        \[
          H=H_{\mathrm{HOTSC}}[\Delta,t]
          +\frac12\sum_\alpha U_\alpha
          (n_{\alpha,L}-n_{\alpha,R})^2 .
        \]
        reflection-even pairing/hybridization 选在
        \(A_{\mathrm{cone}}\)，左右极化的纯虚 HS 场列在
        \(A_{\mathrm{group}}\)。当 normal band 与 pairing mass
        形成高阶拓扑结构时，可用该类研究 corner Majorana modes、
        interaction-shifted boundary transitions 与反射破缺。
        </p>
        <p>
        \(\Delta>|t|\) 一类条件在格点上应替换为完整 contraction
        matrix 负定；下方 dimer 展示的是这一矩阵不等式的最小
        eigenvalue 检查。
        </p>
        """,
    },
    "F-iJ2g-s1+q1-": {
        "title": "Kramers 多轨道超导岛阵列与 moiré 窄带配对",
        "body": r"""
        <p>
        令每个单元含两个 Kramers components 与两个 orbitals，考虑
        \[
          H=\sum_{ij}\boldsymbol c_i^+K_{ij}\boldsymbol c_j
          -\sum_i\Delta_i\Delta_{y,i}
          -\frac12\sum_{ij}U_{ij}Q_iQ_j .
        \]
        \(K\) 可取 time-reversal-symmetric moiré-inspired 窄带；
        pairing stability block 属于 \(A_{\mathrm{cone}}\)，
        total-charge HS generators 属于
        \(A_{\mathrm{group}}\)。四个 annihilation modes 正是本物理
        realization 的 spin-orbital 内容。
        </p>
        <p>
        该模型可研究多轨道 Andreev multiplets、orbital-selective
        pseudogap、pair transfer 与 parity transitions。下方单岛公式
        逐项证明 charge field 与 pairing cone 的归属；格点 hopping
        必须继续满足同一张 \(P\)–\(K_P\) 表。
        </p>
        """,
    },
}


MAXIMAL_ONLY_MODEL_CATALOG: dict[str, dict[str, str]] = {
    "s1+_q1-_s2+_q2+_r-": {
        "title": "相反 Chern 带中的相互作用 Kramers 费米子",
        "body": r"""
        <p>
        令 \(\psi_i=(c_{i\uparrow},c_{i\downarrow})^T\)，并令
        \(S_0=S_0^T\)、\(F_a=F_a^T\) 是实对称格点矩阵，
        \(R_z=-R_z^T\) 是实反对称格点矩阵。考虑厄米模型
        \[
          H=\psi^+\!\left(S_0+i\sigma_z\otimes R_z\right)\psi
          +\frac U2\sum_a
          \left(\psi^+\sigma_z\otimes F_a\,\psi\right)^2,
          \qquad U>0 .
        \]
        \(S_0\) 可包含实 hopping、无序和轨道势；
        \(i\sigma_z\otimes R_z\) 给两个 Kramers components 相反的
        Peierls phases，可实现相反 Chern 数、量子自旋霍尔带或
        time-reversal-symmetric moiré flat bands。\(F_a\) 可选为局域
        flavor density，也可选成有限程 form factor，以研究磁性、
        excitonic order 与拓扑 Mott 转变。
        </p>
        <p>
        每个正的平方用
        \[
          e^{-\Delta\tau U O_a^2/2}
          =\int\frac{d\phi_a}{\sqrt{2\pi}}e^{-\phi_a^2/2}
          e^{\,i\sqrt{\Delta\tau U}\phi_aO_a}
        \]
        分解。采用本卡片的
        \(J_1=I_{\rm Nambu}\otimes i\sigma_y\)、
        \(J_2=I_{\rm Nambu}\otimes\sigma_x\)，固定项与场项为
        \[
        \begin{aligned}
          A_0&=-\Delta\tau\left[
          ZI\otimes S_0+i\,IZ\otimes R_z\right],\\
          A_{\rm HS}(\phi)
          &=i\sqrt{\Delta\tau U}\sum_a\phi_a\,ZZ\otimes F_a .
        \end{aligned}
        \]
        对照本卡片的最终系数表：
        \(ZI\otimes S_0\) 属于 \(ZI{:}R_S\)，
        \(iIZ\otimes R_z\) 属于 \(IZ{:}iR_A\)，
        \(iZZ\otimes F_a\) 属于 \(ZZ{:}iR_S\)；三者全都在
        maximal-subgroup 李代数中。
        </p>
        <p class="result">
        <strong>逐构型无符号证明。</strong>
        \(\Theta=(i\sigma_y)\mathcal K\) 满足
        \(\Theta^2=-I\)，每个时间片及其
        有序乘积 \(\mathcal B\) 都与 \(\Theta\) 对易。非实本征值成
        \(\lambda,\bar\lambda\) 对，实本征值具有偶数重数，故
        \[
          \det(I+\mathcal B)
          =\prod_{\{\lambda,\overline\lambda\}}|1+\lambda|^2
           \prod_{\lambda\in\mathbb R}(1+\lambda)^{2m_\lambda}\geq0 .
        \]
        第一个乘积对每一对非实共轭本征值只取一次。
        费米 Fock space 有限，所以这里不需要
        \(\eta A+A^\dagger\eta<0\) 来控制收敛；等号传播已经给出完整
        grand-canonical AFQMC 权重。
        </p>
        """,
    },
    "s1+_q1-_s2-_q2+_r+": {
        "title": "纯 spin-orbit Kramers Dirac 格点与相互作用质量生成",
        "body": r"""
        <p>
        仍取两分量 \(\psi\)，令
        \(R_x=-R_x^T\)、\(R_z=-R_z^T\) 为实反对称 hopping matrices，
        \(F_a=F_a^T\) 为实对称 form factors。模型
        \[
          H=\psi^+i(\sigma_x\otimes R_x+\sigma_z\otimes R_z)\psi
          +\frac U2\sum_a
          \left(\psi^+\sigma_y\otimes F_a\,\psi\right)^2,
          \qquad U>0
        \]
        是厄米的。适当选择 \(R_x,R_z\) 可产生 Kramers Dirac cones、
        nodal spin-orbit semimetals 或近乎平坦的 helical bands；
        \(F_a\) 则控制 interaction-generated mass、nematicity 与
        superconducting competition。该类别不允许普通 scalar chemical
        potential，因而自然描述 particle-hole-symmetric filling。
        </p>
        <p>
        同一正测度 Gaussian 分解给出
        \[
        \begin{aligned}
          A_0&=-i\Delta\tau
          (IX\otimes R_x+IZ\otimes R_z),\\
          A_{\rm HS}(\phi)&=
          \sqrt{\Delta\tau U}\sum_a\phi_a\,IY\otimes F_a .
        \end{aligned}
        \]
        这里 \(IX{:}iR_A\)、\(IZ{:}iR_A\) 和 \(IY{:}R_S\)
        都在本卡片列出的 maximal-subgroup 生成元中。场项的
        \(IY\otimes F_a\) 对应 \(i\psi^+\sigma_yF_a\psi\)，所以正好是
        repulsive-square HS 指数，而不是非厄米原 Hamiltonian。
        </p>
        <p class="result">
        <strong>逐构型无符号证明。</strong>
        \(J_1\mathcal K=(I_{\rm Nambu}\otimes i\sigma_y)\mathcal K\)
        给出 Kramers anti-linear symmetry；与 \(J_2\mathcal K\)
        一起变到 Majorana 基底后，
        两者属于反对易的 \(\{T^+,T^-\}\) 类。每个有序乘积的 Majorana
        weight 分解为一对互为复共轭的因子，
        \(W(\phi)=w(\phi)\overline{w(\phi)}=|w(\phi)|^2\geq0\)。
        这是 maximal-subgroup 正性，不依赖负定收缩方向。
        </p>
        """,
    },
    "s1-_q1-_s2+_q2+_r+": {
        "title": "相关双轨道 singlet-triplet 拓扑配对网络",
        "body": r"""
        <p>
        令 \(\psi=(c_1,c_2)^T\) 表示两个轨道或两个 layer。
        取 \(S_\Delta=S_\Delta^T\)、\(F_a=F_a^T\) 实对称，
        \(R_\Delta=-R_\Delta^T\) 实反对称，并定义两个反对称 pairing
        matrices
        \[
          \Delta_s=i(i\sigma_y)\otimes S_\Delta,\qquad
          \Delta_t=i\sigma_z\otimes R_\Delta .
        \]
        二者都满足 \(\Delta_{s,t}^T=-\Delta_{s,t}\) 且
        \(\Delta_{s,t}^\dagger=\Delta_{s,t}\)。考虑
        \[
        \begin{aligned}
          H={}&\frac12\left[
          \psi^T(\Delta_s+\Delta_t)\psi+
          \psi^{+T}(\Delta_s+\Delta_t)\psi^+\right]\\
          &+\frac U2\sum_a
          \left(\psi^+\sigma_z\otimes F_a\,\psi\right)^2 ,
          \qquad U>0 .
        \end{aligned}
        \]
        这是厄米的 two-orbital BdG lattice。改变
        \(S_\Delta,R_\Delta\) 的键结构可研究 singlet 与 odd-parity
        triplet pairing 的竞争、higher-order Majorana boundary modes
        及 interaction-driven changes of BdG topology。
        </p>
        <p>
        在本卡片的 Nambu 顺序中，
        \[
        \begin{aligned}
          A_0&=-i\Delta\tau
          (XY\otimes S_\Delta+XZ\otimes R_\Delta),\\
          A_{\rm HS}(\phi)&=
          i\sqrt{\Delta\tau U}\sum_a\phi_a\,ZZ\otimes F_a .
        \end{aligned}
        \]
        固定项分别属于 \(XY{:}iR_S\)、\(XZ{:}iR_A\)，场项属于
        \(ZZ{:}iR_S\)；本卡片的最终表显示三者都在 maximal subgroup。
        因此时间片含真正的 Hermitian pairing，而不是为了满足矩阵关系
        引入非厄米 Hamiltonian。
        </p>
        <p class="result">
        <strong>逐构型无符号证明。</strong>
        这里 \(J_1\mathcal K\) 混合 particle 与 hole；它不应被误称为
        电子的普通 time reversal。把 \(J_1\mathcal K,J_2\mathcal K\)
        同时变到 Majorana basis 后，
        它们是反对易的 \(\{T^+,T^-\}\) 对。该结构把 Gaussian trace
        分成互为复共轭的两个 Majorana sectors，所以
        \(W=|w|^2\geq0\)，并覆盖有 pairing 的全部辅助场历史。
        </p>
        """,
    },
    "s1-_q1-_s2-_q2+_r-": {
        "title": "相互作用 p-wave Majorana 平带网络",
        "body": r"""
        <p>
        这一类的最小 \(m=1\) maximal-subgroup 李代数为零；要得到非平凡
        格点模型必须取至少两个空间轨道。令
        \(R_\Delta=-R_\Delta^T\)、\(R_p=-R_p^T\) 是实反对称矩阵，并定义
        \[
          H_0=\frac12\left(
          c^T iR_\Delta c+c^{+T}iR_\Delta c^+\right),\qquad
          O_p=-i\,c^+R_pc .
        \]
        \(H_0\) 与 \(O_p\) 都是 Hermitian。模型
        \[
          H=H_0+\frac U2\sum_p O_p^2,\qquad U>0
        \]
        描述 particle-hole-symmetric p-wave pairing network 与
        current fluctuations。取 \(R_\Delta\) 为有向 kagome、honeycomb
        或 amorphous graph 的邻接矩阵，可研究 Majorana flat bands、
        disorder topology 与 interaction-driven current order。
        </p>
        <p>
        Gaussian HS 分解后
        \[
          A_0=-\Delta\tau\,X\otimes iR_\Delta,\qquad
          A_{\rm HS}(\phi)=
          \sqrt{\Delta\tau U}\sum_p\phi_p\,I\otimes R_p .
        \]
        它们恰好对应本卡片的 \(X{:}iR_A\) 与 \(I{:}R_A\) 两行。
        后者代表 \(iO_p\)，所以辅助场测度为正，而原 Hamiltonian 保持
        Hermitian。
        </p>
        <p class="result">
        <strong>逐构型无符号证明。</strong>
        \(J_1=i\sigma_y\)、\(J_2=\sigma_z\) 在 Nambu 空间给出该行五条
        关系。变到 Majorana basis 后是反对易的
        \(\{T^+,T^-\}\) anti-linear symmetry pair，所有时间片都在
        maximal subgroup 中，Gaussian trace 为
        \(|w(\phi)|^2\geq0\)。费米 Fock space 有限；即使
        contraction inequality 只能取等号，也没有玻色高占据态发散。
        </p>
        """,
    },
}


def render_physical_model(class_name: str) -> str:
    model = MODEL_CATALOG[class_name]
    program = STRICT_RESEARCH_PROGRAMS[class_name]
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
        scope = (
            "完整 canonical fixed-"
            r"\(N\) sign-free 构造；固定粒子数权重是有限阶 character，"
            "不使用 grand-canonical determinant 公式；不存在一个来自稳定 "
            "Hermitian 二次玻色 Hamiltonian 的零场生成元，使 "
            "grand-canonical 迹收敛并同时满足同一个 "
            r"\(\eta=iJ_2g\) 的收缩不等式"
        )
    else:
        scope = r"费米物理 HS slice；按标准传播矩阵 \(e^A\) 条件检验"
    return (
        '<section class="model-example">'
        f'<p class="model-title"><strong>物理模型：{program["title"]}</strong></p>'
        f'<p class="model-scope"><strong>已经证明的结论：</strong>{scope}</p>'
        '<p class="small">'
        '卡片顶部的 \\(P\\)-\\(K_P\\) 表属于该类的最小 Pauli 代表。'
        '下面的物理模型有时采用同一五条关系的另一组适配 '
        '\\(J_1,J_2\\)，以便让 particle/hole、轨道和格点指标具有直接'
        '物理意义。两组代表不能按 Pauli word 逐字比较。下方折叠栏中的'
        '最小 HS building block 已经用其自身列出的 '
        '\\(J_1,J_2,g,\\eta\\) 重新检验，数值残差记录在 '
        '<a href="tables/physical_hs_slice_checks.csv">'
        'physical_hs_slice_checks.csv</a>；上面的格点推广则按本卡 '
        '\\(P\\)-\\(K_P\\) 表逐项选取方向，新增任意 hopping、pairing '
        '或 form factor 时仍必须保持同一张表的全部条件。'
        '</p>'
        f'{program["body"]}'
        '<details><summary>最小 HS building block 与逐矩阵核对</summary>'
        f'{model["body"]}'
        f"{scalar_note}"
        '</details>'
        "</section>"
    )


def render_maximal_only_model(class_id: str) -> str:
    model = MAXIMAL_ONLY_MODEL_CATALOG[class_id]
    return (
        '<section class="model-example">'
        f'<p class="model-title"><strong>物理模型：{model["title"]}</strong></p>'
        '<p class="model-scope"><strong>已经证明的结论：</strong>'
        '费米 maximal-subgroup 逐构型无符号；不要求负定收缩方向</p>'
        f'{model["body"]}'
        '</section>'
    )
