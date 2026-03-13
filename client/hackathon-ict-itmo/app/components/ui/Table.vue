<template>
  <table>
    <thead>
      <tr>
        <th v-for="header in headers" :key="header">{{ header }}</th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(row, idx) in rows"
        :key="idx"
        @click="$emit('row-click', row)"
        class="hover-row"
      >
        <td v-for="cell in row" :key="cell">{{ cell }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script setup lang="ts">
const props = defineProps<{
  headers: string[]
  rows: (string | number)[][]
}>()
</script>

<style scoped>
.hover-row:hover {
  background-color: #f0f0f0;
  cursor: pointer;
}
</style>