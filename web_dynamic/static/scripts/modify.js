var multiselect = document.querySelector("x-multiselect");
multiselect.addEventListener("change", function () {
	console.log("Selected items:", this.selectedItems());
});