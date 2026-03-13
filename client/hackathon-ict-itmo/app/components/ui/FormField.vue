<template>
  <div class="form-field">
    <label v-if="label">{{ label }}</label>
    <component
      :is="type"
      v-model="modelValue"
      v-bind="attrs"
    ></component>
  </div>
</template>

<script setup lang="ts">
import { toRefs } from "vue"

const props = defineProps<{
  modelValue: string | number
  label?: string
  type?: 'input' | 'textarea' | 'select'
}>()

const emit = defineEmits(['update:modelValue'])

const { modelValue } = toRefs(props)

const attrs = useAttrs()

watch(modelValue, (val) => {
  emit('update:modelValue', val)
})
</script>

<style scoped>
.form-field {
  margin-bottom: var(--space-md);
}

label {
  display: block;
  margin-bottom: var(--space-sm);
  font-weight: 600;
}
</style>