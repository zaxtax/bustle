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
  - [x] implemement remaining TODOs in operation execution
  - [ ] for initialization, extract string constants from I/O examples
  - [x] rectify the DSL to match the benchmarks
  - [x] convert property lists from Appendix C
- [ ] implement ML add-ons (Algorithm 1 including blue lines)
  - [x] scaffold the blue lines
  - [x] settle on shapes for `s_io` and `s_vo`, the interfaces between `propertySignature` and `reweightWithModel`
  - [x] implement `propertySignature`
  - [ ] support multiple inputs in `propertySignature`
  - [x] implement `reweightWithModel`
  - [x] consider reweighting for the initial values
  - [x] learn model
  - [ ] use trained model
- [ ] record some metrics (e.g. the number of subexpressions evaluated) during synthesis to compare approaches
- [ ] re-add the initial string constants and see whether the test cases pass with the ML
- [x] write parser for string DSL
- [x] write a pretty printer
- [ ] use the benchmarks mentioned in the paper
  - [x] Appendix B
    - [ ] add some reasonable test cases for each program in the benchmark set 
  - [ ] [SysGus](https://github.com/SyGuS-Org/benchmarks)
- [x] generate data from synthesis search (last paragraph of Section 3.1)
  - [ ] generate interesting inputs

### Best practices

- [x] build a (DSL-parameterized) program executor
- [ ] improve the DSL interface so that implementations of DSLs are more concise?
- [ ] use a proper Python testing framework?
