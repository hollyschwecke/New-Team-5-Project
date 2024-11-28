// frontend code, linked to html
document.addEventListener("DOMContentLoaded", function() {
  const productNameInput = document.getElementById("product-name");
  const categorySelect = document.getElementById("category");
  const priceInput = document.getElementById("price");
  const descriptionTextarea = document.getElementById("description");
  const quantityInput = document.getElementById("quantity");
  const form = document.querySelector("form");

  form.addEventListener("submit", async function(event) {
    event.preventDefault(); // prevent form submission

    // validate fields
    if (!productNameInput.value || !categorySelect.value || !priceInput.value || !descriptionTextarea.value || !quantityInput.value) {
      alert("Please fill in all required fields.");
      return;
    }
    
    const formData = new FormData();
    formData.append("productName", productNameInput.value);
    formData.append("category", categorySelect.value);
    formData.append("price", priceInput.value);
    formData.append("description", descriptionTextarea.value);
    formData.append("quantity", quantityInput.value);
    
    try {
      const response = await fetch("backend url", {
        method: "POST",
          body: formData,
      });
      
      const data = await response.json();
      
      if (response.ok) {
        alert(data.message); // success message
        form.reset();
      } else {
        alert("Error: " + data.message); // error handling
      }
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("An error occurred while submitting the form.");
    }
  });
});
