$video_carousel = $('#myCarousel');


$video_carousel.carousel({
    interval:30000
});

$video_carousel.on('slide.bs.carousel', function onSlide (ev) {
    var vid = ev.relatedTarget;
    vid.currentTime = 0;
    vid.play();
});
