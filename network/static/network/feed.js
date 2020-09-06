
document.addEventListener("DOMContentLoaded", () => {

    let userid = parseInt(document.getElementById("userid").value)
    

    document.querySelectorAll(".edit").forEach((edit) => {
        edit.onclick = () => {
            let content = edit.parentElement.querySelector("p.content")
            content.setAttribute("contenteditable", "true")
            content.focus()
            content.onkeypress = (event) => {
                if(event.key === "Enter") {
                    fetch(`/post/${edit.getAttribute("value")}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                            content: content.innerHTML
                        })
                    })
                    content.setAttribute("contenteditable", "false")
                }
            }
            return false
        }
    })

    document.querySelectorAll(".likes").forEach(span => {
        let post = span.getAttribute("value")
        
        post = post.replace(/\'/g, '"');
        post = JSON.parse(post)
        updatePost(post, span)       
    })
    
    function updatePost(post, span) {
        let img = span.querySelector("img")
        span.querySelector(".likes-counter").innerHTML = post.likes.length

        if(post.likes.includes(userid)) {
            img.className="like"
            span.querySelector("a").onclick = () => {
                fetch(`/post/unlike/${post.id}`, {method: 'POST'})
                .then(response =>  response.json())
                .then(post => updatePost(post, span))     
            }
        } else {
            img.className="noliked"
            span.querySelector("a").onclick = () => {
                fetch(`/post/like/${post.id}`, {method: 'POST'})
                .then(response =>  response.json())
                .then(post => updatePost(post, span))     
            }
        }   
    }
})