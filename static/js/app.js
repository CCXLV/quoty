const buttons = document.querySelectorAll('.delete-button');

buttons.forEach(function(button) {
  button.addEventListener('click', async function() {
    const _id = button.getAttribute('data-id');

    const confirm = window.confirm("Are you sure you want to delete this document?");

    if (confirm) {
        const response = await fetch(`/quotes/delete?_id=${_id}`, {
        method: 'DELETE'
        });

        if (response.ok) {
            console.log('Document deleted successfully');
            location.reload();
        } else {
            console.log('Error deleting document');
        }
    }
  });
});


// Categories for posts

const motivationalButton = document.getElementById("motivational-button");
motivationalButton.addEventListener("click", function() {
  
  fetch('/get_data/motivational')
    const newDiv = document.createElement("div");
    newDiv.classList.add("post-div");
    document.body.appendChild(newDiv);
    .then(response => response.json())
    .then(data => {
      for (const row of data) {
        const newwDiv = document.createElement("div");
        newwDiv.classList.add("post-content");
        newwDiv.innerHTML += `<p>Author: ${row.author}</p>`
        newwDiv.innerHTML += `<p>- ${row.content}</p>`
        newwDiv.innerHTML += `< p id="date-cat">${row.category} - ${row.date.strftime('%B %d, %Y %I:%M %p')}</p>`
      }

      document.body.appendChild(newwDiv);
