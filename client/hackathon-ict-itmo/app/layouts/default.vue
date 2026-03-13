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