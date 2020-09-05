import { drawPosts, getPosts } from "./helper.js"


document.addEventListener("DOMContentLoaded", () => {

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
                    });
                    content.setAttribute("contenteditable", "false")
                }
            }
            return false
        }
    })
    
  
})