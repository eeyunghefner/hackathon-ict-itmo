<template>
  <div>
    <OrgNavbar />

    <main>
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import OrgNavbar from "~/components/OrgNavbar.vue"
</script>