# @feature classify_ad_component
# @purpose Classify paid components and promotions while protecting organic content and comments
# @abi bf-host-v1
# @inputs enabled and validated context followed by Boolean substring facts in contracts/ad_component_inputs.json order
# @outputs 1 byte; 0=PASS; 1=SUPPRESS_COMPONENT
# @cells 0=enabled; 1=context; 2=exception; 3=match; 4=scratch; 5=doodle; 6=product
# @invariant every input is consumed once; all decisions are executable Brainfuck; output is Boolean
# @safety typed host validates exact Boolean input and exact one byte reply; unknown context is PASS
# @section enabled_and_context
,>,>>
# @note exception substring |comment.
,[[-]<[-]+>]< >
# @note exception substring comment_thread
,[[-]<[-]+>]< >
# @note exception substring home_video_with_context
,[[-]<[-]+>]< >
# @note exception substring library_recent_shelf
,[[-]<[-]+>]< >
# @note exception substring related_video_with_context
,[[-]<[-]+>]< >
# @note positive substring carousel_ad
>,[[-]<[-]+>]<
# @note positive substring _ad_with
>,[[-]<[-]+>]<
# @note positive substring _buttoned_layout
>,[[-]<[-]+>]<
# @note positive substring ads_video_with_context
>,[[-]<[-]+>]<
# @note positive substring banner_text_icon
>,[[-]<[-]+>]<
# @note positive substring brand_video_shelf
>,[[-]<[-]+>]<
# @note positive substring brand_video_singleton
>,[[-]<[-]+>]<
# @note positive substring carousel_footered_layout
>,[[-]<[-]+>]<
# @note positive substring carousel_headered_layout
>,[[-]<[-]+>]<
# @note positive substring compact_landscape_image_layout
>,[[-]<[-]+>]<
# @note positive substring composite_concurrent_carousel_layout
>,[[-]<[-]+>]<
# @note positive substring full_width_portrait_image_layout
>,[[-]<[-]+>]<
# @note positive substring full_width_square_image_carousel_layout
>,[[-]<[-]+>]<
# @note positive substring full_width_square_image_layout
>,[[-]<[-]+>]<
# @note positive substring hero_promo_image
>,[[-]<[-]+>]<
# @note positive substring image_button_group_layout
>,[[-]<[-]+>]<
# @note positive substring landscape_image_carousel_layout
>,[[-]<[-]+>]<
# @note positive substring landscape_image_wide_button_layout
>,[[-]<[-]+>]<
# @note positive substring primetime_promo
>,[[-]<[-]+>]<
# @note positive substring product_details
>,[[-]<[-]+>]<
# @note positive substring shopping_timely_shelf.
>,[[-]<[-]+>]<
# @note positive substring square_image_layout
>,[[-]<[-]+>]<
# @note positive substring text_image_button_layout
>,[[-]<[-]+>]<
# @note positive substring text_image_no_button_layout
>,[[-]<[-]+>]<
# @note positive substring video_display_button_group_layout
>,[[-]<[-]+>]<
# @note positive substring video_display_carousel_button_group_layout
>,[[-]<[-]+>]<
# @note positive substring video_display_carousel_buttoned_short_dr_layout
>,[[-]<[-]+>]<
# @note positive substring video_display_full_buttoned_short_dr_layout
>,[[-]<[-]+>]<
# @note positive substring video_display_full_layout
>,[[-]<[-]+>]<
# @note positive substring watch_metadata_app_promo
>,[[-]<[-]+>]<
# @note positive substring product_sticker.e
>,[[-]<[-]+>]<
# @note positive substring shopping_overlay.e
>,[[-]<[-]+>]<
# @note positive substring shopping_description_item.e
>,[[-]<[-]+>]<
# @note positive substring shopping_description_shelf.e
>,[[-]<[-]+>]<
# @note positive substring cta_shelf_card
>,[[-]<[-]+>]<
# @note positive substring premium_upsell
>,[[-]<[-]+>]<
# @note positive substring premium_promo
>,[[-]<[-]+>]<
# @note positive substring subscription_promo
>,[[-]<[-]+>]<
# @note positive substring paid_product_shelf
>,[[-]<[-]+>]<
# @section statement_banner_except_doodle
>,>,[[-]<[-]>]<[[-]<[-]+>]<
# @section exceptions_win
<[[-]>[-]<]>
# @section require_enabled_and_validated_context
<<<[->>>[->>>+<<<]<<<]>>>>>>[-<<<+>>>]<<<
<<[->>[->>>+<<<]<<]>>>>>[-<<<+>>>]<<<
# @section emit
.
