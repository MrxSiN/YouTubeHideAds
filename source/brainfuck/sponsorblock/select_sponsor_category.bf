# @feature select_sponsor_category
# @purpose Decide auto-skip eligibility for exactly one SponsorBlock category using eight settings and one-hot category evidence.
# @abi bf-host-v1
# @inputs 16 binary Boolean bytes, interleaved by category: setting_enabled[0], category_matches[0], ..., setting_enabled[7], category_matches[7]. Exactly one category_matches bit must be set; the host validates only the encoding.
# @outputs one action byte: PASS 00 when the category is disabled; CATEGORY_AUTO_SKIP 05 when the matching category is enabled
# @cells 0=accumulated eligible match; 1=current setting, then action; 2=current category-match bit
# @invariant cell 0 counts enabled selected categories; host one-hot validation guarantees the count is zero or one
# @safety all 16 input bytes must be Boolean, all eight category selectors must be one-hot; no network or player operation occurs here

# @section select_sponsor
# If this is the selected category AND its toggle is set, increment eligibility.
>,>,<[->[-<<+>>]<]<

# @section select_selfpromo
# If this is the selected category AND its toggle is set, increment eligibility.
>,>,<[->[-<<+>>]<]<

# @section select_interaction
# If this is the selected category AND its toggle is set, increment eligibility.
>,>,<[->[-<<+>>]<]<

# @section select_intro
# If this is the selected category AND its toggle is set, increment eligibility.
>,>,<[->[-<<+>>]<]<

# @section select_outro
# If this is the selected category AND its toggle is set, increment eligibility.
>,>,<[->[-<<+>>]<]<

# @section select_preview
# If this is the selected category AND its toggle is set, increment eligibility.
>,>,<[->[-<<+>>]<]<

# @section select_filler
# If this is the selected category AND its toggle is set, increment eligibility.
>,>,<[->[-<<+>>]<]<

# @section select_music_offtopic
# If this is the selected category AND its toggle is set, increment eligibility.
>,>,<[->[-<<+>>]<]<

# @section emit_category_action
# Translate the one-hot decision into a bounded action opcode, not a host-computed setting.
[->+++++<]>.
