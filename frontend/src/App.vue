<template>
  <TheHeader />

  <div class="main-wrapper">
    <TheMain />
  </div>
</template>

<script>
import TheHeader from './components/TheHeader.vue';
import TheMain from './components/TheMain.vue';

export default {
  components: {
    TheHeader, TheMain
  }
}
</script>

<style scoped>

.main-wrapper {
  @apply w-11/12 mx-auto bg-white mt-8 rounded-lg;
}
</style>