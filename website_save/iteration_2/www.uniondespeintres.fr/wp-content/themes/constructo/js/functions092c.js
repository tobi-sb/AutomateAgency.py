"use strict";

function replaceUrlParam(url, paramName, paramValue) {
    if (paramValue == null)
        paramValue = '';
    var pattern = new RegExp('\\b(' + paramName + '=).*?(&|$)')
    if (url.search(pattern) >= 0) {
        return url.replace(pattern, '$1' + paramValue + '$2');
    }
    return url + (url.indexOf('?') > 0 ? '&' : '?') + paramName + '=' + paramValue
}

function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

jQuery.fn.isOnScreen = function() {
    var win = jQuery(window);

    var viewport = {
        top: win.scrollTop(),
        left: win.scrollLeft()
    };
    viewport.right = viewport.left + win.width();
    viewport.bottom = viewport.top + win.height();

    var bounds = this.offset();
    bounds.right = bounds.left + this.outerWidth();
    bounds.bottom = bounds.top + this.outerHeight();

    return (!(viewport.right < bounds.left || viewport.left > bounds.right || viewport.bottom < bounds.top || viewport.top > bounds.bottom));

};

jQuery.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    jQuery.each(a, function() {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

jQuery(function($) {
    /*-----------------------------------------------------------------------------------*/
    /*  Site search
    /*-----------------------------------------------------------------------------------*/

    $('.site-search-close').on('click', function() {
        $('.site-wrapper').removeClass('site-search-opened');
    });

    $('.site-search-toggle button').on('click', function() {
        if ($('.site-search').length) {
            if( !$('.site-search-opened').length ) {
              $(window).scrollTop(0);
            }

            $('.site-wrapper').toggleClass('site-search-opened');
        } else {
            $('.site-search-minimal').toggleClass('site-search-minimal--active');
        }
    });

    /*-----------------------------------------------------------------------------------*/
    /*  Mobile menu toggle
    /*-----------------------------------------------------------------------------------*/

    $('.navbar-toggle').on('click', function() {
      $('.site-navigation').toggleClass('site-navigation-opened');
        if ($('.site-navigation-opened').length) {
            var offset = $('.nav-wrap').height();

            if (window.innerWidth > 600) {
                offset += $('#wpadminbar').height();
            }

            $('.site-navigation-opened').css({
                'max-height': window.innerHeight - offset, 
            });
        }
    });

    /*-----------------------------------------------------------------------------------*/
    /*  Animated submenu
    /*-----------------------------------------------------------------------------------*/

    if (!$('.menu-item-depth-0').length) {
        $('.site-navigation > ul > li').addClass('menu-item-depth-0');
    }

    if ($('.site-search-toggle') && !$('.site-search-toggle').hasClass('hidden-sm')) {
        $('.cartwrap').addClass('cart-search-space');
    }

    function submenuHeight() {
        $('.menu-item-depth-0 > .sub-menu').each(function() {
            $(this).css({
                'display': 'none',
                'height': 'auto'
            });
            $(this).attr('data-height', $(this).height());
            $(this).attr('style', '');
        });
    }

    if (window.innerWidth > 991) {
        submenuHeight();
    }

    $(window).on('resize', submenuHeight);

    $('.menu-item-depth-0 > a').on('mouseenter', function() {
        if (window.innerWidth > 991) {
            var $subMenu = $(this).siblings('.sub-menu');
            $subMenu.css('height', $subMenu.attr('data-height'));
        }
    });

    $('.menu-item-depth-0 > .sub-menu').on('mouseenter', function() {
        if (window.innerWidth > 991) {
            $(this).css('height', $(this).attr('data-height'));
            $(this).css('overflow', 'visible');
        }
    });

    $('.menu-item-depth-0 > a').on('mouseleave', function() {
        if (window.innerWidth > 991) {
            var $subMenu = $(this).siblings('.sub-menu');
            $subMenu.css('height', -1);
        }
    });

    $('.menu-item-depth-0 > .sub-menu').on('mouseleave', function() {
        if (window.innerWidth > 991) {
            $(this).css('height', -1);
            $(this).css('overflow', '');
        }
    });

    /*-----------------------------------------------------------------------------------*/
    /*  Sticky
    /*-----------------------------------------------------------------------------------*/

    var topOffset;
    var $wpBar = $('#wpadminbar');
    var $siteHeader = $('.site-header');

    function changeTopOffset() {
      topOffset = $siteHeader.offset().top;

      if( $('.site-header-style-transparent').length && $('.top-bar').length ) {
          topOffset = $('.top-bar').innerHeight() + $('.nav-wrap').css('top').replace('px', '')*1;

          if (window.innerWidth < 600) {
              topOffset = $wpBar.height() +  $('.top-bar').innerHeight();
          }
      }

      if (window.innerWidth > 600) {
          topOffset -= $wpBar.height();
      }

      /* Full screen menu type */
      if ($('.site-header-style-full-width, .site-header-style-boxed').length) {
          if (window.innerWidth > 991) {
              topOffset += $('.preheader-wrap').height();
          } else {
              topOffset = 0;

              if (window.innerWidth < 600) {
                  topOffset += $('#wpadminbar').height();
              }

              if ($('.site-search-opened').length) {
                  topOffset += $('.site-search').height();
              }
          }

          if( $('.site-header-style-boxed').length ) {
              topOffset -= $('.nav-bar-wrapper').height() / 2;
          }
      }
    }

    function stickyHeader() {
      if($('.site-header-sticky').length && $(window).scrollTop() > topOffset) {
        $siteHeader.addClass('site-header-sticky-active');
      } else {
        $siteHeader.removeClass('site-header-sticky-active');
      }
    }

    if($('.site-header-sticky').length && $siteHeader.length) {
      $(window).on('resize', changeTopOffset);
      $(window).on('scroll', changeTopOffset);
      changeTopOffset();

      $(window).on('scroll', stickyHeader);
      stickyHeader();
    }

    /*-----------------------------------------------------------------------------------*/
    /*  Top bar
    /*-----------------------------------------------------------------------------------*/

    function topBarSize() {
      $('.top-bar .container').css('height', $('.top-bar-left').innerHeight() + $('.top-bar-right').innerHeight() + 15);
    }

    $('.top-bar-close').on('click', function() {
      if( !$('.top-bar .container').attr('style') ) {
        topBarSize();
        $('.top-bar').addClass('top-bar-show').removeClass('top-bar-hide');
      } else {
        $('.top-bar .container').attr('style', '');
        $('.top-bar').removeClass('top-bar-show').addClass('top-bar-hide');
      }

      $(this).trigger('blur');
    });

    $(window).on('resize', function() {
      if ($siteHeader.length) {
        changeTopOffset();
      }

      if( window.innerWidth > 991 ) {
        $('.top-bar .container').attr('style', '');
        $('.top-bar').removeClass('top-bar-show').removeClass('top-bar-hide');
      } else {
        if( $('.top-bar-show').length ) {
          topBarSize();
        }
      }
    });

    /*-----------------------------------------------------------------------------------*/
    /*	Megamenu
    /*-----------------------------------------------------------------------------------*/

    function megamenu() {
        $('.megamenu > .sub-menu').css('left', 'auto');

        if (window.innerWidth > 991) {
            $('.megamenu').each(function() {
                var left = $('.site-header  .container').offset().left - $(this).find('> .sub-menu').offset().left;
                $(this).find('> .sub-menu').css('left', left + 15);
            });
        }
    }

    if( $('.megamenu').length ) {
        megamenu();
        $(window).on('resize', megamenu);
    }

    /*-----------------------------------------------------------------------------------*/
    /*  Navigation links (smooth scroll)
    /*-----------------------------------------------------------------------------------*/

    $('.site-navigation a[href*="#"]:not([href="#"]):not([href*="="]), .anps-smooth-scroll').click(function(e) {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') ||
            location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                e.preventDefault();
                var $targetoffset = target.offset().top - $('.nav-wrap').outerHeight(true) + 20;

                $('html,body').animate({
                    scrollTop: $targetoffset
                }, 1000);
                return false;
            }
        }
    });

    $(window).on('load', function() {
        if(window.location.hash.length > 0) {
            setTimeout(function() {
                window.scrollTo(0, $(window.location.hash).offset().top);
            }, 1);
        }
    });

    /*-----------------------------------------------------------------------------------*/
    /*  Waypoints
    /*-----------------------------------------------------------------------------------*/

    if ($('body').hasClass('home')) {
        var navLinkIDs = '';

        $('.site-navigation a[href*="#"]:not([href="#"]):not([href*="="])').each(function(index) {
            if (navLinkIDs != "") {
                navLinkIDs += ", ";
            }
            var temp = $('.site-navigation a[href*="#"]:not([href="#"]):not([href*="="])').eq(index).attr('href').split('#');
            navLinkIDs += '#' + temp[1];
        });

        if (navLinkIDs) {
            $(navLinkIDs).waypoint(function(direction) {
                if (direction == 'down') {
                    $('.site-navigation a').parent().removeClass("current_page_item");
                    $('.site-navigation a[href="#' + $(this).attr('id') + '"]').parent().addClass('current_page_item');
                }
            }, {
                offset: 125
            });

            $(navLinkIDs).waypoint(function(direction) {
                if (direction == 'up') {
                    $('.site-navigation a').parent().removeClass("current_page_item");
                    $('.site-navigation a[href="#' + $(this).attr('id') + '"]').parent().addClass("current_page_item");
                }
            }, {
                offset: function() {
                    return -$(this).height() + 20;
                }
            });
        }
    }

    /* Tabs */
    $('.nav-tabs a').on('click', function(e) {
        e.preventDefault()
        $(this).tab('show')
    });

    /* Portfolio */

    /* Build pagination */

    function buildPagination() {
        var page = $('.isotope').attr('data-page');
        var perPage = $('.isotope').attr('data-per-page');
        var number = $('.isotope').attr('data-number');

        $('.portfolio-pagination').html('');
        for(var i = 1; i <= Math.ceil(number/perPage); i++) {
            var selectedClass = '';

            if (i === page*1) {
                selectedClass += ' portfolio-pagination-selected';
            }
            $('.portfolio-pagination').append('<button type="button" class="portfolio-pagination-item' + selectedClass + '">' + i + '</button>');
        }
    }

    function portfolioAjax() {
        $('.isotope').addClass('processing');

        var category = $('.filter .selected').attr('data-filter');

        if(category === '*') {
            category = '';
        }

        $.post(
            anps.ajaxurl,
            {
                'action': 'anps_portfolio_ajax',
                'per_page': $('.isotope').attr('data-per-page'),
                'category': category,
                'mobile_class': $('.isotope').attr('data-mobile-class'),
                'type': $('.isotope').attr('data-type'),
                'columns': $('.isotope').attr('data-columns'),
                'order': $('.isotope').attr('data-order'),
                'page': $('.portfolio-pagination-selected').html(),
                'orderby': $('.isotope').attr('data-orderby'),
            },
            function(response){
                var el = $(response).filter('.portfolio');

                var filterParam = getUrlParameter('filter');
                if (filterParam === undefined) {
                    filterParam = "*";
                }
                var pre = filterParam !== '*' ? '.': '';

                $('.isotope').isotope({
                    filter: pre + filterParam,
                });
                $('.isotope').attr('data-number', el.attr('data-number'));
                $('.isotope').isotope('remove', $('.isotope-item'));
                $('.isotope').isotope('insert', $(el.html()));

                $('.isotope img').on('load', function() {
                    buildPagination();
                    $('.isotope').isotope('layout');
                    $('.isotope').removeClass('processing');
                });

            }
        );
    }

    if ($('.isotope[data-per-page]')) {
        buildPagination();
    }

    /* Switch pagination */
    $('body').on('click', '.portfolio-pagination-item', function() {
        $('.portfolio-pagination-selected').removeClass('portfolio-pagination-selected');
        $(this).addClass('portfolio-pagination-selected');
        $('.isotope').attr('data-page', $(this).html());
        portfolioAjax();
    });

    // bind filter button click
    $('.filter button').on('click', function() {
        $(this).parents('.filter').find('.selected').removeClass('selected');
        $(this).addClass('selected');

        // set filter in hash
        var newURL = replaceUrlParam(location.href, 'filter', $(this).attr('data-filter'));
        window.history.pushState('', '', newURL);

        if ($('.isotope[data-per-page]').length) {
            $('.portfolio-pagination-selected').removeClass('portfolio-pagination-selected');
            $('.portfolio-pagination-item:first-child').addClass('portfolio-pagination-selected');
            $('.isotope').attr('data-page', '1');

            portfolioAjax();
        } else {
            isotopeLayout.call(this);
        }
    });

    function isotopeLayout() {
        var parent = $('body');
        var el = $('.isotope');
        if (this !== window) {
            parent = $(this).parents('.filter');
            el = $(this).parents('.wpb_wrapper').find('.isotope');
        }

        var filterParam = getUrlParameter('filter');
        if (filterParam === undefined) {
            filterParam = parent.find('.filter > li:first-of-type button').data('filter');
        }
        var pre = filterParam !== '*' ? '.': '';

        parent.find('button[data-filter="' + filterParam + '"]').addClass('selected');

        var options = {
            itemSelector: '.isotope-item',
            layoutMode: 'fitRows',
            filter: pre + filterParam,
        };

        if(el.hasClass('random')) {
            if ($('.isotope').width() > 1140) {
                options.layoutMode = 'masonry';
                options.masonry = {
                    columnWidth: 292,
                };
            } else if ($('.isotope').width() > 940) {
                options.layoutMode = 'masonry';
                options.masonry = {
                    columnWidth: 242,
                };
            }
        }

        el.isotope(options);
    }

    // Call Isotope
    if ($('.isotope').length) {
        isotopeLayout();
        $(window).on('load', isotopeLayout);
        $(window).on('resize', isotopeLayout);
    }

    /* Blog masonry */

    try {
        var $containerMasonry = $('.blog-masonry');
        $containerMasonry.imagesLoaded(function() {
            if ($containerMasonry.length) {
                $containerMasonry.isotope({
                    itemSelector: '.blog-masonry .post',
                    animationOptions: {
                        duration: 750,
                        queue: false,
                    }
                });
                $(window).resize(function() {
                    $containerMasonry.isotope('layout');
                });
                $(window).focus(function() {
                    $containerMasonry.isotope('layout');
                });
                $(document).ready(function() {
                    $(window).load(function() {
                        $containerMasonry.isotope('layout');
                    });
                });
            }
        });
    } catch (e) {}
    /* Twitter */
    try {
        $("[data-twitter]").each(function(index) {
            var el = $("[data-twitter]").eq(index);
            $.ajax({
                type: "POST",
                url: 'http://localhost:8004/assets/php/twitter.php',
                data: {
                    account: el.attr("data-twitter")
                },
                success: function(msg) {
                    el.find(".carousel-inner").html(msg);
                }
            });

        });
    } catch (e) {}

    function checkForOnScreen() {
        $('.counter-number').each(function(index) {
            if (!$(this).hasClass('animated') && $('.counter-number').eq(index).isOnScreen()) {
                $('.counter-number').eq(index).countTo({
                    speed: 5000
                });
                $('.counter-number').eq(index).addClass('animated');
            }
        });
    }
    checkForOnScreen();
    $(window).scroll(function() {
        checkForOnScreen();
    });
    /* Fullscreen */
    if ($(window).height > 700) {
        $('.fullscreen').css('height', $(window).height() + 'px'); //menu position on home page
    }

    /* WordPress specific */
    // Comment button
    $('button[data-form="submit"]').on('click', function() {
        $('.form-submit #submit').click();
    });
    // Search widget
    $('.widget_product_search form').addClass('searchform');
    $('.searchform input[type="submit"]').remove();
    $('.searchform div').append('<button type="submit" class="fa fa-search" id="searchsubmit" value=""></button>');
    $('.searchform input[type="text"]').attr('placeholder', anps.search_placeholder);

    $('.blog-masonry').parent().removeClass('col-md-12');
    $('.post.style-3').parent().parent().removeClass('col-md-12').parent().removeClass('col-md-12');

    //$("a[rel^='prettyPhoto']").prettyPhoto();

    $('.site-navigation > div > ul').unwrap();

    $('.show-register').on('click', function() {
        $('#customer_login h3, #customer_login .show-register').addClass('hidden');
        $('#customer_login .register').removeClass('hidden');
    });

    function anpsLightbox() {
        $(window).on('grid:items:added', function () {
			$('.prettyphoto').addClass('vc-gitem-link-ajax')
		});

        if (rlArgs.script === 'swipebox') {
            $('.prettyphoto').swipebox({ hideBarsDelay: 0 });
        } else if (rlArgs.script === 'prettyphoto') {
            $('.prettyphoto').prettyPhoto();
        } else if (rlArgs.script === 'fancybox') {
            $('.prettyphoto').fancybox();
        } else if (rlArgs.script === 'nivo') {
            $('.prettyphoto').nivoLightbox();
        } else if (rlArgs.script === 'imagelightbox') {
            $('.prettyphoto').imageLightbox();
        }
    }

    if (typeof rlArgs !== 'undefined') {
        anpsLightbox();

        $(window).load(function() {
            /* Disable PrettyPhoto in VC */
            //$('.wpb_single_image .wpb_wrapper a[href$=".jpg"], .wpb_single_image .wpb_wrapper a[href$=".png"], .wpb_single_image .wpb_wrapper a[href$=".gif"]').attr('rel', 'lightbox');

            window.vc_prettyPhoto = function() {
                anpsLightbox();
            }
            anpsLightbox();
        });
    }

    $(document).ready(function() {
        $('.parallax-window[data-type="background"]').each(function() {
            var $bgobj = $(this); // assigning the object

            $(window).scroll(function() {
                var yPos = -($(window).scrollTop() / $bgobj.data('speed'));

                // Put together our final background position
                var coords = '50% ' + yPos + 'px';

                // Move the background
                $bgobj.css({
                    backgroundPosition: coords
                });
            });
        });
    });


});

