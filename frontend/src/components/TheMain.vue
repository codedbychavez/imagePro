<template>
  <main class="the-main">
    <div class="options-form-wrapper">
      <OptionsForm @results="handleResults" />
    </div>
    <div class="the-results-wrapper">
      <TheResults :results="emittedResults" />
    </div>
  </main>
</template>

<script>
import OptionsForm from './OptionsForm.vue';
import TheResults from './TheResults.vue';

export default {

  components: {
    OptionsForm,
    TheResults
  },

  data() {
    return {
      emittedResults: [],
    }
  },
  methods: {
    handleResults(results) {
      this.emittedResults = results;
    }
  }
}

</script>

<style scoped>

.the-main {
  @apply p-4;
}

.options-form-wrapper {
  @apply bg-white rounded-lg;
}

.the-results-wrapper {
  @apply bg-white rounded-lg mt-4;
}

</style>