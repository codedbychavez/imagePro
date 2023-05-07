<template>
  <header class="the-header">
    <div class="navbar-wrapper">
      <Navbar />
    </div>
  </header>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  components: {
    Navbar
  }
}

</script>

<style scoped>

.the-header {
  @apply bg-gray-100 p-4;
}
</style>