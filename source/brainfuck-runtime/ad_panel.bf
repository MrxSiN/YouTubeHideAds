# @feature suppress_ad_panel
# @purpose Suppress shopping and Premium engagement panels without touching ordinary panels
# @abi bf-panel-bits-v1
# @inputs 0=popup enabled; 1=premium enabled; 2=PAproduct substring; 3=jumpahead substring; all Boolean
# @outputs exactly one byte; 0=PASS; 1=SUPPRESS_PANEL
# @cells 0=popup; 1=premium; 2=shopping; 3=jumpahead; 5=match; 6=output
# @invariant all policy lives in the eight command stream; no platform calls
# @safety host validates the panel field type and exact one byte reply; missing evidence passes

# @section read_facts
,>,>,>,
# @section premium_and_jumpahead
<<[->>[->>+<<]<<]>>>>
# @section shopping_or_premium
<<<[[-]>>>[-]+<<<]
# @section require_popup_enabled
<<[->>>>>[->+<]<<<<<]>>>>>>.
