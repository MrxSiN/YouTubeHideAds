# @feature suppress_video_slot
# @purpose Suppress a verified player ad slot only when playback transition is safe.
# @abi bfc_call_v1
# @inputs 0=enabled (0 or 1); 1=structural_ad_slot (0 or 1); 2=safe_player_transition (0 or 1); 3=channel_whitelisted (0 or 1)
# @outputs 1 byte; 0=PASS; 1=SUPPRESS_COMPONENT
# @cells 0=accumulator; 1=next input; 2=product and action; all 8bit wrapping
# @invariant pointer returns to cell 0 after each AND; cells 0 and 2 are always Boolean before emission
# @safety host MUST validate all input bits; invalid or missing inputs MUST fail closed; no host action without valid ABI

# @section seed
# A single input byte decides whether policy evaluation can proceed. No feature constants here.
,

# @section gate_1_structural_ad_slot
# Boolean multiply. Consume the accumulator and evidence into a scratch cell.
>,<[->[->+<]<]>>[-<<+>>]<<

# @section gate_2_safe_player_transition
# Boolean multiply. Consume the accumulator and evidence into a scratch cell.
>,<[->[->+<]<]>>[-<<+>>]<<

# @section respect_channel_whitelist
# Convert whitelist=0 to permit=1 and whitelist=1 to permit=0 on cell 1.
# This inversion, not the platform host, owns the channel exception rule.
>,>+<[->-<]>[<+>-]<<

# @section whitelist_gate
# Multiply by the inverted whitelist bit. Scratch cells remain bounded.
[->[->+<]<]>>[-<<+>>]<<

# @section emit_action
# Cell 2 is zero. Zero input yields PASS; nonzero input becomes the ABI action code.
[->>+<<]>>.
