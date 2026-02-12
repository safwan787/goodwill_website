// gd_admin/js/ai.js

document.addEventListener("DOMContentLoaded", function () {

  const aiButton = document.getElementById("ai-generate-product");
  if (!aiButton) return; // not on product page

  const errorBox = document.getElementById("ai-error");

  function getCSRFToken() {
    const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return tokenInput ? tokenInput.value : "";
  }

  function setLoading(button, loading) {
    button.disabled = loading;
    button.innerText = loading ? "Generating..." : "✨ Generate with AI";
  }

  aiButton.addEventListener("click", async function () {
    errorBox.style.display = "none";

    const nameField = document.getElementById("id_name");
    const descriptionField = document.getElementById("id_description");

    if (!nameField || !descriptionField) return;

    const name = nameField.value.trim();

    if (!name) {
      errorBox.innerText = "Please enter the product name first.";
      errorBox.style.display = "block";
      return;
    }

    setLoading(aiButton, true);

    try {
      const response = await fetch("/ai/product-description/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          name: name,
        }),
      });

      const data = await response.json();

      if (data.success) {
        descriptionField.value = data.description;
        descriptionField.focus();
      } else {
        errorBox.innerText = data.error || "AI generation failed.";
        errorBox.style.display = "block";
      }
    } catch (error) {
      errorBox.innerText = "Something went wrong. Please try again.";
      errorBox.style.display = "block";
    } finally {
      setLoading(aiButton, false);
    }
  });

});

// ---------- CATEGORY AI ----------

const categoryButton = document.getElementById("ai-generate-category");

if (categoryButton) {
  const categoryErrorBox = document.getElementById("ai-category-error");

  categoryButton.addEventListener("click", async function () {
    categoryErrorBox.style.display = "none";

    const nameField = document.getElementById("id_name");
    const descriptionField = document.getElementById("id_description");

    if (!nameField || !descriptionField) return;

    const categoryName = nameField.value.trim();

    if (!categoryName) {
      categoryErrorBox.innerText = "Please enter the category name first.";
      categoryErrorBox.style.display = "block";
      return;
    }

    categoryButton.disabled = true;
    categoryButton.innerText = "Generating...";

    try {
      const response = await fetch("/ai/category-description/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({
          category_name: categoryName,
        }),
      });

      const data = await response.json();

      if (data.success) {
        descriptionField.value = data.description;
        descriptionField.focus();
      } else {
        categoryErrorBox.innerText = data.error || "AI generation failed.";
        categoryErrorBox.style.display = "block";
      }
    } catch (error) {
      categoryErrorBox.innerText = "Something went wrong. Please try again.";
      categoryErrorBox.style.display = "block";
    } finally {
      categoryButton.disabled = false;
      categoryButton.innerText = "✨ Generate with AI";
    }
  });
}
