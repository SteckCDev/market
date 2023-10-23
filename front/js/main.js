function setRating(stars) {
    const filled_star_path = "img/star.svg"
    const unfilled_star_path = "img/star_unfilled.svg"

    let actual_input = document.getElementById("reviewRatingHidden");
    actual_input.value = stars;

    for (let i = 1; i <= 5; i++) {
        let star_svg = document.getElementById("reviewRating" + String(i))

        if (i <= stars) {
            star_svg.setAttribute("src", filled_star_path);
        } else {
            star_svg.setAttribute("src", unfilled_star_path);
        }
    }
}