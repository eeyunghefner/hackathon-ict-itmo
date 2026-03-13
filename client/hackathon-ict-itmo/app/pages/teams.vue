<template>
  <Card>
    <h1>Поиск команд</h1>
    <FormField label="Поиск" v-model="query" type="input" />
  </Card>

  <Table
    :headers="['Команда', 'Количество участников', 'Действие']"
    :rows="teams.map(t => [t.name, t.members, 'Подать заявку'])"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useTeamStore } from '~/stores/teamStore'
import Card from '~/components/ui/Card.vue'
import Table from '~/components/ui/Table.vue'
import FormField from '~/components/ui/FormField.vue'

const query = ref('')
const store = useTeamStore()

const teams = store.getTeams
</script>