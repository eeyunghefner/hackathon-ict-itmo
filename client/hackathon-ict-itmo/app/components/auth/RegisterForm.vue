<template>
  <Card>
    <h2>Регистрация</h2>

    <FormField label="Email" v-model="email" type="input" />
    <FormField label="Пароль" v-model="password" type="input" />
    <FormField label="Имя" v-model="firstName" type="input" />
    <FormField label="Фамилия" v-model="lastName" type="input" />
    <FormField label="Университет" v-model="university" type="input" />

    <Button @tap="submit" variant="primary">
      Зарегистрироваться
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
const firstName = ref("")
const lastName = ref("")
const university = ref("")

const router = useRouter()

async function submit() {
  try {

    await auth.register({
      email: email.value,
      password: password.value,
      firstName: firstName.value,
      lastName: lastName.value,
      university: university.value,
      isuNumber: '367801'
    })

    router.push("/")
  } catch (e) {
    console.error(e)
    alert("Ошибка регистрации")
  }
}
</script>