jQuery(document).ready(function($) {
    $('.site-navigation ul').doubleTapToGo();

    jQuery('.ls-wp-fullwidth-helper:after').animate({
        width: "90px"
    }, "slow");
});



jQuery(document).ready(function() {

    // hide #back-top first
    jQuery("#back-top").hide();

    // fade in #back-top
    jQuery(function() {
        jQuery(window).scroll(function() {

            if (jQuery(this).scrollTop() > 300) {
                jQuery('#scrolltop').fadeIn();
            } else {
                jQuery('#scrolltop').fadeOut();
            }
        });

        // scroll body to 0px on click
        jQuery('#scrolltop a').click(function() {
            jQuery('body,html').animate({
                scrollTop: 0
            }, 800);
            return false;
        });
    });

    jQuery(document).ready(function($) {
        if ($('.owl-carousel').length) {
            $('.owl-carousel').each(function() {
                var $owl = $(this);

                var numberItems = $owl.attr('data-col');

                var autoplay = $owl.attr('data-autoplay') === 'true';
                var autoplayTimeout = $owl.attr('data-autoplay-timeout') ? $owl.attr('data-autoplay-timeout') : 5000;
                var autoplayPause = $owl.attr('data-autoplay-pause') === 'true';

                var itemsXS = $owl.attr('data-xs') ? $owl.attr('data-xs') : 1;
                var itemsSM = $owl.attr('data-sm') ? $owl.attr('data-sm') : 2;

                var dataNav = $owl.attr('data-nav') ? true : false;

                var margin = $owl.attr('data-margin') ? $owl.attr('data-margin') * 1 : 30;

                $owl.owlCarousel({
                    loop: true,
                    margin: margin,
                    autoplay: autoplay,
                    autoplayTimeout: autoplayTimeout,
                    autoplayHoverPause: autoplayPause,
                    responsiveClass: true,
                    rtl: $('body').hasClass('rtl'),
                    responsive: {
                        0: {
                            items: itemsXS,
                            nav: dataNav,
                            slideBy: itemsXS,
                        },
                        600: {
                            items: itemsSM,
                            nav: dataNav,
                            slideBy: itemsSM,
                        },
                        992: {
                            items: numberItems,
                            nav: dataNav,
                            slideBy: numberItems,
                        },
                    },
                });

                // Custom Navigation Events
                $owl.parents('.wpb_wrapper').find('.owlnext').on('click', function() {
                    $owl.trigger('next.owl.carousel');
                });

                $owl.parents('.wpb_wrapper').find('.owlprev').on('click', function() {
                    $owl.trigger('prev.owl.carousel');
                });
            });
        }
    });

    /*vertical menu*/
    if (jQuery('body').hasClass('vertical-menu')) {
        //jQuery('body > .site-wrapper .nav-wrap').prepend('<div class="hide-menu"></div>')
        jQuery('.nav-wrap > .hide-menu').click(function($) {
            jQuery('header.vertical-menu, body.vertical-menu').toggleClass('hide-side-menu');
        });
    }



}); //end of (document).ready function


