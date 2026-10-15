# @feature authorize_seek
# @purpose Authorize a generation-bound auto-skip and choose its 64-bit endpoint from validated segment metadata.
# @abi bf-host-v1
# @inputs 0..5 are Boolean: enabled; category_auto_skip; matching_video_generation; valid_segment_window; not_live; not_already_skipped. Bytes 6..13 are unsigned little-endian segment_end_milliseconds.
# @outputs 1 byte PASS (00) or 9 bytes: SEEK_PLAYER (04) followed by the original 64-bit little-endian end timestamp
# @cells 0=gate; 1=emission_gate; 2=action; 3..10=segment_end_le; remaining cells remain zero
# @invariant gate is Boolean after the six predicates; pointer returns to cell 0 before splitting into action and emission gate
# @safety host validates six Boolean bytes, complete timestamp, generation and endpoint bounds; BF emits timestamp ONLY when all six gates pass

# @section first_gate
,

# @section combine_auto_skip
>,<[->[->+<]<]>>[-<<+>>]<<

# @section combine_video_generation
>,<[->[->+<]<]>>[-<<+>>]<<

# @section combine_valid_segment_window
>,<[->[->+<]<]>>[-<<+>>]<<

# @section combine_not_live
>,<[->[->+<]<]>>[-<<+>>]<<

# @section combine_not_previously_skipped
>,<[->[->+<]<]>>[-<<+>>]<<

# @section collect_destination
# Eight explicit Brainfuck reads: no annotations, templates or host-side byte-copy policy.
# The bytewise endpoint is preserved even when it contains NUL or 0xFF.
>>>,>,>,>,>,>,>,>,
<<<<<<<<<<

# @section split_action_and_emit_gate
# Consume cell 0: cell 1 receives the one-shot gate, cell 2 receives 4 or 0.
>[-]<
[->+>++++<<]
>>.

# @section emit_destination_only_for_authorized_seek
# A denied request emits exactly one PASS byte, never a dangling timestamp.
<[-
  >>.>.>.>.>.>.>.>.
  <<<<<<<<<
]
