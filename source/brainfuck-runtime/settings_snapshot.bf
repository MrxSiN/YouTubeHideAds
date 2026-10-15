# @feature settings_snapshot
# @purpose Turn stored preference bits into effective feature switches, owning defaults and the master gate.
# @abi bf-host-v1
# @inputs 10 Boolean bytes as (present, value) pairs in order: master, video_ads, component_ads, premium_promotions, fullscreen_promotions
# @outputs 9 bytes: raw effective master, video, component, premium, fullscreen; then master-gated video, component, premium, fullscreen
# @cells 0..4=raw effective switches; 9=else flag for the master gate; 10=present; 11=value; 12=result under construction
# @invariant a missing preference means ON; cells 10..12 are zero between pairs; pointer rests on cell 10 between pairs
# @safety host passes exact Boolean bytes from SharedPreferences; fixed input length; no loop depends on unbounded input
# @status runtime: called on every Activity focus change, never on a hook hot path

# Defaults live here, not in the host. Every switch ships ON, because a user
# who installed an ad blocker presumably did not want to opt in five times.

# @section park_on_scratch
>>>>>>>>>>

# @section pair_master
# Cell 12 starts at 1 (the default). A present preference replaces it with
# the stored value; an absent one leaves the default alone.
,>,>+<<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<<<<+>>>>>>>>>>>>]
<<

# @section pair_video_ads
,>,>+<<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<<<+>>>>>>>>>>>]
<<

# @section pair_component_ads
,>,>+<<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<<+>>>>>>>>>>]
<<

# @section pair_premium_promotions
,>,>+<<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<+>>>>>>>>>]
<<

# @section pair_fullscreen_promotions
,>,>+<<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<+>>>>>>>>]
<<

# @section emit_raw_switches
# The settings page shows these, so a feature remembers its own state while
# the master switch is off.
<<<<<<<<<<
.>.>.>.>.

# @section arm_else_flag
>>>>>+<<<<<<<<<

# @section master_on_branch
# Master ON: the hooks get the feature switches untouched. Cell 0 is spent
# afterwards, which is fine; it already said what it had to say.
[>.>.>.>.<<<<[-]>>>>>>>>>-<<<<<<<<<]

# @section master_off_branch
# Master OFF: four zeros from the clean scratch cell. No feature sneaks through.
>>>>>>>>>
[->....<]
