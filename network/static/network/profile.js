import { drawPosts, getPosts } from "./helper.js"


document.addEventListener("DOMContentLoaded", () => {
    
    let posts_div = document.querySelector("#profile-posts")
    let profileUserid = parseInt(document.querySelector("#profile_user_id").value)
    let currentUserid = parseInt(document.querySelector("#current_user_id").value)
    
    document.querySelectorAll("#new-post-form").forEach(item => {
        item.addEventListener("submit", (event) => {
            event.preventDefault();
            let content = document.querySelector("#content-form").value
            fetch("post/new_post", {
                method: "POST",
                body: JSON.stringify({ content: content })
            }).then(() => {
                posts_div.innerHTML = ""
                document.querySelector("#content-form").value = ""
                manageProfileContent()
            });
        }) 
    })  
    
    manageProfileContent()


    function manageProfileContent() {
        let following = document.getElementById("following")
        let followers = document.getElementById("followers")
        return fetch(`profile/${profileUserid}`)
        .then((response) => response.json())
        .then((profile) => {
            following.innerHTML = profile.followings.length
            followers.innerHTML = profile.followers.length
            if (profile.userId !== currentUserid) {
                let follow_button = document.getElementById("follow_button")
                follow_button.style.display = "block"    
                // follow_button.innerHTML = profile.followers.includes(currentUserid)? "Unfollow" : "Follow"
                if (profile.followers.includes(currentUserid)) {
                    follow_button.innerHTML = "Unfollow"
                    follow_button.onclick = () => {
                        fetch(`unfollow/${profile.userId}`, { method: 'POST' })
                        .then(() => manageProfileContent())
                    }
                } else {
                    follow_button.innerHTML = "Follow"
                    follow_button.onclick = () => {
                        fetch(`follow/${profile.userId}`, { method: 'POST' })
                        .then(() => manageProfileContent())
                    }
                }
            }
            
            // return drawPosts(profile.posts, posts_div, profileUserid)
        })
    }
})