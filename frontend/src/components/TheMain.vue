<template>
  <main class="the-main">
    <div class="options-form-wrapper">
      <OptionsForm />
    </div>
  </main>
</template>

<script>
import OptionsForm from './OptionsForm.vue';
export default {

  components: {
    OptionsForm,
  }
}

</script>

<style scoped>

.the-main {
  @apply p-4;
}

</style>