<template>
  <Card>
    <h1>Личный кабинет</h1>

    <FormField label="ФИО" v-model="user.fullName" type="input" />
    <FormField label="Образование" v-model="user.education" type="input" />
    <FormField label="Навыки" v-model="user.skills" type="input" />
    <FormField label="Описание" v-model="user.description" type="textarea" />

    <Button @click="save" variant="primary">Сохранить</Button>
  </Card>
</template>

<script setup lang="ts">
import { useUserStore } from '~/stores/userStore'
import FormField from '~/components/ui/FormField.vue'
import Card from '~/components/ui/Card.vue'
import Button from '~/components/ui/Button.vue'

const store = useUserStore()
const user = store.getUser

function save() {
  store.updateUser(user)
  alert('Сохранено!')
}
</script>