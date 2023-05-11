<template>
  <div class="options-form-container">
    <h2 class="form-title">Define options</h2>
    <div class="input-group">
      <label class="input-label" for="api-endpoint"
        >Enter processor API Endpoint</label
      >
      <input
        class="api-endpoint-input"
        id="resolution-min-width"
        type="text"
        :placeholder="APIEndpoint"
        @keyup="handleSetAPIEndpoint($event)"
      />
      <p class="helper-text">Default: {{ APIEndpoint }}</p>
      <p class="helper-text mt-2 underline text-blue-500">
        <a href="https://github.com/codedbychavez/imagepro" target="_blank"
          >How to launch backend?</a
        >
      </p>
    </div>

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
            v-model="formData.resolution_min_width"
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
            v-model="formData.resolution_min_height"
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
            v-model="formData.square_images"
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
            v-model="formData.blur_check"
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
            v-model="formData.padding_remove"
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
            v-model="formData.padding_add"
          />
          <p class="helper-text">Default: 10px</p>
        </div>
      </div>
      <div class="input-group">
        <label class="input-label" for="image-url"
          >7. Add URLs of images to process</label
        >

        <div v-for="(image, index) in imageURLs" class="image-input-wrapper">
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
      imageURLs: [],
      formData: {
        resolution_width_min: 1000,
        resolution_height_min: 1000,
        square_images: false,
        blur_check: true,
        blur_threshold: 100,
        padding_remove: false,
        padding_add: 10,
        images: [],
      },
      isProcessing: false,
      formIsValid: false,
      APIEndpoint: "http://127.0.0.1:5000/api/process-images",
    };
  },
  methods: {
    handleSetAPIEndpoint(event) {
      const urlRegex =
        /^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$/;
      if (urlRegex.test(event.target.value)) {
        this.APIEndpoint = event.target.value;
      }
    },
    async handleFormSubmit(event) {
      this.isProcessing = true;
      if (this.formIsValid) {
        this.formData.images = this.imageURLs;
        const postDataResponse = await this.postData(
          this.APIEndpoint,
          this.formData
        )
          .then((response) => {
            console.log(response);
            this.isProcessing = false;
          })
          .catch((err) => {
            console.log("There was an error, is the backend running?");
            this.isProcessing = false;
          });
      }
    },

    async postData(url, data) {
      const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      return response.json();
    },

    handleAddImage() {
      this.imageURLs.push("");
    },

    handleDeleteImage(index) {
      this.imageURLs.splice(index, 1);
      if (this.imageURLs.length == 0) this.formIsValid = false;
    },

    handleUpdateImageUrl(event, index) {
      var imageUrlRegex = /(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png)/g;
      let theElementRef = `imageInput${index}`;
      if (imageUrlRegex.test(event.target.value)) {
        this.imageURLs[index] = event.target.value;
        this.$refs[theElementRef][0].classList.remove("input-text-error");
        this.formIsValid = true;
      } else {
        this.$refs[theElementRef][0].classList.add("input-text-error");
        this.formIsValid = false;
      }
    },
  },
  watch: {
    imageURLs: {
      handler() {
        this.imageURLs.forEach((imageURL) => {
          if (imageURL != "") {
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

.image-input,
.api-endpoint-input {
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
