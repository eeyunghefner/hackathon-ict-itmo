<template>
  <Card>
    <h1>Создание команды</h1>

    <FormField label="Название" v-model="name" type="input" />
    <FormField label="Описание" v-model="description" type="textarea" />

    <div class="actions">
      <Button @click="create" variant="primary" :disabled="!name.trim()">
        Создать
      </Button>

      <Button @click="back" variant="secondary">
        Назад
      </Button>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { computed, ref } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useTeamStore } from "~/stores/teamStore"
import Card from "~/components/ui/Card.vue"
import FormField from "~/components/ui/FormField.vue"
import Button from "~/components/ui/Button.vue"

const store = useTeamStore()
const route = useRoute()
const router = useRouter()

const hackathonId = computed(() => {
  const v = route.query.hackathonId
  return typeof v === "string" && v.length ? v : undefined
})

const name = ref("")
const description = ref("")

async function create() {
  try {
    await store.createTeam({
      name: name.value,
      description: description.value
    })

    router.push({
      path: "/teams",
      query: hackathonId.value ? { hackathonId: hackathonId.value } : {}
    })
  } catch (e) {
    console.error(e)
    alert("Не удалось создать команду")
  }
}

function back() {
  router.push({
    path: "/teams",
    query: hackathonId.value ? { hackathonId: hackathonId.value } : {}
  })
}
</script>

<style scoped>
.actions {
  display: flex;
  gap: 1rem;
  margin-top: var(--space-md);
}
</style>

