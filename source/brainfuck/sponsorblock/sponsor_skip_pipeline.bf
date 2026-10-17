# @feature sponsor_skip_pipeline
# @purpose In one Brainfuck invocation, select SponsorBlock category authorization and gate a 64-bit seek destination; no host-supplied intermediate category decision.
# @abi bfc_call_v1
# @inputs First 16 category toggle/select Boolean bytes; then enabled, matching_generation, valid_segment_window, raw_playback_type, not_already_skipped; then 8 little-endian unsigned segment_end_milliseconds bytes.
# @outputs PASS (00) or SEEK_PLAYER (04) with verbatim 64-bit little-endian endpoint
# @cells 0=Brainfuck-owned category permission and seek conjunction; 1,2=gate scratch and action; 3..10=endpoint
# @invariant exactly one category selector; four remaining guards are Boolean; playback type 1 is verified VOD, every other type passes without seeking
# @safety host validates the byte contract, positive signed-long endpoint and actual player generation before applying a seek

# @section category_selection
# The eight clauses are executable, one interleaved toggle AND selector clause per category.
>,>,<[->[-<<+>>]<]<>,>
,<[->[-<<+>>]<]<>,>,<[
->[-<<+>>]<]<>,>,<[->[
-<<+>>]<]<>,>,<[->[-<<
+>>]<]<>,>,<[->[-<<+>>
]<]<>,>,<[->[-<<+>>]<]
<>,>,<[->[-<<+>>]<]<
# @section clear_category_scratch
# Last selected category can leave a byte in cell2 even when its toggle is off. Clear cells1/2 without changing cell0.
>[-]>[-]<<

# @section remaining_runtime_predicates_and_binary_seek
# @note enabled
>,<[->[->+<]<]>>[-<<+>>]<<
# @note matching generation
>,<[->[->+<]<]>>[-<<+>>]<<
# @note Brainfuck window result
>,<[->[->+<]<]>>[-<<+>>]<<
# @note raw playback type equals verified VOD value 1; unknown and live types cannot seek
>,->+<[[-]>[-]<]>[-<+>]<<[->[->+<]<]>>[-<<+>>]<<
# @note not already skipped
>,<[->[->+<]<]>>[-<<+>>]<<
# @note endpoint and exact action reply
>>>,>,>,>,>,>,>,>,<<<<<<<<<<>[-]<[->+>++++<<]>>.<[->>.>.>.>.>.>.>.>.<<<<<<<<<]
