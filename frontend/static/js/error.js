
const scrimer = document.getElementsByClassName('scrimer')[0]
const error_img = document.getElementsByClassName('error_img')[0]

const gif = scrimer.getElementsByTagName('img')[0]
const audio = scrimer.getElementsByTagName('audio')[0]

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function show_scrimer() {
    scrimer.style.display = 'flex'
    error_img.style.display = 'none'
    audio.autoplay = true
    audio.volume = 1.0
    audio.play()
}

function main() {
    audio.volume = 0.0
    sleep(1000).then(() => {
        show_scrimer()
    }) 
}


document.addEventListener("click", function handleClick() {
    document.removeEventListener("click", handleClick);
    main();
});

document.addEventListener("keydown", function handleKeyDown(event) {
    document.removeEventListener("keydown", handleKeyDown);
    main();
});

document.addEventListener("touchstart", function handleTouchStart() {
    document.removeEventListener("touchstart", handleTouchStart);
    main();
});