/*-----------------------------------------------------------------------------------*/
/*  Overwriting the vc row behaviour function for the vertical menu
/*-----------------------------------------------------------------------------------*/

if (typeof window['vc_rowBehaviour'] !== 'function') {
  window.vc_rowBehaviour = function() {
    function fullWidthRow() {
      var $elements = $('[data-vc-full-width="true"]');
      $.each($elements, function(key, item) {
        /* Anpthemes */
        var verticalOffset = 0;
        if( $('.site-header-vertical-menu').length && window.innerWidth > 992 ) {
          verticalOffset = $('.site-header-vertical-menu').innerWidth();
        }

        var boxedOffset = 0;
        if( $('body.boxed').length && window.innerWidth > 992 ) {
          boxedOffset = ($('body').innerWidth() - $('.site-wrapper').innerWidth()) / 2;
        }

        var $el = $(this);
        $el.addClass("vc_hidden");
        var $el_full = $el.next(".vc_row-full-width");
        $el_full.length || ($el_full = $el.parent().next(".vc_row-full-width"));
        var el_margin_left = parseInt($el.css("margin-left"), 10)
          , el_margin_right = parseInt($el.css("margin-right"), 10)
          , offset = 0 - $el_full.offset().left - el_margin_left
          , width = $(window).width() - verticalOffset - boxedOffset*2
          , positionProperty = $('body.rtl').length ? 'right' : 'left';

        if( positionProperty === 'right' ) {
            verticalOffset = 0;
        }

        var options = {
            'position': 'relative',
            'box-sizing': 'border-box',
            'width': width
        };
        options[positionProperty] = offset + verticalOffset + boxedOffset;

        $el.css(options);

        if(!$el.data("vcStretchContent")) {
          var padding = -1 * offset - verticalOffset - boxedOffset;
          0 > padding && (padding = 0);
          var paddingRight = width - padding - $el_full.width() + el_margin_left + el_margin_right;
          0 > paddingRight && (paddingRight = 0),
          $el.css({
            "padding-left": padding + "px",
            "padding-right": paddingRight + "px"
          })
        }
        $el.attr("data-vc-full-width-init", "true"),
        $el.removeClass("vc_hidden")
      }),
      $(document).trigger("vc-full-width-row", $elements)
    }
    function parallaxRow() {
      var vcSkrollrOptions, callSkrollInit = !1;
      return window.vcParallaxSkroll && window.vcParallaxSkroll.destroy(),
      $(".vc_parallax-inner").remove(),
      $("[data-5p-top-bottom]").removeAttr("data-5p-top-bottom data-30p-top-bottom"),
      $("[data-vc-parallax]").each(function() {
        var skrollrSpeed, skrollrSize, skrollrStart, skrollrEnd, $parallaxElement, parallaxImage, youtubeId;
        callSkrollInit = !0,
        "on" === $(this).data("vcParallaxOFade") && $(this).children().attr("data-5p-top-bottom", "opacity:0;").attr("data-30p-top-bottom", "opacity:1;"),
        skrollrSize = 100 * $(this).data("vcParallax"),
        $parallaxElement = $("<div />").addClass("vc_parallax-inner").appendTo($(this)),
        $parallaxElement.height(skrollrSize + "%"),
        parallaxImage = $(this).data("vcParallaxImage"),
        youtubeId = vcExtractYoutubeId(parallaxImage),
        youtubeId ? insertYoutubeVideoAsBackground($parallaxElement, youtubeId) : "undefined" != typeof parallaxImage && $parallaxElement.css("background-image", "url(" + parallaxImage + ")"),
        skrollrSpeed = skrollrSize - 100,
        skrollrStart = -skrollrSpeed,
        skrollrEnd = 0,
        $parallaxElement.attr("data-bottom-top", "top: " + skrollrStart + "%;").attr("data-top-bottom", "top: " + skrollrEnd + "%;")
      }),
      callSkrollInit && window.skrollr ? (vcSkrollrOptions = {
        forceHeight: !1,
        smoothScrolling: !1,
        mobileCheck: function() {
          return !1
        }
      },
      window.vcParallaxSkroll = skrollr.init(vcSkrollrOptions),
      window.vcParallaxSkroll) : !1
    }
    function fullHeightRow() {
      var $element = $(".vc_row-o-full-height:first");
      if ($element.length) {
        var $window, windowHeight, offsetTop, fullHeight;
        $window = $(window),
        windowHeight = $window.height(),
        offsetTop = $element.offset().top,
        windowHeight > offsetTop && (fullHeight = 100 - offsetTop / (windowHeight / 100),
        $element.css("min-height", fullHeight + "vh"))
      }
      $(document).trigger("vc-full-height-row", $element)
    }
    function fixIeFlexbox() {
      var ua = window.navigator.userAgent
        , msie = ua.indexOf("MSIE ");
      (msie > 0 || navigator.userAgent.match(/Trident.*rv\:11\./)) && $(".vc_row-o-full-height").each(function() {
        "flex" === $(this).css("display") && $(this).wrap('<div class="vc_ie-flexbox-fixer"></div>')
      })
    }
    var $ = window.jQuery;
    $(window).off("resize.vcRowBehaviour").on("resize.vcRowBehaviour", fullWidthRow).on("resize.vcRowBehaviour", fullHeightRow),
    fullWidthRow(),
    fullHeightRow(),
    fixIeFlexbox(),
    vc_initVideoBackgrounds(),
    parallaxRow()
  }
}

