function drawPosts(posts, parentElement, currentUserId) {
    return posts.forEach(post => {
        // Create row
        let row = document.createElement("div")
        row.className = "row mt-1"
        parentElement.append(row)
        // Create column
        let column = document.createElement("div")
        column.className = "col-12"
        row.append(column)
        // Create span poster
        let poster = document.createElement("a")
        poster.className = "poster"
        poster.innerHTML = post.user
        poster.href = `/${post.user}`
        column.append(poster)
        // Add a line break
        column.append(document.createElement("br"))
        column.append(document.createElement("br"))
        if (currentUserId == post.userId) {
           createEditButton(column, post.id)
        }

        // Create p content
        let content = document.createElement("p")
        content.className = "content"
        content.innerHTML = post.content
        column.append(content)
        // Create span timestamp
        let timestamp = document.createElement("span")
        timestamp.className = "timestamp"
        timestamp.innerHTML = post.timestamp
        column.append(timestamp)
        // Add a line break
        column.append(document.createElement("br"))
        //Create span likes
        let likes = document.createElement("span")
        likes.className = "likes"
        likes.innerHTML = post.likes
        column.append(likes)
        // Add a line break
        column.append(document.createElement("br"))
        //Create a comment
        let commment = document.createElement("a")
        commment.className = "comment"
        commment.innerHTML = "comment"
        column.append(commment)
    });
}

function createEditButton(parentElement, post_id) {
    // Create a Edit
    let edit = document.createElement("a")
    edit.className = "edit"
    edit.innerHTML = "Edit"
    edit.href = ""
    parentElement.append(edit)
    
    edit.onclick = () => {
        let content = edit.parentElement.querySelector("p.content")
        content.setAttribute("contenteditable", "true")
        content.focus()
        content.onkeypress = (event) => {
            if(event.key === "Enter") {
                fetch(`/post/${post_id}`, {
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
}

function getPosts (option) {
    return fetch(`posts/${option}`)
    .then(response => response.json())
}

export { drawPosts, getPosts }