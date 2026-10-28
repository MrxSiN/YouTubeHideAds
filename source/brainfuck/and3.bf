# @feature and3
# @purpose Three-input Boolean AND shared by every gate whose decision is "own switch AND fact AND valid context".
# @abi bfc_call_v1
# @inputs 0=enabled (0 or 1); 1=fact (0 or 1); 2=context_valid (0 or 1)
# @outputs 1 byte; 0=PASS; 1=ACT (suppress, remove, handle, select or allow background capability, per caller)
# @cells 0=accumulator; 1=next input; 2=product and action; all 8bit wrapping
# @invariant pointer returns to cell 0 after each AND; cells 0 and 2 are always Boolean before emission
# @safety host MUST validate all input bits; invalid or missing inputs MUST fail closed; no host action without valid ABI
# @note callers: Premium upsell, Shorts ad slot, Playables, fullscreen swipe, feed section, AI channel, original audio, background playback

# @section seed
# A single input byte decides whether policy evaluation can proceed. No feature constants here.
,

# @section gate_1_fact
# Boolean multiply. Consume the accumulator and evidence into a scratch cell.
>,<[->[->+<]<]>>[-<<+>>]<<

# @section gate_2_context_valid
# Boolean multiply. Consume the accumulator and evidence into a scratch cell.
>,<[->[->+<]<]>>[-<<+>>]<<

# @section emit_action
# Cell 2 is zero. Zero input yields PASS; nonzero input becomes the ABI action code.
[->>+<<]>>.
