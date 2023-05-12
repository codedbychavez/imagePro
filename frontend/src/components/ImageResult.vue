<template>
  <div class="image-result-container">
    <p class="helper-text">Passed: {{ result.success }}</p>
    <p class="file-name">{{ result.file_name }}</p>
    <p class="src-original"> <a :href="result.src_original" target="_blank">{{ result.src_original }}</a></p>
    <div class="image-preview-flex-container">
      <div class="original-image-preview-wrapper">
        <p class="helper-text">Original Image</p>
        <div class="preview-image-wrapper">
          <img :src="result.src_original" />
        </div>

      </div>

      <div class="modified-image-preview-wrapper">
        <p class="helper-text">Modified Image</p>
        <div class="preview-image-wrapper">
          <img ref="modifiedImageRef" />
        </div>
      </div>
    </div>

    <div>
      <p class="helper-text">Blurry: {{ result.blurry }} | Score: {{ result.blurry_score }}</p>
    </div>

    <div class="error-container helper-text">
      Error codes:
      <p v-for="errorCode of result.error_code">{{ errorCode }}</p>
    </div>
    <div class="error-container helper-text">
      Error messages:
      <p class="flex gap-2" v-for="errorMessage of result.error_message"><IconAlertTriangle /> {{ errorMessage }}</p>
    </div>
  </div>
</template>


<script>
import IconAlertTriangle from './Icons/IconAlertTriangle.vue';
export default {
  props: {
    result: {
      type: Object,
    }
  },
  components: {
    IconAlertTriangle,
  },
  mounted() {
    let base64String = this.result.base64;
    this.$refs.modifiedImageRef.setAttribute('src', "data:image/jpg;base64," + base64String);
  },
}
</script>

<style scoped>
.image-result-container:not(first-child) {
  @apply mt-2;
}

.image-result-container {
  @apply border p-4;
}

.file-name {
  @apply text-gray-900 text-sm font-semibold;
}

.src-original {
  @apply underline text-blue-500 text-xs;
}

.image-preview-flex-container {
  @apply flex gap-4 flex-wrap items-center mt-2;
}

.original-image-preview-wrapper {
  /* @apply ; */
}

.preview-image-wrapper {
  @apply w-80;
}

.helper-text {
  @apply text-sm text-gray-700;
}

.error-container {
  @apply mt-2;
}
</style>