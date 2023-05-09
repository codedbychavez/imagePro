<template>
  <div class="options-form-container">
    <h2 class="form-title">Define options</h2>
    <form @submit.prevent="handleFormSubmit" class="options-form">
      <div class="input-group">
        <label class="input-label" for="resolution-min-width">Enter resolution min width</label>
        <input id="resolution-min-width" type="number" placeholder="Resolution min width" />
        <p class="helper-text">Default: 1000px</p>
      </div>
    </form>
  </div>
</template>

<script>

export default {
  data() {
    return {
      resolution_min_width: 1000,
      resolution_min_height: 1000,
      square_images: true,
      blur_check: true,
      blur_threshold: 100,
      padding_remove: false,
      padding_add: 10,
      images: []
    }
  },
  methods: {
    handleFormSubmit() {
      console.log('The form was submitted');
    }
  }
}

</script>

<style>

.options-form-container {
  @apply bg-gray-50 p-4 rounded-lg;
}

.form-title {
  @apply font-bold text-xl;
}


.options-form {
  @apply mt-8;
}

.input-group {
  @apply flex-col;
}

.input-label {
  @apply block mb-2 font-semibold;
}

.helper-text {
  @apply text-xs;
}

</style>