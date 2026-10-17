# @feature classify_fullscreen_ad
# @abi bf-fullscreen-bits-v1
# @inputs 0=popup enabled; 1=interstitial marker; 2=existing component classifier decision
# @outputs 1 Boolean byte; popup AND interstitial OR existing decision
# @safety host validates Boolean facts and exact one byte reply
,>,<[->[->+<]<]>[-]>[[-]<+>],[[-]<[-]+>]<.
