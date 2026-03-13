<template>
  <div>
    <h1>Личный кабинет</h1>

    <div>
      <label>ФИО</label>
      <input v-model="user.fullName" />
    </div>

    <div>
      <label>Образование</label>
      <input v-model="user.education" />
    </div>

    <div>
      <label>Навыки</label>
      <input v-model="user.skills" />
    </div>

    <div>
      <label>Описание</label>
      <textarea v-model="user.description"></textarea>
    </div>

    <button @click="save">Сохранить</button>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "~/stores/userStore"

const userStore = useUserStore()

const user = userStore.user

function save() {
  userStore.updateUser(user)
}
</script>