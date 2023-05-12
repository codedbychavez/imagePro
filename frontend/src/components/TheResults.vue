<template>
  <div class="results-container">
    <h2 class="form-title">Results</h2>
    <p class="text-gray-600 my-4">Results will be displayed here</p>
    <div v-for="result in results" :key="result" class="result">
      <ImageResult :result="result" />
    </div>
  </div>
</template>

<script>
import ImageResult from './ImageResult.vue';

export default {
  components: {
    ImageResult,
},
  props: {
    results: {
      type: Array,
    }
  },
}

</script>

<style scoped>

.results-container {
  @apply p-4;
}

</style>