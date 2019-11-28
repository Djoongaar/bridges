;(function($) {
    'use strict';

    var wprtTheme = {

        // Main init function
        init : function() {
            this.config();
            this.events();
        },

        // Define vars for caching
        config : function() {
            this.config = {
                $window : $(window),
                $document : $(document),
            };
        },

        // Events
        events : function() {
            var self = this;

            // Run on document ready
            self.config.$document.on( 'ready', function() {

                // Hero SlideShow
                self.hereSection();

                // Scroll to Target
                self.scrollTarget();

                // Header Sticky
                self.headerFixed();

                // Tabs
                self.tabs();

                // Cart Icon
                self.cartIcon();

                // Progress Bar
                self.progressBar();

                // Toggle
                self.toggles();

                // Popup Images
                self.popupImage();

                // Mobile Navigation
                self.mobileNav();

                // Partners Slider
                self.partners();

                // Counter
                self.counter();

                // Galleries Flexslider
                self.galleriesFlex();

                // Galleries CubePortfolio
                self.galleriesCube();

                // Team
                self.team();

                // Search Icon
                self.searchIcon();

                // Retina Logos
                self.retinaLogo();

                // Featured Media
                self.featuredMedia();

                // Responsive Videos
                self.responsiveVideos();

                // Match Height Content
                self.matchHeight();

                // Scroll to Top
                self.scrollToTop();

                // Tweet Slider
                self.tweetSlider();

                // Spacer
                self.spacer();

                // Projects
                self.projectFilter();

                // Services
                self.serviceSlider();

                // Testimonails
                self.testimonails();

                // Contact Form
                self.ajaxContactForm();

                // Preloader
                self.preLoader();
            } );

            // Run on Window Load
            self.config.$window.on( 'load', function() {
                // Google Map
                self.googleMap();

                // Parallax
                self.parallax();

                // Detect Viewport
                self.inViewport();
            } );
        },

        preLoader: function() {
            if ( $().animsition ) {
                $(".animsition").animsition({
                    inClass: 'fade-in',
                    outClass: 'fade-out',
                    inDuration: 1500,
                    outDuration: 800,
                    loading: true,
                    loadingParentElement: 'body',
                    loadingClass: 'animsition-loading',
                    timeout: false,
                    timeoutCountdown: 5000,
                    onLoadEvent: true,
                    browser: [
                        '-webkit-animation-duration',
                        '-moz-animation-duration',
                        'animation-duration'
                        ],
                    overlay: false,
                    overlayClass: 'animsition-overlay-slide',
                    overlayParentElement: 'body',
                    transition: function(url){ window.location.href = url; }
                });
            }
        },

        hereSection: function() {
            $(window).on('load resize', function(){
                var
                hero = $('#hero-section'),
                heroContent = hero.find('.hero-content'),
                contentHeight = heroContent.height(),
                sliderHeight = $(window).height(),
                headerHeight = $('#site-header-wrap').height();

                if ( $('body').hasClass('header-sticky') )
                    headerHeight = headerHeight / 2;

                var contentMargin = (sliderHeight - contentHeight - headerHeight) / 2;

                hero.css({ height: sliderHeight + "px" });

                heroContent.css({ 
                   "margin-top" : headerHeight + contentMargin + "px",
                   "margin-bottom": contentMargin + "px"
                });
            })

            if ( $().vegas ) {
                $("#hero-section").each(function() {
                    var
                    $this = $(this),
                    number = $this.data('number'),
                    number = parseInt(number),
                    effect = $this.data('effect'),
                    i = 1,
                    slides = [];

                    while ( i <= number ) {
                        slides.push( {src:$this.data('image-'+i)} );
                        i++;
                    }

                    $this.vegas({
                        slides: slides,
                        overlay: true,
                        transition: effect
                    });
                });
            }

            if ( $().fitText ) {
                $('#hero-section .hero-title').each(function(){
                    var min = $(this).data("min");
                    var max = $(this).data("max");

                    $(this).children('h1').fitText(1.8, {
                        minFontSize: min,
                        maxFontSize: max
                    });
                });
            }

            if ( $('.hero-title').is('.scroll') ) {
                var
                current = 1,
                height = $('.hero-title').height(),
                numberDivs = $('.hero-title').children().length,
                first = $('.hero-title h1:nth-child(1)');

                setInterval(function() {
                    var number = current * -height;
                    
                    first.css('margin-top', number + 'px');
                    if ( current === numberDivs ) {
                        first.css('margin-top', '0px');
                        current = 1;
                    } else current++;
                }, 2500);
            }

            if ( $('.hero-title').is('.typing') ) {
                $('.hero-title').find('span').typed({
                    strings: ["FOCUS ON YOU", "HAVE EXPERIENCE"],
                    typeSpeed: 10,
                    loop:true,
                    backDelay: 2000
                });
            }
        },

        scrollTarget: function() {
            $('.scroll-target').on('click',function() {
                var anchor = $(this).attr('href').split('#')[1];

                $(this).parent()
                    .addClass('current-menu-item')
                    .siblings()
                        .removeClass('current-menu-item');

                if ( anchor ) {
                    if ( $('#'+anchor).length > 0 ) {
                        var headerHeight = 0;

                        if ( $('body').hasClass('header-sticky') )
                            headerHeight = $('#site-header').height();

                        var target = $('#' + anchor).offset().top - headerHeight;

                        $('html,body').animate({scrollTop: target}, 1000, 'easeInOutExpo');
                   }
                }
                return false;
            })
        },

        headerFixed: function() {
            if ( $('body').hasClass('header-sticky') ) {
                var nav = $('#site-header');

                if ( nav.size() != 0 ) {
                    var offsetTop = nav.offset().top,
                        headerHeight = nav.height(),
                        injectSpace = $('<div />', {
                            height: headerHeight
                        }).insertAfter(nav);

                    $(window).on('load scroll', function(){
                        if ( $(window).scrollTop() > offsetTop ) {
                            $('#site-header').addClass('is-sticky');
                            injectSpace.show();
                        } else {
                            $('#site-header').removeClass('is-sticky');
                            injectSpace.hide();
                        }
                    })
                }
            }     
        },

        tabs: function() {
            $('.woocommerce-tabs').each(function() {
                $(this).find('.wc-tab').hide();
                $(this).find('.wc-tab:first').show();

                $(this).find('.wc-tabs li').on('click', function(e) {
                    var idx = $(this).index();
                    var content = $(this).closest('.woocommerce-tabs').find('.wc-tab').eq(idx);

                    $(this).addClass('active').siblings().removeClass('active');
                    content.fadeIn('slow').siblings('.wc-tab').hide();

                    e.preventDefault();
                });
            });
        },
        
        cartIcon: function() {
            $(document).on( 'woocommerce-cart-changed', function( e, data ) {
                if ( parseInt( data.items_count ) > 0 ) {
                    $('.shopping-cart-items-count')
                        .text( data.items_count )
                }
            } );
        },

        progressBar: function() {
            if ( $().waypoint ) {
                $('.progress-bar').on('on-appear', function() {
                    $(this).each(function() {
                        var percent = parseInt($(this).data('percent'));

                        $(this).find('.progress-animate').animate({
                            "width": percent + '%'
                        },1000, "easeInCirc");

                        $(this).parent('.wprt-progress').find('.perc').addClass('show').animate({
                            "width": percent + '%'
                        },1000, "easeInCirc");
                    });
                });
            }
        },

        toggles: function() {
            var args = {easing:'easeOutExpo', duration:300};

            $('.wprt-toggle.active').find('.toggle-content').show();
            $('.toggle-title').on('click', function () {
                if ( !$(this).parent().is('.active') ) {
                    $(this).parent().toggleClass('active')
                        .children('.toggle-content').slideToggle(args)
                    .parent().siblings('.active').removeClass('active')
                        .children('.toggle-content').slideToggle(args);
                } else {
                    $(this).parent().toggleClass('active');
                    $(this).next().slideToggle(args);
                }
            });
        },

        popupImage: function() {
            if ( $().magnificPopup ) {
                $('.wprt-galleries, .wprt-galleries-grid').each(function () {
                    $(this).find('.zoom').magnificPopup({
                        disableOn: 700,
                        type: 'image',
                        gallery:{
                            enabled: true
                        },
                        mainClass: 'mfp-fade',
                        removalDelay: 160,
                        preloader: false,
                        fixedContentPos: true
                    });
                });
            }
        },

        mobileNav: function() {
            var menuType = 'desktop';

            $(window).on('load resize', function() {
                var mode = 'desktop';
                var $wrapMenu = $('#site-header-inner .wrap-inner');

                if ( matchMedia( 'only screen and (max-width: 991px)' ).matches )
                    mode = 'mobile';

                if ( mode != menuType ) {
                    menuType = mode;

                    if ( mode == 'mobile' ) {
                        $('#main-nav').attr('id', 'main-nav-mobi')
                            .appendTo('#site-header')
                            .hide()
                                .find('li:has(ul)')
                                .children('ul')
                                    .hide()
                                    .before('<span class="arrow"></span>');
                    } else {
                        if ( $('#site-header').is('.style-2, .style-3, .style-4') )
                            $wrapMenu = $('.site-navigation-wrap .inner');

                        $('#main-nav-mobi').attr('id', 'main-nav')
                            .removeAttr('style')
                            .prependTo($wrapMenu)
                            .find('.sub-menu')
                                .removeAttr('style')
                                .prev().remove();
                                
                        $('.mobile-button').removeClass('active');
                    }
                }
            });

            $(document).on('click', '.mobile-button', function() {
                $(this).toggleClass('active');
                $('#main-nav-mobi').slideToggle();
            })

            $(document).on('click', '#main-nav-mobi .arrow', function() {
                $(this).toggleClass('active').next().slideToggle();
            })
        },

        partners: function() {
            if ( $().owlCarousel ) {
                $('.wprt-partners').each(function(){
                    var $this = $(this);
                    $this.find('.owl-carousel').owlCarousel({
                        navigation : false,
                        pagination: false,
                        responsive: true,
                        items: 1,
                        navigationText: false,
                        itemsDesktop: [3000,5],
                        itemsDesktopSmall: [1400,4],
                        itemsTablet:[970,3],
                        itemsTabletSmall: [600,2],
                        itemsMobile: [360,1],
                        touchDrag: true,
                        mouseDrag: true,
                        autoHeight: false,
                        autoPlay: true
                    });
                });
            }
        },

        counter: function() {
            if ( $().countTo ) {
                $('.wprt-counter').on('on-appear', function() {
                    $(this).find('.number').each(function() {
                        var to = parseInt( $(this).data('to'), 10 ),
                            speed = parseInt( $(this).data('speed'), 10 );
                            
                        $(this).countTo({
                            to: to,
                            speen: speed
                        });
                    });
                }); //counter
            }
        },

        galleriesFlex: function() {
            $('.wprt-galleries').each(function(){
                var itemW = $(this).data("width");
                var itemM = $(this).data("margin");

                $(this).children('#wprt-carousel').flexslider({
                    animation: "slide",
                    controlNav: false,
                    animationLoop: false,
                    slideshow: false,
                    itemWidth: itemW,
                    itemMargin: itemM,
                    asNavFor: $(this).children('#wprt-slider'),
                    prevText: '<i class="fa fa-angle-left"></i>',
                    nextText: '<i class="fa fa-angle-right"></i>'
                });
                $(this).children('#wprt-slider').flexslider({
                    animation: "slide",
                    controlNav: false,
                    animationLoop: false,
                    slideshow: false,
                    sync: $(this).children('#wprt-carousel'),
                    prevText: '<i class="fa fa-angle-left"></i>',
                    nextText: '<i class="fa fa-angle-right"></i>'
                });
            });
        },

        galleriesCube: function() {
            $('.wprt-galleries-grid').each(function() {
                var
                $this = $(this),
                item = $this.data("column"),
                item2 = $this.data("column2"),
                item3 = $this.data("column3"),
                item4 = $this.data("column4"),
                layout = $this.data("layout"),
                gapH = Number($this.data("gaph")),
                gapV = Number($this.data("gapv"));

                $(this).find('#images-wrap').cubeportfolio({
                    layoutMode: layout,
                    defaultFilter: '*',
                    animationType: 'quicksand',
                    gapHorizontal: gapH,
                    gapVertical: gapV,
                    showNavigation: true,
                    showPagination: true,
                    gridAdjustment: 'responsive',
                    rewindNav: false,
                    auto: true,
                    mediaQueries: [{
                        width: 1500,
                        cols: item
                    }, {
                        width: 1100,
                        cols: item
                    }, {
                        width: 800,
                        cols: item2
                    }, {
                        width: 550,
                        cols: item3
                    }, {
                        width: 320,
                        cols: item4
                    }],
                    caption: ' ',
                    displayType: 'bottomToTop',
                    displayTypeSpeed: 100
                });
            });
        },

        team: function() {
            $('.wprt-team').each(function() {
                var
                $this = $(this),
                item = $this.data("column"),
                item2 = $this.data("column2"),
                item3 = $this.data("column3"),
                item4 = $this.data("column4"),
                layout = $this.data("layout"),
                gapH = Number($this.data("gaph")),
                gapV = Number($this.data("gapv"));

                $(this).find('#team-wrap').cubeportfolio({
                    layoutMode: layout,
                    defaultFilter: '*',
                    animationType: 'quicksand',
                    gapHorizontal: gapH,
                    gapVertical: gapV,
                    showNavigation: true,
                    showPagination: true,
                    gridAdjustment: 'responsive',
                    rewindNav: false,
                    auto: true,
                    mediaQueries: [{
                        width: 1500,
                        cols: item
                    }, {
                        width: 1100,
                        cols: item
                    }, {
                        width: 800,
                        cols: item2
                    }, {
                        width: 550,
                        cols: item3
                    }, {
                        width: 320,
                        cols: item4
                    }],
                    caption: ' ',
                    displayType: 'bottomToTop',
                    displayTypeSpeed: 100
                });
            });
        },


        searchIcon: function() {
            $('.header-search-icon').on('click', function() {
                var searchForm = $(this).parent().find('.header-search-form'),
                    searchField = $(this).parent().find('.header-search-field');

                searchForm.stop().fadeToggle(function () {
                    searchField.focus();
                });
            });
        },

        retinaLogo: function() {
            var retina = window.devicePixelRatio > 1 ? true : false;
            var $logo = $('#site-logo img');
            var $logo_retina = $logo.data('retina');

            if ( retina && $logo_retina ) {
                $logo.attr({
                    src: $logo.data('retina'),
                    width: $logo.data('width'),
                    height: $logo.data('height')
                });
            }
        },

        responsiveVideos: function() {
            if ( $().fitVids ) {
                $('.wprt-container').fitVids();
            }
        },

        matchHeight: function() {
            if ( $().matchHeight ) {
                if ( $('body').hasClass('match-height-content' ) ) {
                    $('#main-content').find('.inner-content-wrap').matchHeight();
                }
            }
        },

        scrollToTop: function() {
            var scrollBtn = $('#scroll-top');
            
            $(window).on('scroll', function() {
                if ( $(this).scrollTop() > 800 ) {
                    scrollBtn.addClass('show');
                } else {
                    scrollBtn.removeClass('show');
                }
            });

            scrollBtn.on('click', function() {
                $('html, body').animate({ scrollTop: 0 }, 1000 , 'easeInOutExpo');
            return false;
            });
        },

        featuredMedia: function() {
            if ( $().cubeportfolio ) {
                $('.blog-slider').each(function () {
                    var $this = $(this);
                    var item = $this.data("item1500");
                    var item2 = $this.data("item1100");
                    var item3 = $this.data("item800");
                    var item4 = $this.data("item550");
                    var item5 = $this.data("item320");
                    var layout = $this.data("layout");
                    var arrows = $this.data("arrows");
                    var bullets = $this.data("bullets");
                    var gapH = Number($this.data("gaph"));
                    var gapV = Number($this.data("gapv"));

                    $this.find('.item-wrap').cubeportfolio({
                        layoutMode: layout,
                        gapHorizontal: gapH,
                        gapVertical: gapV,
                        showNavigation: arrows,
                        showPagination: bullets,
                        gridAdjustment: 'responsive',
                        rewindNav: false,
                        mediaQueries: [{
                            width: 1500,
                            cols: item
                        }, {
                            width: 1100,
                            cols: item2
                        }, {
                            width: 800,
                            cols: item3
                        }, {
                            width: 550,
                            cols: item4
                        }, {
                            width: 320,
                            cols: item5
                        }],
                        caption: ' ',
                        displayType: 'bottomToTop',
                        displayTypeSpeed: 100
                    });
                });
            }
        },

        testimonails: function() {
            $('.wprt-testimonials').each(function() {
                var
                $this = $(this),
                item = $this.data("column"),
                item2 = $this.data("column2"),
                item3 = $this.data("column3"),
                item4 = $this.data("column4"),
                gapV = Number($this.data("gapv"));

                $(this).find('#testimonials-wrap').cubeportfolio({
                    layoutMode: 'slider',
                    defaultFilter: '*',
                    animationType: 'quicksand',
                    gapHorizontal: 0,
                    gapVertical: gapV,
                    showNavigation: true,
                    showPagination: true,
                    gridAdjustment: 'responsive',
                    rewindNav: false,
                    auto: true,
                    mediaQueries: [{
                        width: 1500,
                        cols: item
                    }, {
                        width: 1100,
                        cols: item
                    }, {
                        width: 800,
                        cols: item2
                    }, {
                        width: 550,
                        cols: item3
                    }, {
                        width: 320,
                        cols: item4
                    }],
                    caption: ' ',
                    displayType: 'bottomToTop',
                    displayTypeSpeed: 100
                });
            });
        },

        tweetSlider: function() {
            if ( $().cubeportfolio ) {
                $('.tweets-slider').each(function () {
                    var $this = $(this);
                    var layout = $this.data("layout");

                    $this.find('.item-wrap').cubeportfolio({
                        layoutMode: layout,
                        auto: 0,
                        showNavigation: false,
                        showPagination: true,
                        gridAdjustment: 'responsive',
                        rewindNav: false,
                        mediaQueries: [{
                            width: 1500,
                            cols: 1
                        }, {
                            width: 1100,
                            cols: 1
                        }, {
                            width: 800,
                            cols: 1
                        }, {
                            width: 550,
                            cols: 1
                        }, {
                            width: 320,
                            cols: 1
                        }],
                        caption: ' ',
                        displayType: 'bottomToTop',
                        displayTypeSpeed: 100
                    });
                });
            }
        },

        spacer: function() {
            $(window).on('load resize', function() {
                $('.wprt-spacer').each(function(){
                    if ( $(window).width() > 991 ) {
                        $(this).attr('style', 'height:' + $(this).data('desktop') + 'px')
                    } else if ( $(window).width() > 767 ) {
                        $(this).attr('style', 'height:' + $(this).data('mobi') + 'px')
                    } else {
                        $(this).attr('style', 'height:' + $(this).data('smobi') + 'px') 
                    }
                })
            });
        },

        projectFilter: function() {
            $('.wprt-project').each(function() {
                var
                $this = $(this),
                item = $this.data("column"),
                item2 = $this.data("column2"),
                item3 = $this.data("column3"),
                item4 = $this.data("column4"),
                layout = $this.data("layout"),
                gapH = Number($this.data("gaph")),
                gapV = Number($this.data("gapv"));

                $(this).find('#projects').cubeportfolio({
                    filters: '#project-filter',
                    layoutMode: layout,
                    defaultFilter: '*',
                    animationType: 'quicksand',
                    gapHorizontal: gapH,
                    gapVertical: gapV,
                    showNavigation: true,
                    showPagination: true,
                    gridAdjustment: 'responsive',
                    rewindNav: false,
                    auto: false,
                    mediaQueries: [{
                        width: 1500,
                        cols: item
                    }, {
                        width: 1100,
                        cols: item
                    }, {
                        width: 800,
                        cols: item2
                    }, {
                        width: 550,
                        cols: item3
                    }, {
                        width: 320,
                        cols: item4
                    }],
                    caption: ' ',
                    displayType: 'bottomToTop',
                    displayTypeSpeed: 100
                });
            });
        },

        serviceSlider: function() {
            $('.wprt-service').each(function() {
                var
                $this = $(this),
                item = $this.data("column"),
                item2 = $this.data("column2"),
                item3 = $this.data("column3"),
                item4 = $this.data("column4"),
                layout = $this.data("layout"),
                gapH = Number($this.data("gaph")),
                gapV = Number($this.data("gapv"));

                $(this).find('#service-wrap').cubeportfolio({
                    layoutMode: layout,
                    defaultFilter: '*',
                    animationType: 'quicksand',
                    gapHorizontal: gapH,
                    gapVertical: gapV,
                    showNavigation: true,
                    showPagination: true,
                    gridAdjustment: 'responsive',
                    rewindNav: false,
                    auto: true,
                    mediaQueries: [{
                        width: 1500,
                        cols: item
                    }, {
                        width: 1100,
                        cols: item
                    }, {
                        width: 800,
                        cols: item2
                    }, {
                        width: 550,
                        cols: item3
                    }, {
                        width: 320,
                        cols: item4
                    }],
                    caption: ' ',
                    displayType: 'bottomToTop',
                    displayTypeSpeed: 100
                });
            });
        },

        ajaxContactForm: function() {
            if ( $().validate ) {        
                $('.contact-form').each(function() {
                    $(this).validate({
                        submitHandler: function( form ) {
                            var
                            $form = $(form),
                            str = $form.serialize();

                            $.ajax({
                                type: "POST",
                                url:  $form.attr('action'),
                                data: str,
                                beforeSend: function () {
                                    $form.find('.bwp-alert').remove();
                                },
                                success: function( msg ) {
                                    var result, cls;

                                    if ( msg == 'Success' ) {
                                        result = 'Your message has been sent. Thank you!';
                                        cls = 'success';
                                    } else {
                                        result = 'Ваше сообщение отправлено';
                                        cls = 'error';
                                    }

                                    $form.prepend(
                                        $('<div />', {
                                            'class': 'bwp-alert ' + cls,
                                            'text' : result
                                        }).append(
                                            $('<a class="remove" href="#"><i class="fa fa-close"></i></a>')
                                        )
                                    );

                                    $form.find(':input').not('.submit').val('');
                                }
                            });
                        }
                    });
                });
            }
            $(document).on('click', '.bwp-alert .remove', function(e) {
                $(this).parent().slideUp();

                e.preventDefault();
            })
        },

        parallax: function() {
            var iOS = ( navigator.userAgent.match(/(iPad|iPhone|iPod)/g) ? true : false );
            /*
             * Please note that background attachment fixed doesn't work on iOS
             */ 
            if (!iOS) {
                $('.parallax').css({backgroundAttachment:'fixed'});
            } else {
                $('.parallax').css({backgroundAttachment:'scroll'});
            }

            if ( $().parallax && matchMedia( 'only screen and (min-width: 867px)' ).matches ) {
                $('.works').parallax("50%", 0.5);
                $('.facts').parallax("50%", 0.5);
                $('.facts-2').parallax("50%", 0.5);
                $('.facts-3').parallax("50%", 0.5);
                $('.promotion-2').parallax("50%", 0.5);
                $('.progressbar').parallax("50%", 0.5);
            }
        },

        inViewport: function() {
            $('[data-in-viewport="yes"]').waypoint(function() {
                $(this).trigger('on-appear');
            }, { offset: '75%', triggerOnce: true });

            $(window).on('load', function() {
                setTimeout(function() {
                    $.waypoints('refresh');
                }, 100);
            });
        },

        googleMap: function() {
            if ( $().gmap3 ) {
                var contentString = '<div id="content">'+
                    '<div style="max-width: 300px;">'+
                    '<h3>YOUR COMPANY</h3>'+
                    '<p>Cras id justo eget sapien scelerisque. Vivamus pretium at condimentum porta. Phasellus mollis mauris dolor, a tincidunt mauris fringilla.' +
                    '</p>'+
                    '</div>';
                $('#gmap')
                .gmap3({
                    center: [11.535478, 106.890631],
                    zoom: 14,
                    scrollwheel: false
                })
                .infowindow({
                    position: [11.537034, 106.890167],
                    content: contentString
                })
                .then(function (infowindow) {
                    infowindow.open(this.get(0));
                });
            }
        },

    }; // end wprtTheme

    // Start things up
    wprtTheme.init();

})(jQuery);