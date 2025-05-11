const mushroomInput = document.getElementById("mushroom_image");
const filePreview = document.getElementById("file-preview");

if (mushroomInput && filePreview) {
  mushroomInput.addEventListener("change", function (e: Event) {
    const input = e.target as HTMLInputElement;
    filePreview.innerHTML = "";

    if (input.files && input.files[0]) {
      const file = input.files[0];
      const reader = new FileReader();

      reader.onload = function (e: ProgressEvent<FileReader>) {
        const result = e.target?.result;
        if (typeof result === "string") {
          const img = document.createElement("img");
          img.src = result;
          filePreview.appendChild(img);

          const filename = document.createElement("p");
          filename.textContent = file.name;
          filePreview.appendChild(filename);
        }
      };

      reader.readAsDataURL(file);
    }
  });
}
