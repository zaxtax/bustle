# bustle
a re-creation of _BUSTLE: Botton-up Program Synthesis Through Learning-Guided Exploration_, an [ICLR 2021 paper](https://openreview.net/forum?id=yHeg4PbFHh) by Odena et al.

## TODOs

- [x] implement basic bottom-up synthesis (Algorithm 1 without blue lines)
- [x] test implementation on tiny arithmetic language
- [x] add types to DSL operations and extend tiny arithmetic language with boolean types and `if` operation
- [x] allow multiple DSLs
- [ ] support dynamic errors (such as out-of-bound string access) in DSL execution (probably just discount those expressions)
- [ ] improve the DSL interface so that implementations of DSLs are more concise
- [ ] implement string manipulation DSL (Figure 1)
- [ ] implement ML add-ons (Algorithm 1 including blue lines)
- [ ] use the benchmarks mentioned in the paper
  - [ ] Appendix B
  - [ ] [SysGus](https://github.com/SyGuS-Org/benchmarks)
- [ ] generate data from synthesis search (last paragraph of Section 3.1)
