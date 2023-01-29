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
