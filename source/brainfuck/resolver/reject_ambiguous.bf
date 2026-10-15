# @feature reject_ambiguous
# @purpose Reject ambiguous and structurally invalid resolver candidates.
# @abi bf-host-v1
# @inputs 0=resolver_active (0 or 1); 1=multiple_equally_scored (0 or 1); 2=no_unique_valid_match (0 or 1)
# @outputs 1 byte; 0=PASS; 3=REJECT_RESOLUTION
# @cells 0=accumulator; 1=next input; 2=product and action; all 8bit wrapping
# @invariant pointer returns to cell 0 after each AND; cells 0 and 2 are always Boolean before emission
# @safety host MUST validate all input bits; invalid or missing inputs MUST fail closed; no host action without valid ABI

# @section seed
# A single input byte decides whether policy evaluation can proceed. No feature constants here.
,

# @section gate_1_multiple_equally_scored
# Boolean multiply. Consume the accumulator and evidence into a scratch cell.
>,<[->[->+<]<]>>[-<<+>>]<<

# @section gate_2_no_unique_valid_match
# Boolean multiply. Consume the accumulator and evidence into a scratch cell.
>,<[->[->+<]<]>>[-<<+>>]<<

# @section emit_action
# Cell 2 is zero. Zero input yields PASS; nonzero input becomes the ABI action code.
[->>+++<<]>>.
