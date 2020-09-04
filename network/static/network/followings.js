import { drawPosts, getPosts } from "./helper.js"

document.addEventListener("DOMContentLoaded", () => {
    let post_div = document.getElementById("followings-posts")
    let userid = document.querySelector("#userid").value

    getPosts("followings")
    .then(posts => drawPosts(posts, post_div, userid))
    
})