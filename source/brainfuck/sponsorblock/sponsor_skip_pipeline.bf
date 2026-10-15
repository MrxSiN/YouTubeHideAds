# @feature sponsor_skip_pipeline
# @purpose In one Brainfuck invocation, select SponsorBlock category authorization and gate a 64-bit seek destination; no host-supplied intermediate category decision.
# @abi bf-host-v1
# @inputs First 16 one-hot category toggle/select Boolean bytes; then 5 Boolean flags enabled, matching_generation, valid_segment_window, not_live, not_already_skipped; then 8 little-endian unsigned segment_end_milliseconds bytes.
# @outputs PASS (00) or SEEK_PLAYER (04) with verbatim 64-bit little-endian endpoint
# @cells 0=Brainfuck-owned category permission and seek conjunction; 1,2=gate scratch and action; 3..10=endpoint
# @invariant exactly one category selector, validated by the host; five remaining guards are Boolean; pointer ends at cell 1
# @safety host validates 21 Boolean bytes, category one-hot, endpoint positive signed 64-bit, generation; positive seeks cannot execute without actual Android runtime proofs

# @section category_selection
# The eight clauses are executable, copied exactly from select_sponsor_category.bf excluding the output emitter.
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
>,<[->[->+<]<]>>[-<<+>>]<<>,<[->[->+<]<]>>[-<<+>>]<<>,<[->[->+<]<]>>[-<<+>>]<<>,<[->[->+<]<]>>[-<<+>>]<<>,<[->[->+<]<]>>[-<<+>>]<<>>>,>,>,>,>,>,>,>,<<<<<<<<<<>[-]<[->+>++++<<]>>.<[->>.>.>.>.>.>.>.>.<<<<<<<<<]
