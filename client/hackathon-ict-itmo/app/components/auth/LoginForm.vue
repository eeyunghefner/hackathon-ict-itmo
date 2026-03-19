<template>
  <Card>
    <h2>Вход</h2>

    <FormField label="Email" v-model="email" type="input" />
    <FormField label="Пароль" v-model="password" type="input" />

    <Button @click="submit" variant="primary">
      Войти
    </Button>
  </Card>
</template>

<script setup lang="ts">
import { ref } from "vue"
import { useAuthStore } from "~/stores/authStore"
import Card from "~/components/ui/Card.vue"
import FormField from "~/components/ui/FormField.vue"
import Button from "~/components/ui/Button.vue"

const auth = useAuthStore()

const email = ref("")
const password = ref("")

const router = useRouter()

async function submit() {
  try {
    await auth.login(email.value, password.value)
    router.push("/")
  } catch (e) {
    alert("Ошибка входа")
  }
}
</script>