# bustle
a re-creation of _BUSTLE: Botton-up Program Synthesis Through Learning-Guided Exploration_, an [ICLR 2021 paper](https://openreview.net/forum?id=yHeg4PbFHh) by Odena et al.

## TODOs

### Paper

- [x] [`bustle`](bustle.py) implement basic bottom-up synthesis (Algorithm 1 without blue lines)
- [x] test implementation on tiny arithmetic language
- [x] add types to DSL operations and extend tiny arithmetic language with boolean types and `if` operation
- [x] allow multiple DSLs
- [x] support dynamic errors (such as division by zero) in DSL execution
- [x] [`stringdsl`](stringdsl.py) implement string manipulation DSL (Figure 1)
  - [ ] implemement remaining TODOs in operation execution
  - [ ] for initialization, extract string constants from I/O examples
  - [ ] rectify the DSL to match the benchmarks
  - [x] convert property lists from Appendix C
- [ ] implement ML add-ons (Algorithm 1 including blue lines) (Z)
  - [x] scaffold the blue lines
  - [ ] implement `propertySignature`
  - [ ] implement `reweightWithModel`
  - [ ] learn model
- [ ] re-add the initial string constants and see whether the test cases pass with the ML
- [ ] write parser for string DSL
- [ ] use the benchmarks mentioned in the paper
  - [ ] Appendix B
  - [ ] [SysGus](https://github.com/SyGuS-Org/benchmarks)
- [ ] generate data from synthesis search (last paragraph of Section 3.1)

### Best practices

- [ ] build a (DSL-paramterized) program executor for the synthesized expressions
- [ ] improve the DSL interface so that implementations of DSLs are more concise?
- [ ] use a proper Python testing framework?
