document.addEventListener("DOMContentLoaded", function () {
		// Universal Custom Select Handler
		class CustomSelect {
			constructor(wrapper) {
				this.wrapper = wrapper;
				this.selectId = wrapper.dataset.selectId;
				this.originalSelect = document.getElementById(this.selectId);
				this.button = wrapper.querySelector(".select-btn");
				this.selectedText = wrapper.querySelector(".selected-text");
				this.dropdown = wrapper.querySelector(".dropdown-menu");
				this.dropdownList = wrapper.querySelector(".dropdown-menu ul");

				if (!this.originalSelect) {
					console.warn(`Select element with id "${this.selectId}" not found`);
					return;
				}

				this.init();
			}

			init() {
				this.populateDropdown();
				this.setupEventListeners();
				this.setInitialValue();
			}

			populateDropdown() {
				// Populate the custom dropdown with options from the original select
				for (let option of this.originalSelect.options) {
					const li = document.createElement("li");
					li.textContent = option.text;
					li.dataset.value = option.value;
					li.classList.add("px-4", "py-2", "bg-blur", "cursor-pointer");

					// Mark as selected if it's the currently selected option
					if (option.selected) {
						li.classList.add("bg-gray-900");
						this.selectedText.textContent = option.text;
					}

					li.addEventListener("click", () => this.selectOption(li));
					this.dropdownList.prepend(li);
				}
			}

			selectOption(optionElement) {
				// Update the original select value
				this.originalSelect.value = optionElement.dataset.value;

				// Trigger both 'change' and 'input' events
				["change", "input"].forEach((eventName) => {
					const event = new Event(eventName, { bubbles: true });
					this.originalSelect.dispatchEvent(event);
				});

				// Update the button text
				this.selectedText.textContent = optionElement.textContent;

				// Hide the dropdown with animation
				this.hideDropdown();

				// Update selected visual state
				this.dropdownList.querySelectorAll("li").forEach((item) => {
					item.classList.remove("bg-gray-900");
				});
				optionElement.classList.add("bg-gray-900");
			}

			showDropdown() {
				this.dropdown.classList.remove("hidden");
				setTimeout(() => {
					this.dropdown.classList.remove("opacity-0", "scale-95");
					this.dropdown.classList.add("opacity-100", "scale-100");
				}, 10);
			}

			hideDropdown() {
				this.dropdown.classList.remove("opacity-100", "scale-100");
				this.dropdown.classList.add("opacity-0", "scale-95");
				setTimeout(() => {
					this.dropdown.classList.add("hidden");
				}, 200);
			}

			toggleDropdown() {
				if (this.dropdown.classList.contains("hidden")) {
					this.showDropdown();
				} else {
					this.hideDropdown();
				}
			}

			setInitialValue() {
				// If no option was initially selected, show the first available option text
				const defaultText = this.selectedText.textContent;
				const hasPlaceholder = defaultText.includes("Select a");

				if (hasPlaceholder && this.originalSelect.options.length > 0) {
					// Check if there's a selected option
					const selectedOption = Array.from(this.originalSelect.options).find((opt) => opt.selected);
					if (selectedOption) {
						this.selectedText.textContent = selectedOption.text;
					} else if (this.originalSelect.options[0].value !== "") {
						this.selectedText.textContent = this.originalSelect.options[0].text;
					}
				}
			}

			setupEventListeners() {
				// Toggle dropdown when button is clicked
				this.button.addEventListener("click", () => this.toggleDropdown());

				// Close dropdown when clicking outside
				document.addEventListener("click", (event) => {
					if (!this.button.contains(event.target) && !this.dropdown.contains(event.target) && !this.dropdown.classList.contains("hidden")) {
						this.hideDropdown();
					}
				});
			}
		}

		// Initialize all custom selects
		const customSelectWrappers = document.querySelectorAll(".custom-select-wrapper");
		const customSelects = [];

		customSelectWrappers.forEach((wrapper) => {
			const customSelect = new CustomSelect(wrapper);
			customSelects.push(customSelect);
		});

		// Make customSelects available globally if needed for debugging
		window.customSelects = customSelects;
	});