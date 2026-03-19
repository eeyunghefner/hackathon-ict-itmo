<template>
  <button
    :class="variant"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
const props = defineProps<{
  variant?: 'primary' | 'secondary'
  disabled?: boolean
}>()

const variant = props.variant === 'secondary' ? 'secondary' : 'primary'
</script>

<style scoped>
button.primary {
  background-color: var(--color-primary);
  color: var(--color-white);
}

button.primary:hover {
  background-color: #0f3499;
}

button.secondary {
  background-color: var(--color-white);
  color: var(--color-black);
  border: 1px solid var(--color-black);
}

button.secondary:hover {
  background-color: var(--color-gray);
}
</style>