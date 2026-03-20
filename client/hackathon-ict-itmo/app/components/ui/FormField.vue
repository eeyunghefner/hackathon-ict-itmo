<template>
  <div class="form-field">
    <label v-if="label">{{ label }}</label>
    <component
      :is="componentType"
      :value="modelValue"
      @input="handleInput"
      @update:modelValue="handleUpdate"
      v-bind="attrs"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue"

const props = defineProps<{
  modelValue: string | number
  label?: string
  type?: "input" | "textarea" | "select"
}>()

const emit = defineEmits<{
  (e: "update:modelValue", value: string | number): void
}>()

const attrs = useAttrs()

const componentType = computed(() => props.type || 'input')

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement | HTMLTextAreaElement
  emit('update:modelValue', target.value)
}

const handleUpdate = (value: string | number) => {
  emit('update:modelValue', value)
}
</script>