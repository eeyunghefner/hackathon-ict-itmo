<template>
  <div class="form-field">
    <label v-if="label">{{ label }}</label>
    <component
      :is="type || 'input'"
      v-model="localValue"
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

const localValue = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val)
})
</script>