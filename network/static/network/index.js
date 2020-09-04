import { drawPosts, getPosts } from "./helper.js"


document.addEventListener("DOMContentLoaded", () => {
    
    let posts_div = document.querySelector("#posts")
    let userid = document.querySelector("#userid").value
    getPosts("all").then(posts => drawPosts(posts, posts_div, userid))

    // document.querySelector("#new-post-form").addEventListener("submit", (event) => {
    //     event.preventDefault();
    //     let content = document.querySelector("#content-form").value
    //     fetch("new_post", {
    //         method: "POST",
    //         body: JSON.stringify({ content: content })
    //     })
    //     .then(() => {
    //         posts_div.innerHTML = ""
    //         document.querySelector("#content-form").value = ""
    //         return getPosts().then(posts => drawPosts(posts, posts_div, userid))
    //     });
    // })  
})