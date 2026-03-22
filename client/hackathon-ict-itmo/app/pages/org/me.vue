<template>
  <Card>
    <h1>Личный кабинет</h1>

    <template v-if="user">
      <FormField label="Имя" v-model="form.firstName" type="input" />
      <FormField label="Фамилия" v-model="form.lastName" type="input" />
      <FormField label="Университет" v-model="form.university" type="input" />
      <p>Email: {{ user.email }}</p>
      <p>Роль: {{ user.roles.join(' ') }}</p>
      <p>Team ID: {{ user.teamId || "—" }}</p>
    </template>
    <p v-else>Профиль не загружен</p>

    <Button @tap="save" variant="primary">Сохранить</Button>
  </Card>
</template>

<script setup lang="ts">
import { useUserStore } from '~/stores/userStore'
import FormField from '~/components/ui/FormField.vue'
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'

const store = useUserStore()
const user = computed(() => store.getUser)
const form = reactive({
  firstName: "",
  lastName: "",
  university: ""
})

onMounted(async () => {
  try {
    const profile = await store.fetchMyProfile()
    form.firstName = profile.firstName
    form.lastName = profile.lastName
    form.university = profile.university
  } catch (error) {
    console.error(error)
    alert("Не удалось загрузить профиль")
  }
})

async function save() {
  try {
    await store.updateMyProfile({
      firstName: form.firstName,
      lastName: form.lastName,
      university: form.university
    })
    alert('Сохранено!')
  } catch (error) {
    console.error(error)
    alert("Не удалось сохранить профиль")
  }
}
</script>