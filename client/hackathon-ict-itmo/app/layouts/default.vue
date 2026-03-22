<template>
  <div>
    <Navbar />

    <main>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import Navbar from "~/components/Navbar.vue"
</script>

<style>
.right-margin {
  margin-right: 1.5rem;
}
</style>