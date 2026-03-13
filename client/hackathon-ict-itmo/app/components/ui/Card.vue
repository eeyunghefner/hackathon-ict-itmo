<template>
  <div class="card">
    <slot />
  </div>
</template>

<style scoped>
.card {
  background-color: var(--color-white);
  padding: var(--space-md);
  border-radius: var(--radius);
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  margin-bottom: var(--space-lg);
}
</style>