/* Google Maps (using gmaps.js) */

function isFloat(n) {
    return parseFloat(n.match(/^-?\d*(\.\d+)?$/)) > 0;
}

function checkCoordinates(str) {
    if (!str) {
        return false;
    }

    str = str.split(',');
    var isCoordinate = true;

    if (str.length !== 2 || !isFloat(str[0].trim()) || !isFloat(str[1].trim())) {
        isCoordinate = false;
    }

    return isCoordinate;
}

jQuery(function($) {
    $('.map').each(function() {
        /* Options */
        var gmap = {
            zoom: ($(this).attr('data-zoom')) ? parseInt($(this).attr('data-zoom')) : 15,
            address: $(this).attr('data-address'),
            markers: $(this).attr('data-markers'),
            icon: $(this).attr('data-icon'),
            typeID: $(this).attr('data-type'),
            ID: $(this).attr('id'),
        };

        var gmapScroll = ($(this).attr('data-scroll')) ? $(this).attr('data-scroll') : 'false';
        var markersArray = [];
        var bound = new google.maps.LatLngBounds();

        if (gmapScroll == 'false') {
            gmap.draggable = false;
            gmap.scrollwheel = false;
        }

        /* Google Maps with markers */

        if (gmap.markers) {
            gmap.markers = gmap.markers.split('|');

            /* Get markers and their options */
            gmap.markers.forEach(function(marker) {
                if (marker) {
                    marker = $.parseJSON(marker);

                    if (checkCoordinates(marker.address)) {
                        marker.latLng = marker.address.split(',');
                        delete marker.address;
                    }

                    markersArray.push(marker);
                }
            });

            /* Initialize map */
            $('#' + gmap.ID).gmap3({
                zoom: gmap.zoom,
                draggable: gmap.draggable,
                scrollwheel: gmap.scrollwheel,
                mapTypeId: google.maps.MapTypeId[gmap.typeID],
                styles: gmap.styles
            }).marker(markersArray).then(function(results) {
                var center = null;

                if (typeof results[0].position.lat !== 'function' ||
                    typeof results[0].position.lng !== 'function') {
                    return false;
                }

                results.forEach(function(m, i) {
                    if (markersArray[i].center) {
                        center = new google.maps.LatLng(m.position.lat(), m.position.lng());
                    } else {
                        bound.extend(new google.maps.LatLng(m.position.lat(), m.position.lng()));
                    }
                });

                if (!center) {
                    center = bound.getCenter();
                }

                this.get(0).setCenter(center);
            }).infowindow({
                content: ''
            }).then(function(infowindow) {
                var map = this.get(0);
                this.get(1).forEach(function(marker) {
                    if (marker.data !== '') {
                        marker.addListener('click', function() {
                            infowindow.setContent(decodeURIComponent(marker.data));
                            infowindow.open(map, marker);
                        });
                    }
                });
            });
        }

        /* Google Maps Basic */

        if (gmap.address) {
            if (checkCoordinates(gmap.address)) {
                $('#' + gmap.ID).gmap3({
                    zoom: gmap.zoom,
                    draggable: gmap.draggable,
                    scrollwheel: gmap.scrollwheel,
                    mapTypeId: google.maps.MapTypeId[gmap.typeID],
                    center: gmap.address.split(',')
                }).marker({
                    latLng: gmap.address.split(','),
                    options: {
                        icon: gmap.icon
                    }
                });
            } else {
                $('#' + gmap.ID).gmap3({
                    zoom: gmap.zoom,
                    draggable: gmap.draggable,
                    scrollwheel: gmap.scrollwheel,
                    mapTypeId: google.maps.MapTypeId[gmap.typeID],
                }).latlng({
                    address: gmap.address
                }).then(function(result) {
                    if (!result) {
                        return
                    };

                    this.get(0).setCenter(new google.maps.LatLng(result.lat(), result.lng()));
                }).marker(function() {
                    return {
                        position: this.get(0).getCenter(),
                        icon: gmap.icon
                    };
                });
            }
        }
    });

    /* Featured content style 2 */

    $('.f-content--style-2').each(function () {
        $(this).parents('.vc_row').find('.vc_column-inner').css({
            'padding-left': '0px',
            'padding-right': '0px',
        });

         $(this).parents('.vc_row').css({
             'padding-left': '15px',
             'padding-right': '15px',
         });

         $(this).parents('[data-vc-full-width="true"]').css({
             'margin-left': '0',
             'margin-right': '0',
         });
    });


    /*-----------------------------------------------------------------------------------*/
    /*	Gallery Thumbnails
    /*-----------------------------------------------------------------------------------*/

    var openGallery = false;

    function changeThumb(el) {
        var $gallery = el.parents('.gallery-fs');

        if (!el.hasClass('selected')) {
            $gallery.find('> figure > img').attr('src', el.attr('href'));
            $gallery.find('> figure > figcaption').html(el.attr('title'));
            $gallery.find('.gallery-fs-thumbnails .selected').removeClass('selected');
            el.addClass('selected');
        }
    }

    var thumbCol = 6;
    var galleryParent = $('.gallery-fs').parents('[class*="col-"]');
    var galleryParentSize = Math.floor(galleryParent.outerWidth() / galleryParent.parent().outerWidth() * 100);

    if (galleryParentSize < 60) {
        thumbCol = 5;
    }
    if (galleryParentSize == 100) {
        thumbCol = 9;
    }

    var navText = ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'];

    if ($('html[dir="rtl"]').length) {
        navText.reverse();
    }

    function setOwlNav(e){
        if(e.page.size >= e.item.count) {
            if ($('html[dir="rtl"]').length) {
                $(e.target).siblings('.gallery-fs-nav').children('a, button').css('transform', 'translateX(-83px)');
            } else {
                $(e.target).siblings('.gallery-fs-nav').children('a, button').css('transform', 'translateX(83px)');
            }
        } else {
            $(e.target).siblings('.gallery-fs-nav').children('a, button').css('transform', 'translateX(0)');
        }
    }
    $('.gallery-fs-thumbnails').owlCarousel({
        onInitialized: setOwlNav,
        onResized: setOwlNav,
        loop: false,
        margin: 17,
        nav: true,
        navText: navText,
        rtl: ($('html[dir="rtl"]').length > 0),
        responsive: {
            0:    { items: 2 },
            600:  { items: 4 },
            1000: { items: thumbCol },
        },
    });

    $('.gallery-fs-thumbnails a').swipebox({
        hideBarsDelay: -1,
        afterOpen: function() {
            if (!openGallery) {
                $.swipebox.close();
            }
            openGallery = false;
        },
        nextSlide: function() {
            var index = $('.gallery-fs-thumbnails .owl-item a.selected').parent().index();

            if (index < $('.gallery-fs-thumbnails .owl-item').length - 1) {
                changeThumb($('.gallery-fs-thumbnails .owl-item').eq(index + 1).children('a'));
            }
        },
        prevSlide: function() {
            var index = $('.gallery-fs-thumbnails .owl-item a.selected').parent().index();

            if (index > 0) {
                changeThumb($('.gallery-fs-thumbnails .owl-item').eq(index - 1).children('a'));
            }
        },
    });

    $('.gallery-fs-thumbnails .owl-item a').on('click', function() {
        changeThumb($(this));
    });

    $('.gallery-fs-fullscreen').on('click', function(e) {
        e.preventDefault();
        openGallery = true;

        var $gallery = $(this).parents('.gallery-fs');

        if ($gallery.find('.gallery-fs-thumbnails').length) {
            $gallery.find('.gallery-fs-thumbnails .owl-item a.selected').eq(0).click();
        }
    });

    /* Only one thumbnail */

    if (!$('.gallery-fs-thumbnails').length) {
        $('.gallery-fs-fullscreen').css({
            'right': '21px'
        });
        $('.gallery-fs-fullscreen').swipebox({
            hideBarsDelay: 1
        })
    }

    /*-----------------------------------------------------------------------------------*/
    /*	Fixed Footer
    /*-----------------------------------------------------------------------------------*/

    $(window).on('load', function() {
        if ($('.footer-parallax').length) {
            fixedFooter();

            $(window).on('resize', function() {
                fixedFooter();
            });
        }
    })

    function fixedFooter() {
        $('.site-wrapper').css('margin-bottom', $('.site-footer').innerHeight());
        $('.site-wrapper').css('padding-bottom', $('.site-footer').css('margin-top'));
    }

    /* iOS hover box fix */

    function isIOS() {
        return /(iPad|iPhone|iPod)/g.test(navigator.userAgent);
    }

    if (isIOS) {
        $('.vc-hoverbox').attr('onclick', '');
    }
});
