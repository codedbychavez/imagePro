<template>
  <div class="options-form-container">
    <h2 class="form-title">Define options</h2>
    <form @submit.prevent="handleFormSubmit($event)" class="options-form">
      <div class="form-flex-container">
        <div class="input-group">
          <label class="input-label" for="resolution-min-width"
            >1. Enter resolution min width (e.g. 1000)</label
          >
          <input
            id="resolution-min-width"
            type="number"
            placeholder="Resolution min width"
            v-model="resolution_min_width"
          />
          <p class="helper-text">Default: 1000px</p>
        </div>
        <div class="input-group">
          <label class="input-label" for="resolution-min-height"
            >2. Enter resolution min height (e.g. 1000)</label
          >
          <input
            id="resolution-min-width"
            type="number"
            placeholder="Resolution min height"
            v-model="resolution_min_height"
          />
          <p class="helper-text">Default: 1000px</p>
        </div>
        <div class="input-group">
          <label class="input-label" for="square-images"
            >3. Square Images?</label
          >
          <input
            id="square-images"
            type="checkbox"
            v-model="square_images"
          />
          <p class="helper-text">Default: No</p>
        </div>
        <div class="input-group">
          <label class="input-label" for="check-for-blurry-images"
            >4. Check for blurry images?</label
          >
          <input
            id="check-for-blurry-images"
            type="checkbox"
            v-model="blur_check"
          />
          <p class="helper-text">Default: Yes</p>
        </div>
        <div class="input-group">
          <label class="input-label" for="remove-padding"
            >5. Remove padding from images?</label
          >
          <input
            id="remove-padding"
            type="checkbox"
            v-model="padding_remove"
          />
          <p class="helper-text">Default: No</p>
        </div>
        <div class="input-group">
          <label class="input-label" for="add-padding"
            >6. Padding to add in pixels (e.g. 10)</label
          >
          <input
            id="add-padding"
            type="number"
            placeholder="10"
            v-model="padding_add"
          />
          <p class="helper-text">Default: 10px</p>
        </div>
      </div>
      <div class="input-group">
        <label class="input-label" for="image-url"
          >7. Add URLs of images to process</label
        >

        <div v-for="(image, index) in images" class="image-input-wrapper">
          <input
            :ref="`imageInput${index}`"
            @keyup="handleUpdateImageUrl($event, index)"
            class="image-input"
            id="image-url"
            type="text"
            placeholder="https://your-image-url.com/my-image.jpg"
            required
          />
          <button
            @click="handleDeleteImage(index)"
            class="ml-2 p-2 text-sm rounded-full bg-red-500 text-white"
          >
            <IconTrash />
          </button>
        </div>

        <button type="button" class="add-image-button" @click="handleAddImage">
          Add image
        </button>
      </div>

      <div class="submit-button-wrapper">
        <button
          :disabled="isProcessing | !formIsValid"
          class="submit-button"
          type="submit"
        >
          {{ isProcessing ? "Processing..." : "Process Images" }}
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import IconTrash from "./Icons/IconTrash.vue";

export default {
  components: {
    IconTrash,
  },
  data() {
    return {
      resolution_min_width: 1000,
      resolution_min_height: 1000,
      square_images: false,
      blur_check: true,
      blur_threshold: 100,
      padding_remove: false,
      padding_add: 10,
      images: [],
      isProcessing: false,
      formIsValid: false,
    };
  },
  methods: {
    handleFormSubmit(event) {
      if (this.images.length > 0) {
        console.log("Valid");
      }
      console.log("The form was submitted");
    },

    handleAddImage() {
      this.images.push("");
    },

    handleDeleteImage(index) {
      this.images.splice(index, 1);
    },

    handleUpdateImageUrl(event, index) {
      var imageUrlRegex = /(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png)/g;
      let theElementRef = `imageInput${index}`;
      if (imageUrlRegex.test(event.target.value)) {
        this.images[index] = event.target.value;
        this.$refs[theElementRef][0].classList.remove("input-text-error");
      } else {
        this.$refs[theElementRef][0].classList.add("input-text-error");
        this.formIsValid = false;
      }
    },
  },
  watch: {
    images: {
      handler() {
        console.log("hello");
        this.images.forEach((image) => {
          if (image != "") {
            this.formIsValid = true;
          } else this.formIsValid = false;
        });
      },
      deep: true,
    },
  },
};
</script>

<style>
.options-form-container {
  @apply bg-gray-50 p-4 rounded-lg;
}

.form-title {
  @apply font-bold text-xl;
}

.input-text-error {
  @apply border border-red-500;
}

.input-text-ok {
  @apply border border-green-500;
}

.options-form {
  @apply mt-8;
}

.form-flex-container {
  @apply flex flex-wrap;
}

.input-group {
  @apply flex-col m-4;
}

.input-label {
  @apply block mb-2 font-semibold;
}

.helper-text {
  @apply text-xs;
}

.image-input-wrapper {
  @apply mt-2 flex;
}

.image-input {
  @apply w-96;
}

.add-image-button {
  @apply bg-violet-500 px-2 py-1 text-white rounded mt-2;
}

.submit-button-wrapper {
  @apply text-right;
}

.submit-button {
  @apply bg-green-500 text-gray-50 px-4 py-2 rounded-lg disabled:bg-gray-400 shadow;
}
</style>
