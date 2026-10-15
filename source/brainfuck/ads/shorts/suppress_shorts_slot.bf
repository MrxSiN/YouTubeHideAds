# @feature suppress_shorts_slot
# @purpose Suppress a Shorts ad only for the current item generation.
# @abi bf-host-v1
# @inputs 0=enabled (0 or 1); 1=shorts_ad_slot (0 or 1); 2=current_generation_valid (0 or 1)
# @outputs 1 byte; 0=PASS; 1=SUPPRESS_COMPONENT
# @cells 0=accumulator; 1=next input; 2=product and action; all 8bit wrapping
# @invariant pointer returns to cell 0 after each AND; cells 0 and 2 are always Boolean before emission
# @safety host MUST validate all input bits; invalid or missing inputs MUST fail closed; no host action without valid ABI

# @section seed
# A single input byte decides whether policy evaluation can proceed. No feature constants here.
,

# @section gate_1_shorts_ad_slot
# Boolean multiply. Consume the accumulator and evidence into a scratch cell.
>,<[->[->+<]<]>>[-<<+>>]<<

# @section gate_2_current_generation_valid
# Boolean multiply. Consume the accumulator and evidence into a scratch cell.
>,<[->[->+<]<]>>[-<<+>>]<<

# @section emit_action
# Cell 2 is zero. Zero input yields PASS; nonzero input becomes the ABI action code.
[->>+<<]>>.
