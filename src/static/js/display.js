// VIDEO CAROUSEL
$video_carousel = $('#myCarousel');

$video_carousel.carousel({
    interval:30000
});

$video_carousel.on('slide.bs.carousel', function onSlide (ev) {
    var vid = ev.relatedTarget;
    vid.currentTime = 0;
    vid.play();
});


//EVENT BAR
setInterval(function(){
    setTimeout(function(){
            $events = $('#events');
            $event_cards = $events.find("div.card");
            if ($event_cards.length > 4){
                $event_cards[4].scrollIntoView({behavior: 'smooth', block: 'end'});
            }
        },
        4500);
        $events.append($event_cards[0]);
    },
    7000
);