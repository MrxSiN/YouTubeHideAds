# @feature sponsor_settings
# @purpose Own SponsorBlock defaults and the master gate
# @abi bf-sponsor-settings-v1
# @inputs master Boolean, then nine (present,value) Boolean pairs: enabled,sponsor,selfpromo,interaction,intro,outro,preview,filler,music_offtopic
# @outputs ten bytes: nine raw effective switches, then master AND enabled
# @cells 0..8=raw switches; 9=effective enabled; 10=master; 11=present; 12=value; 13=result; 15=copy; 16=product
# @invariant scratch cells are zero between pairs; defaults exist only in the command stream
# @safety exact Boolean input and ten-byte output are required

# @section read_master
>>>>>>>>>>,
>
# @section enabled
,>,>+<<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<<<<<+>>>>>>>>>>>>>]
<<
# @section sponsor
,>,>+<<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<<<<+>>>>>>>>>>>>]
<<
# @section selfpromo
,>,>+<<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<<<+>>>>>>>>>>>]
<<
# @section interaction
,>,><<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<<+>>>>>>>>>>]
<<
# @section intro
,>,><<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<<+>>>>>>>>>]
<<
# @section outro
,>,><<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<<+>>>>>>>>]
<<
# @section preview
,>,><<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<<+>>>>>>>]
<<
# @section filler
,>,><<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<<+>>>>>>]
<<
# @section music_offtopic
,>,><<
[->>[-]<[->+<]<]
>[-]>
[-<<<<<+>>>>>]
<<
# @section copy_enabled_and_gate_with_master
<<<<<<<<<<<
[->>>>>>>>>+>>>>>>+<<<<<<<<<<<<<<<]
>>>>>>>>>>>>>>>[-<<<<<<<<<<<<<<<+>>>>>>>>>>>>>>>]
<<<<<[-<[->>>>>>>+<<<<<<<]>]
<[-]>>>>>>>[-<<<<<<<+>>>>>>>]
# @section emit
<<<<<<<<<<<<<<<<.>.>.>.>.>.>.>.>.>.

