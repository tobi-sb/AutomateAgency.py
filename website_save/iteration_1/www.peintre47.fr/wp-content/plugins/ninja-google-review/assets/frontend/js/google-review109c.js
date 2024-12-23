jQuery(document).ready(function () {
  // var columnsSlides = jQuery(".njt-reviews-carousel-column").data("column");
  // var carouselAutoplay= jQuery(".njt-google-places-reviews-wap").data("carousel-autoplay");
  // var carouselAutoplaySpeed = jQuery(".njt-google-places-reviews-shortcode .njt-google-places-reviews-wap").data("carousel-speed");
  jQuery('.btn-reivew').click(function()
    {
      jQuery(this).data('clicked',!jQuery(this).data('clicked'));

    if (jQuery(this).data('clicked'))
        {
          var id = jQuery(this).data("id");

          jQuery(this).text(njt_ggreviews.read_less);
    
          jQuery("#" + id + " .review-item-long").show();
    
          jQuery("#" + id + " .review-item-short").hide();
        }
    else
        {
          var id = jQuery(this).data("id");

          jQuery(this).text(njt_ggreviews.read_more);
    
          jQuery("#" + id + " .review-item-long").hide();
    
          jQuery("#" + id + " .review-item-short").show();
        }
    });
  jQuery(".njt-google-places-reviews-wap[data-id]").each(function (index) {
    var thisElement = this;

    var columnsSlides = jQuery(thisElement)
      .find(".njt-reviews-carousel-column")
      .data("column");
    var carouselAutoplay = jQuery(thisElement).data("carousel-autoplay");
    var carouselAutoplaySpeed = jQuery(thisElement).data("carousel-speed");
    var getDir = jQuery('html').attr('dir');
    var setDir = false
    if(getDir == 'rtl') {
      setDir = true;
    }
    if(jQuery('.njt-reviews-carousel-wrap').length > 0) {
      jQuery(thisElement)
      .find(".njt-reviews-carousel-wrap")
      .slick({
        rtl: setDir,
        show: 1,
        slidesToShow: columnsSlides,
        slidesToScroll: columnsSlides,
        responsive: [
          {
            breakpoint: 600,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
        prevArrow: '<div class="njt-gr-slick-prev"></div>',
        nextArrow: '<div class="njt-gr-slick-next"></div>',
        dots: false,
        autoplay: carouselAutoplay == true ? true : false,
        autoplaySpeed: carouselAutoplaySpeed
          ? Number(carouselAutoplaySpeed)
          : 3000,
      });
    }
    
  });
  // jQuery(".njt-reviews-carousel-wrap").slick({
  //   show: 1,
  //   slidesToShow: columnsSlides,
  //   slidesToScroll: columnsSlides,
  //   prevArrow: '<div class="njt-gr-slick-prev"></div>',
  //   nextArrow: '<div class="njt-gr-slick-next"></div>',
  //   dots: false,
  //   autoplay: carouselAutoplay == true ? true : false,
  //   autoplaySpeed: carouselAutoplaySpeed ? Number(carouselAutoplaySpeed) : 3000
  // });
});
